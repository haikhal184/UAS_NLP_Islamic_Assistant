"""
=======================================================================
ANTARMUKA PENGGUNA (FRONTEND STREAMLIT)
=======================================================================
NPM         : 233510516
Tugas       : UAS Natural Language Processing (NLP)
Deskripsi   : Skrip utama untuk merender antarmuka visual (UI/UX) dan 
              menghubungkan input pengguna dengan mesin LangGraph.
=======================================================================
"""

import os
import time
import warnings
from dotenv import load_dotenv
import streamlit as st

# Menginisialisasi variabel environment secara aman
load_dotenv()
warnings.filterwarnings("ignore")

# Memanggil mesin arsitektur LangGraph dari direktori backend
try:
    from src.workflow import graf_langgraph_utama
except ImportError:
    graf_langgraph_utama = None
    st.error("⚠️ [SISTEM FATAL] Modul graf_langgraph_utama gagal dimuat dari direktori src.")

def konfigurasi_halaman_ui_233510516():
    """Membungkus pengaturan meta-halaman agar terisolasi dari pola global Streamlit."""
    st.set_page_config(
        page_title="AI Islamic Assistant",
        page_icon="🕌",
        layout="centered",
        initial_sidebar_state="auto"
    )

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp { background-color: #F0FDF4; }

        [data-testid="stSidebar"] {
            background-color: #064E3B !important;
        }
        [data-testid="stSidebar"] * { color: #ECFDF5 !important; }
        [data-testid="stSidebar"] hr { border-color: rgba(16, 185, 129, 0.3); margin: 1rem 0; }

        .wadah-judul-aplikasi { text-align: center; padding: 2rem 0 1rem 0; }
        .wadah-judul-aplikasi h1 { font-weight: 700; color: #064E3B; font-size: 2.2rem; margin-bottom: 0.5rem; }
        .wadah-judul-aplikasi p { color: #059669; font-size: 1.1rem; }

        .stChatMessage {
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(16, 185, 129, 0.05); border: 1px solid #A7F3D0;
            background-color: #FFFFFF;
        }

        .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) { border-left: 4px solid #34D399; }
        .stChatMessage[data-testid="stChatMessage"]:nth-child(even) { background-color: #ECFDF5; border-left: 4px solid #059669; }

        .streamlit-expanderHeader { font-size: 0.9rem; color: #064E3B; background-color: #D1FAE5; border-radius: 8px; }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def render_panel_samping():
    """Merender kotak identitas NPM di sebelah kiri."""
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="font-size: 4rem; margin: 0; color: #FCD34D !important;">☪️</h1>
                <h2 style="font-size: 1.5rem; font-weight: 700; margin-top: 0.5rem; color: #FFFFFF !important;">AI Islamic Assistant</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
            <div style="background-color: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(52, 211, 153, 0.2);">
                <p style="font-size: 0.8rem; color: #A7F3D0 !important; margin: 0;">IDENTITAS PROYEK (UAS NLP)</p>
                <p style="font-weight: 600; color: #FFFFFF !important; margin: 5px 0 0 0;">NPM: 233510516</p>
                <p style="font-size: 0.8rem; margin: 0; color: #34D399 !important;">Teknik Informatika - Smt 5</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# INISIALISASI APLIKASI
# ==========================================
konfigurasi_halaman_ui_233510516()
render_panel_samping()

# Aset Visual
avatar_user_biasa = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
avatar_mesin_pakar = "https://cdn-icons-png.flaticon.com/512/6134/6134346.png"

# Manajemen Memori UI (Session State Custom)
if "memori_sesi_233510516" not in st.session_state:
    st.session_state.memori_sesi_233510516 = [
        {
            "aktor": "bot", 
            "isi_pesan": "Assalamu'alaikum! Saya adalah asisten cerdas berbasis agen RAG. Ada pertanyaan tentang hukum fiqih, zakat, atau sejarah Islam yang bisa saya bantu hari ini?", 
            "teks_rujukan_rag": ""
        }
    ]

st.markdown("""
<div class="wadah-judul-aplikasi">
    <h1>💬 Chat Assistant</h1>
    <p>Sistem Tanya Jawab Islam Berbasis Agen LangGraph</p>
</div>
""", unsafe_allow_html=True)

# Melakukan perulangan untuk merender riwayat percakapan sebelumnya
for rekaman_log in st.session_state.memori_sesi_233510516:
    ikon_terpilih = avatar_user_biasa if rekaman_log["aktor"] == "manusia" else avatar_mesin_pakar
    with st.chat_message(rekaman_log["aktor"], avatar=ikon_terpilih):
        st.markdown(rekaman_log["isi_pesan"])
        
        # Mengecek apakah bot menyertakan bukti referensi (RAG)
        referensi = rekaman_log.get("teks_rujukan_rag", "")
        if referensi and len(referensi) > 10:
            with st.expander("📚 Lihat Referensi Dokumen Lokal"):
                st.info(referensi)

# Kotak Input Chat
kueri_diketik = st.chat_input("Ketikkan kueri atau pertanyaan Anda di sini...")

if kueri_diketik:
    # 1. Simpan dan tampilkan pesan pengguna
    st.session_state.memori_sesi_233510516.append({"aktor": "manusia", "isi_pesan": kueri_diketik, "teks_rujukan_rag": ""})
    with st.chat_message("manusia", avatar=avatar_user_biasa):
        st.markdown(kueri_diketik)

    # 2. Proses dan tampilkan balasan AI
    with st.chat_message("bot", avatar=avatar_mesin_pakar):
        tempat_teks_animasi = st.empty()
        konteks_referensi_didapat = ""
        
        with st.spinner("Mesin LangGraph sedang memproses kueri..."):
            try:
                # Mengirim data ke otak LangGraph dengan dictionary keys yang baru
                state_langgraph = graf_langgraph_utama.invoke({"kueri_input": kueri_diketik})
                
                # Menarik hasil komputasi dari state akhir
                jawaban_mentah_ai = state_langgraph["respons_final"]
                konteks_referensi_didapat = state_langgraph.get("teks_konteks_rag", "")
                
                # Menjalankan animasi efek pengetikan (Typewriter effect)
                kalimat_bertahap = ""
                for suku_kata in jawaban_mentah_ai.split(" "):
                    kalimat_bertahap += suku_kata + " "
                    time.sleep(0.02) 
                    tempat_teks_animasi.markdown(kalimat_bertahap + "▌")
                tempat_teks_animasi.markdown(kalimat_bertahap)
                
                # Merender komponen dokumen sumber jika ada teks yang disintesis
                if konteks_referensi_didapat and len(konteks_referensi_didapat) > 10:
                    with st.expander("📚 Lihat Referensi Dokumen Lokal"):
                        st.info(konteks_referensi_didapat)
                        
            except Exception as e:
                jawaban_mentah_ai = f"⚠️ [GANGGUAN SISTEM]: Eksekusi node graf gagal - {e}"
                tempat_teks_animasi.error(jawaban_mentah_ai)
                
    # 3. Simpan balasan AI ke memori browser
    st.session_state.memori_sesi_233510516.append({
        "aktor": "bot", 
        "isi_pesan": jawaban_mentah_ai, 
        "teks_rujukan_rag": konteks_referensi_didapat
    })