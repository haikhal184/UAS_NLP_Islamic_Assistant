"""
=======================================================================
PIPELINE INGESTI DATA - SISTEM RAG ISLAMIC ASSISTANT
=======================================================================
Mata Kuliah : Natural Language Processing (NLP)
NPM         : 233510516
Semester    : 6 (Teknik Informatika UIR)

Dokumentasi:
Skrip ini diarsiteki secara mandiri untuk membaca korpus teks (TXT/PDF),
melakukan pemotongan (chunking) berbasis rekursif, dan memproyeksikannya 
ke ruang vektor menggunakan model HuggingFace lokal versi MULTIBAHASA.
=======================================================================
"""

import os
import sys
from glob import glob


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# --- Pustaka Ekstraksi & Pemrosesan Bahasa ---
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma

# Injeksi path agar modul konfigurasi kustom terbaca
lokasi_skrip_sekarang = os.path.dirname(os.path.abspath(__file__))
lokasi_akar = os.path.dirname(lokasi_skrip_sekarang)
sys.path.append(lokasi_akar)

from src.config import DIREKTORI_KUMPULAN_TEKS, DIREKTORI_BASISDATA_VEKTOR

def ekstraksi_sumber_pengetahuan_lokal():
    """Fase 1: Pengumpulan Korpus"""
    kumpulan_naskah_mentah = []
    print(f"[*] [233510516-LOG] Memulai pemindaian direktori: {DIREKTORI_KUMPULAN_TEKS}")
    
    koleksi_pdf = glob(os.path.join(DIREKTORI_KUMPULAN_TEKS, "*.pdf"))
    for berkas_pdf in koleksi_pdf:
        print(f"    -> Ditemukan PDF: {os.path.basename(berkas_pdf)}")
        alat_baca = PyPDFLoader(berkas_pdf)
        kumpulan_naskah_mentah.extend(alat_baca.load())
        
    koleksi_txt = glob(os.path.join(DIREKTORI_KUMPULAN_TEKS, "*.txt"))
    for berkas_txt in koleksi_txt:
        print(f"    -> Ditemukan TXT: {os.path.basename(berkas_txt)}")
        alat_baca_txt = TextLoader(berkas_txt, encoding='utf-8')
        kumpulan_naskah_mentah.extend(alat_baca_txt.load())
        
    print(f"[+] Total halaman teks yang terhimpun: {len(kumpulan_naskah_mentah)}\n")
    return kumpulan_naskah_mentah

def fragmentasi_teks_konteks(naskah_utuh):
    """Fase 2: Segmentasi Token"""
    print("[*] Melakukan segmentasi (chunking) pada naskah...")
    
    # Diubah menjadi 600 agar lebih fokus membaca poin per poin
    mesin_pemotong = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    potongan_informasi_terindeks = mesin_pemotong.split_documents(naskah_utuh)
    print(f"[+] Sukses memecah naskah menjadi {len(potongan_informasi_terindeks)} fragmen.\n")
    return potongan_informasi_terindeks

def konstruksi_basisdata_vektor_hf(fragmen_teks):
    """Fase 3: Pemetaan Vektor Geometris (Embedding)"""
    print("[*] Memulai komputasi vektorisasi (Hugging Face MULTIBAHASA)...")
    
    try:
        # PERUBAHAN KRUSIAL: Menggunakan model Multibahasa agar paham Bahasa Indonesia!
        model_representasi_kata = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        
        penyimpanan_vektor = Chroma.from_documents(
            documents=fragmen_teks,
            embedding=model_representasi_kata,
            persist_directory=DIREKTORI_BASISDATA_VEKTOR
        )
        
        print(f"[+] Basis data vektor berhasil dimatangkan pada: {DIREKTORI_BASISDATA_VEKTOR}")
        return penyimpanan_vektor
        
    except Exception as e:
        print(f"\n[!!!] FATAL ERROR: Gagal membuat database vektor! Pesan sistem: {e}")
        sys.exit(1)

def eksekusi_pipeline_utama():
    """Fungsi pembungkus (Wrapper) eksekusi"""
    print("="*65)
    print("⚙️ MENGAKTIFKAN MESIN INGESTI DATA RAG (VERSI LOKAL MULTIBAHASA)")
    print("="*65)
    
    if not os.path.exists(DIREKTORI_KUMPULAN_TEKS):
        print(f"[!] GAGAL: Direktori korpus {DIREKTORI_KUMPULAN_TEKS} tidak terdeteksi!")
        sys.exit(1)
        
    naskah_awal = ekstraksi_sumber_pengetahuan_lokal()
    
    if len(naskah_awal) == 0:
        print("[!] KORPUS KOSONG: Harap masukkan file referensi (.txt) ke direktori data.")
        sys.exit(0)
        
    fragmen_siap_olah = fragmentasi_teks_konteks(naskah_awal)
    konstruksi_basisdata_vektor_hf(fragmen_siap_olah)
    
    print("="*65)
    print("✅ PROSES INGESTI SELESAI DENGAN SUKSES!")
    print("Sistem NLP kini memiliki basis pengetahuan lokal Bahasa Indonesia.")
    print("="*65)

if __name__ == "__main__":
    eksekusi_pipeline_utama()