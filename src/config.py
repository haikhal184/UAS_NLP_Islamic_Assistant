"""
Konfigurasi Utama - AI Islamic Assistant
Mengatur Environment Variables, API Keys, dan Path direktori.
"""

import os
from dotenv import load_dotenv

# Memuat variabel environment dari file .env yang ada di root folder
load_dotenv()

# ==========================================
# 1. KONFIGURASI LANGSMITH (WAJIB UNTUK UAS)
# ==========================================
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "UAS_NLP_Islamic_Assistant")

# ==========================================
# 2. KONFIGURASI LLM & EMBEDDING
# ==========================================
# Jika menggunakan OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Jika menggunakan Local LLM via Ollama (Direkomendasikan agar gratis & private)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3")       # Model untuk chat
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text") # Model untuk embedding RAG

# ==========================================
# 3. KONFIGURASI DIREKTORI (PATH)
# ==========================================
# Mendapatkan path absolut ke folder root proyek
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(ROOT_DIR, "data")
VECTOR_STORE_DIR = os.path.join(ROOT_DIR, "vector_store")

# ==========================================
# 4. FUNGSI VALIDASI
# ==========================================
def init_environment():
    """
    Fungsi ini dipanggil saat aplikasi pertama kali dijalankan 
    untuk memastikan semua variabel environment yang krusial sudah siap.
    """
    print("🔄 Menginisialisasi Environment...")
    
    # Set explicit environment variables agar otomatis terdeteksi oleh modul LangChain
    os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
    os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
    
    if LANGCHAIN_API_KEY:
        os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
        print(f"✅ LangSmith Tracing AKTIF (Project: {LANGCHAIN_PROJECT})")
    else:
        print("⚠️ WARNING: LANGCHAIN_API_KEY belum diset di file .env!")
        print("   Tracing LangSmith tidak akan berfungsi.")

    # Memastikan direktori data dan vector store tersedia
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Eksekusi fungsi inisialisasi secara otomatis saat modul ini di-import
init_environment()