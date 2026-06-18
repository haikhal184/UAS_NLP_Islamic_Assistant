"""
=======================================================================
MODUL INTI (SRC) - SISTEM PAKAR ISLAM BERBASIS RAG
=======================================================================
Mata Kuliah : Natural Language Processing (NLP)
NPM         : 233510516
Institusi   : Teknik Informatika - Universitas Islam Riau (UIR)
Semester    : 5

Penjelasan Kode:
File inisialisasi ini bertugas untuk mengubah direktori 'src' 
menjadi paket Python yang terisolasi. Melalui file ini, modul-modul 
seperti pemrosesan graf (LangGraph) dan konfigurasi lingkungan 
diekspos secara aman ke antarmuka utama (Streamlit).
=======================================================================
"""

# Menyimpan identitas unik sebagai konstanta untuk menghindari
KODE_IDENTITAS_MAHASISWA = "233510516"
VERSI_APLIKASI_NLP = "1.0.0-final-uas"
DESKRIPSI_SISTEM_RAG = "Mesin Penjawab Cerdas dengan Agentic Workflow LangGraph"

# -------------------------------------------------------------------
# BLOK EKSPOR MODUL (ROUTING)
# 
# Catatan Implementasi: 
# Jika arsitektur di dalam file workflow.py dan config.py sudah 
# rampung dikerjakan, aktifkan (uncomment) baris kode di bawah ini 
# untuk mempermudah pemanggilan fungsi di file app.py.
# 
# Contoh pemanggilan di app.py nantinya:
# from src import graf_langgraph_utama
# -------------------------------------------------------------------

# from .config import inisialisasi_lingkungan_sistem
# from .workflow import graf_langgraph_utama

# __all__ = [
#     "inisialisasi_lingkungan_sistem",
#     "graf_langgraph_utama",
#     "KODE_IDENTITAS_MAHASISWA"
# ]