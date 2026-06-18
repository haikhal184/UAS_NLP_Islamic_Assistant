"""
=======================================================================
PENGATURAN LINGKUNGAN SISTEM (ENVIRONMENT CONFIGURATION)
=======================================================================
Mata Kuliah : Natural Language Processing (NLP)
Tugas       : UAS AI Islamic Assistant
NPM         : 233510516
Institusi   : Teknik Informatika UIR
Semester    : 6

Catatan:
Skrip ini menangani routing path absolut dan injeksi kredensial ke 
dalam environment OS secara dinamis. Ditulis spesifik untuk arsitektur 
lokal (Ollama) dan tracing LangGraph.
=======================================================================
"""

import os
from dotenv import load_dotenv

# Ekstraksi variabel rahasia dari sistem lokal
load_dotenv()

# ==========================================
# 1. PARAMETER OBSERVABILITAS (LANGSMITH)
# ==========================================
PELACAKAN_AKTIF = os.getenv("LANGCHAIN_TRACING_V2", "true")
TITIK_AKHIR_LANGSMITH = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
KUNCI_API_PELACAK = os.getenv("LANGCHAIN_API_KEY", "")
NAMA_PROYEK_UAS = os.getenv("LANGCHAIN_PROJECT", "UAS_NLP_Islamic_Assistant")

# ==========================================
# 2. PARAMETER MESIN INFERENSI (LLM & VEKTOR)
# ==========================================
# Jika menggunakan provider eksternal
KUNCI_OPENAI_CADANGAN = os.getenv("OPENAI_API_KEY", "")

# Pengaturan untuk eksekusi mesin lokal tanpa biaya API
URL_DASAR_OLLAMA_LOKAL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_BAHASA_UTAMA = os.getenv("OLLAMA_LLM_MODEL", "llama3")       
MODEL_PEMECAH_KATA = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text") 

# ==========================================
# 3. PEMETAAN LOKASI DIREKTORI
# ==========================================
# Kalkulasi path absolut agar terhindar dari error relative import
LOKASI_AKAR_PROYEK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIREKTORI_KUMPULAN_TEKS = os.path.join(LOKASI_AKAR_PROYEK, "data")
DIREKTORI_BASISDATA_VEKTOR = os.path.join(LOKASI_AKAR_PROYEK, "vector_store")

# ==========================================
# 4. RUTINITAS VALIDASI STARTUP
# ==========================================
def persiapkan_lingkungan_eksekusi_233510516():
    """
    Fungsi pelindung: Memastikan seluruh folder dan API Key sudah 
    di-inject ke memori OS sebelum LangGraph mulai membangun node-nya.
    """
    print("🔄 [SISTEM] Memuat konfigurasi lingkungan pengembangan...")
    
    # Injeksi paksa ke dalam environment agar terdeteksi framework RAG
    os.environ["LANGCHAIN_TRACING_V2"] = PELACAKAN_AKTIF
    os.environ["LANGCHAIN_ENDPOINT"] = TITIK_AKHIR_LANGSMITH
    os.environ["LANGCHAIN_PROJECT"] = NAMA_PROYEK_UAS
    
    if KUNCI_API_PELACAK:
        os.environ["LANGCHAIN_API_KEY"] = KUNCI_API_PELACAK
        print(f"✅ [LANGSMITH] Tracing terhubung ke proyek: {NAMA_PROYEK_UAS}")
    else:
        print("⚠️ [PERINGATAN] Kredensial LANGCHAIN_API_KEY tidak ditemukan!")
        print("   Pelacakan node LangGraph mungkin tidak akan terekam.")

    # Eksekusi pembuatan folder database jika belum ada di mesin ini
    os.makedirs(DIREKTORI_KUMPULAN_TEKS, exist_ok=True)
    os.makedirs(DIREKTORI_BASISDATA_VEKTOR, exist_ok=True)
    print("📁 [DIREKTORI] Struktur penyimpanan lokal telah tervalidasi.")

# Pemicu otomatis (Auto-trigger)
persiapkan_lingkungan_eksekusi_233510516()