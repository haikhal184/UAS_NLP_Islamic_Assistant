Markdown
# 🕌 AI Islamic Assistant

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-F9AB00?style=flat&logo=huggingface&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=flat)

**AI Islamic Assistant** adalah sistem tanya jawab cerdas berbasis *Retrieval-Augmented Generation* (RAG) dan *Agentic Workflow*. Aplikasi ini dirancang untuk menjawab pertanyaan seputar hukum (Fiqih), sejarah Islam, dan pengetahuan agama lainnya secara akurat dengan merujuk langsung pada dokumen referensi lokal, guna menghindari halusinasi kecerdasan buatan.

Proyek ini dikembangkan sebagai pemenuhan tugas **Ujian Akhir Semester (UAS) Natural Language Processing (NLP)** di Universitas Islam Riau (UIR).

---

## ✨ Fitur Utama

* 🧠 **RAG Pipeline:** Mengekstraksi konteks yang relevan dari dokumen lokal (PDF/TXT) sebelum menghasilkan jawaban.
* ⚡ **Agentic Workflow:** Dibangun menggunakan LangGraph untuk mengelola *state* percakapan dan *routing* logika secara dinamis.
* 🚀 **Cloud LLM Integration:** Menggunakan model `Llama-3.1-8b-instant` via Groq API untuk inferensi secepat kilat.
* 🔍 **Local Embeddings:** Menjalankan model `all-MiniLM-L6-v2` dari Hugging Face sepenuhnya di mesin lokal tanpa biaya API tambahan.
* 🎨 **Premium UI/UX:** Antarmuka responsif dan modern bergaya SaaS menggunakan Streamlit, mengusung tema *Emerald Green*.
* 📈 **Observability:** Terintegrasi penuh dengan LangSmith untuk pelacakan (*tracing*) metrik performa dan *debugging* AI di *backend*.

## 📸 Tampilan Aplikasi

Berikut adalah dokumentasi visual dari AI Islamic Assistant saat dijalankan di mesin lokal:

### 1. Antarmuka Utama (Chat Assistant)
*Tampilan utama aplikasi dengan tema Emerald Green yang bersih dan fokus pada percakapan.*
![Main Chat Interface](assets/ss_main_chat.png)

### 2. Bukti Fitur RAG (Retrieval-Augmented Generation)
*AI menarik potongan teks asli dari dokumen PDF lokal untuk menjawab pertanyaan spesifik, menjamin akurasi jawaban.*
![RAG Feature](assets/ss_rag_reference.png)

### 3. Tracing Backend via LangSmith
*Pelacakan (tracing) alur sistem menggunakan LangSmith untuk memastikan setiap node pada LangGraph berjalan sesuai logika.*
![LangSmith Dashboard](assets/ss_langsmith.png)

---

## 🛠️ Arsitektur & Tech Stack

* **Bahasa Utama:** Python
* **Frontend:** Streamlit
* **AI Orchestration:** LangChain & LangGraph
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`sentence-transformers`)
* **LLM Provider:** Groq

---

## 📂 Struktur Direktori

```text
ai-islamic-assistant/
├── assets/                    # Folder gambar dokumentasi untuk README
│   ├── ss_langsmith.png
│   ├── ss_main_chat.png
│   └── ss_rag_reference.png
├── data/                      # Folder sumber pengetahuan lokal
│   └── ensiklopedia_islam_mini.txt
├── src/                       # Folder modul inti (Backend)
│   ├── __init__.py
│   ├── config.py              # Konfigurasi variabel dan path direktori
│   ├── data_ingestion.py      # Skrip pemrosesan teks ke dalam Vector DB
│   ├── retriever.py           # Logika pencarian dokumen untuk RAG
│   └── workflow.py            # Konfigurasi Node dan Edge pada LangGraph
├── vector_store/              # Folder penyimpanan database lokal (ChromaDB)
├── .env                       # File rahasia kredensial API Keys
├── .gitignore                 # Daftar file/folder yang diabaikan oleh Git
├── app.py                     # Skrip antarmuka UI utama (Streamlit)
├── cli.py                     # Skrip antarmuka Command Line (Terminal)
├── README.md                  # Dokumentasi proyek
└── requirements.txt           # Daftar pustaka dependencies proyek

## ⚙️ Cara Instalasi & Menjalankan Program (Di Komputer Baru)

Karena alasan keamanan dan efisiensi penyimpanan, file kredensial (`.env`) dan *database* lokal (`vector_store/`) **tidak ikut diunggah** ke GitHub. Oleh karena itu, jika Anda mengunduh repositori ini untuk dijalankan di PC lain, ikuti langkah-langkah wajib berikut dari awal.

### 🖥️ Persiapan: Membuka Terminal
Semua perintah kode di bawah ini harus dijalankan melalui **Terminal** (Command Prompt / PowerShell / Terminal Mac/Linux). 
* Jika Anda menggunakan **Visual Studio Code (VS Code)**, buka terminal dengan mengklik menu **Terminal > New Terminal** di bar atas, atau gunakan *shortcut* `Ctrl` + `~` (Tilde).

---

### 1. Unduh Kode Proyek (Download)
Ketik perintah berikut di terminal Anda untuk meng-*clone* repositori:
```bash
git clone [https://github.com/USERNAME_GITHUB_KAMU/ai-islamic-assistant.git](https://github.com/USERNAME_GITHUB_KAMU/ai-islamic-assistant.git)
cd ai-islamic-assistant
(Alternatif: Klik tombol "<> Code" di GitHub, pilih Download ZIP, ekstrak filenya, lalu buka terminal dan arahkan cd ke dalam folder hasil ekstraksi tersebut).

2. Buat & Aktifkan Virtual Environment (Sangat Disarankan)
Untuk menghindari bentrok antar-pustaka Python di PC Anda, ketik perintah ini di terminal:

Bash
python -m venv env

# Untuk mengaktifkan di Windows:
env\Scripts\activate

# Untuk mengaktifkan di Mac/Linux:
source env/bin/activate
(Pastikan muncul tulisan (env) di awal baris terminal Anda yang menandakan lingkungan virtual sudah aktif).

3. Instalasi Dependencies (Pustaka Python)
Selagi masih di dalam terminal, instal semua pustaka yang dibutuhkan proyek ini:

Bash
pip install -r requirements.txt
4. Setup File Kredensial (.env)
Anda wajib membuat file baru bernama .env di folder utama (sejajar dengan app.py). Buka file tersebut dengan text editor dan masukkan API Keys Anda:

Code snippet

GROQ_API_KEY="masukkan_groq_api_key_anda_di_sini"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="masukkan_langchain_api_key_anda_di_sini"
LANGCHAIN_PROJECT="UAS_NLP_Islamic_Assistant"

5. Membangun Ulang Vector Database (Data Ingestion)
Karena database sebelumnya tidak ikut diunduh, Anda harus membuat database baru di PC ini melalui terminal:

Pastikan sudah ada file referensi (contoh: ensiklopedia_islam_mini.txt) di dalam folder data/.

Jalankan skrip pembacaan data di terminal:

Bash
   python src/data_ingestion.py
Tunggu hingga terminal menampilkan pesan sukses. Proses ini akan mengunduh model bahasa (Hugging Face) dan membentuk folder vector_store/ secara otomatis.

6. Jalankan Aplikasi Web
Setelah semua persiapan di atas selesai, jalankan antarmuka aplikasi melalui terminal dengan perintah:

Bash
python -m streamlit run app.py
Aplikasi secara otomatis akan terbuka di browser Anda melalui tautan lokal (umumnya http://localhost:8501).

🎓 Identitas Proyek
Aplikasi ini dikembangkan untuk keperluan akademis:

Mata Kuliah: Natural Language Processing (NLP)

Program Studi: Teknik Informatika

Universitas: Universitas Islam Riau (UIR)

Semester: 6

NPM: 233510516