"""
=======================================================================
MODUL ORKESTRASI AGEN (LANGGRAPH WORKFLOW)
=======================================================================
Pengembang  : 233510516 (UAS Teknik Informatika)
Fokus       : Manajemen State, Routing Kognitif, & Conditional Edges

Dokumentasi:
Skrip ini merancang otak "Agentic" dari AI menggunakan ekosistem 
HuggingFace (Multilingual) untuk retrieval dan Groq untuk penalaran bahasa.
=======================================================================
"""

import os
import sys
from typing import TypedDict, List

# --- PENGAMAN WINDOWS ---
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# --- Pustaka Pengatur Alur Logika ---
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Memastikan modul internal terbaca dengan path absolut
lokasi_saat_ini = os.path.dirname(os.path.abspath(__file__))
lokasi_root = os.path.dirname(lokasi_saat_ini)
sys.path.append(lokasi_root)

# Mengimpor fungsi-fungsi dari retriever.py
from src.retriever import (
    inisiator_mesin_inferensi_groq, 
    pencari_konteks_relevan_233510516, 
    sintesis_teks_dokumen
)

# ==========================================
# 1. STRUKTUR MEMORI (KOGNITIF AGEN)
# ==========================================
class StrukturMemoriKognitif(TypedDict):
    kueri_input: str
    kategori_niat: str
    teks_konteks_rag: str
    sumber_literatur: List[str]
    respons_final: str

# ==========================================
# 2. DEFINISI NODE (FUNGSI PEKERJA)
# ==========================================
def node_analisis_niat_user(state: StrukturMemoriKognitif):
    print("[+] [NODE: KLASIFIKASI] Membedah niat pengguna...")
    pertanyaan_mentah = state["kueri_input"]
    mesin_penganalisa = inisiator_mesin_inferensi_groq()
    
    prompt_kategorisasi = PromptTemplate.from_template(
        "Lakukan klasifikasi semantik pada kueri ini ke dalam SATU dari 3 label:\n"
        "- 'salam' : Jika kueri murni sapaan (contoh: assalamualaikum, halo bro)\n"
        "- 'islam' : Jika kueri memuat terminologi agama, hukum, zakat, rukun shalat, sejarah nabi\n"
        "- 'blokir': Jika kueri membahas di luar agama (contoh: pemilu, resep kue, koding)\n\n"
        "Kueri: {kueri_input}\n"
        "Label Klasifikasi (1 kata):"
    )
    
    rantai_analisis = prompt_kategorisasi | mesin_penganalisa | StrOutputParser()
    hasil_label = rantai_analisis.invoke({"kueri_input": pertanyaan_mentah}).strip().lower()
    
    # Filter sanitasi
    if "salam" in hasil_label:
        kategori_final = "salam"
    elif "blokir" in hasil_label or "luar" in hasil_label:
        kategori_final = "blokir"
    else:
        kategori_final = "islam"
        
    print(f"    => Kategori Terdeteksi: [{kategori_final.upper()}]")
    return {"kategori_niat": kategori_final}

def node_pencarian_dalil(state: StrukturMemoriKognitif):
    print("[+] [NODE: RETRIEVAL] Menggali literatur dari Database Ruang Vektor...")
    pertanyaan = state["kueri_input"]
    
    dokumen_ditemukan = pencari_konteks_relevan_233510516(pertanyaan)
    konteks_gabungan = sintesis_teks_dokumen(dokumen_ditemukan)
    
    # Ekstraksi jejak metadata
    daftar_dalil = [dalil.metadata.get("source", "Entitas Tak Dikenal") for dalil in dokumen_ditemukan]
    
    # Print diagnostik agar terlihat di terminal apakah data berhasil ditarik
    print("\n--- [DIAGNOSTIK TEKS YANG DITEMUKAN] ---")
    if konteks_gabungan.strip():
        print(konteks_gabungan[:250] + "...\n(Teks terpotong untuk log)")
    else:
        print("[!] PERINGATAN: Tidak ada teks yang cocok ditemukan di database!")
    print("----------------------------------------\n")
    
    return {"teks_konteks_rag": konteks_gabungan, "sumber_literatur": daftar_dalil}

def node_sintesis_jawaban_islami(state: StrukturMemoriKognitif):
    print("[+] [NODE: GENERATOR] Memformulasi diksi Islami menggunakan Groq...")
    mesin_penjawab = inisiator_mesin_inferensi_groq()
    
    templat_sintesis = """
    Peran Anda: Asisten Edukasi Islam Berbasis AI.
    Kewajiban: Menyusun respons HANYA mengacu pada 'Literatur Valid' di bawah.
    
    SOP KETAT:
    1. Berbahasa Indonesia ejaan yang disempurnakan (EYD).
    2. Dilarang keras mengarang ayat, langkah, atau fatwa fiktif. 
    3. Jika informasi tidak ada di Literatur Valid, jawab: "Mohon maaf, referensi saya belum mencakup hal tersebut."
    4. Selalu tulis ulang sumber/referensi di akhir jawaban.

    Literatur Valid:
    {teks_konteks_rag}

    Kueri Pengguna:
    {kueri_input}

    Draf Balasan:
    """
    kerangka = PromptTemplate.from_template(templat_sintesis)
    rantai_final = kerangka | mesin_penjawab | StrOutputParser()
    
    jawaban_ai = rantai_final.invoke({
        "teks_konteks_rag": state["teks_konteks_rag"], 
        "kueri_input": state["kueri_input"]
    })
    return {"respons_final": jawaban_ai}

def node_balasan_salam(state: StrukturMemoriKognitif):
    print("[+] [NODE: SAPAAN] Mengirim salam balasan...")
    return {"respons_final": "Waalaikumsalam warahmatullah. Ada yang bisa saya bantu terkait hukum fiqih atau sejarah Islam hari ini?"}

def node_blokir_topik_luar(state: StrukturMemoriKognitif):
    print("[-] [NODE: FILTER] Menolak kueri non-Islami...")
    return {"respons_final": "Mohon maaf, sistem AI ini dikhususkan untuk menjawab pertanyaan seputar ilmu pengetahuan Islam."}

# ==========================================
# 3. PENENTU ARAH (ROUTING CONDITIONAL EDGE)
# ==========================================
def penentu_jalur_kognitif(state: StrukturMemoriKognitif):
    return state["kategori_niat"]

# ==========================================
# 4. PERAKITAN GRAF (ARSITEKTUR INTI)
# ==========================================
mesin_state_graph_233510516 = StateGraph(StrukturMemoriKognitif)

# Registrasi Node Pekerja
mesin_state_graph_233510516.add_node("simpul_analis", node_analisis_niat_user)
mesin_state_graph_233510516.add_node("simpul_pencari", node_pencarian_dalil)
mesin_state_graph_233510516.add_node("simpul_penjawab", node_sintesis_jawaban_islami)
mesin_state_graph_233510516.add_node("simpul_salam", node_balasan_salam)
mesin_state_graph_233510516.add_node("simpul_penolak", node_blokir_topik_luar)

# Konfigurasi Titik Masuk (Entry Point)
mesin_state_graph_233510516.set_entry_point("simpul_analis")

# Penjadwalan Cabang (Conditional Edges)
mesin_state_graph_233510516.add_conditional_edges(
    "simpul_analis", 
    penentu_jalur_kognitif, 
    {
        "salam": "simpul_salam",
        "islam": "simpul_pencari",
        "blokir": "simpul_penolak"
    }
)

# Pemetaan Jalur Lurus
mesin_state_graph_233510516.add_edge("simpul_pencari", "simpul_penjawab")
mesin_state_graph_233510516.add_edge("simpul_penjawab", END)
mesin_state_graph_233510516.add_edge("simpul_salam", END)
mesin_state_graph_233510516.add_edge("simpul_penolak", END)

# Kompilasi menjadi aplikasi berjalan
graf_langgraph_utama = mesin_state_graph_233510516.compile()

# ==========================================
# SIMULASI TERMINAL LOKAL
# ==========================================
if __name__ == "__main__":
    print("="*60)
    print("🧪 DIAGNOSTIK: GRAF LANGGRAPH 233510516 (VERSI HF LOKAL)")
    print("="*60)
    
    tes_input = "Sebutkan rukun shalat menurut literatur yang ada." 
    print(f"INPUT : {tes_input}\n")
    
    status_akhir = graf_langgraph_utama.invoke({"kueri_input": tes_input})
    
    print("\n" + "="*60)
    print("💡 HASIL SINTESIS AKHIR:")
    print("="*60)
    print(status_akhir["respons_final"])