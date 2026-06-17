"""
Modul Data Ingestion - AI Islamic Assistant (UAS NLP)
Membaca dokumen dari folder data/, memecahnya menjadi potongan kecil (chunks),
dan menyimpannya ke dalam Vector Database (Chroma) menggunakan Hugging Face.
"""

import os
import sys
from glob import glob

# --- Library LangChain ---
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings # Pengganti Ollama
from langchain_community.vectorstores import Chroma

# Menambahkan path root ke sistem agar bisa melakukan import config dengan aman
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import DATA_DIR, VECTOR_STORE_DIR

def load_all_documents():
    """
    Tahap 1: LOAD
    Membaca semua file berformat .pdf dan .txt yang ada di dalam folder data/
    """
    documents = []
    print(f"📂 Mencari dokumen di: {DATA_DIR}...")
    
    # Mencari file PDF
    for pdf_path in glob(os.path.join(DATA_DIR, "*.pdf")):
        print(f"   -> Memuat PDF: {os.path.basename(pdf_path)}")
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
        
    # Mencari file TXT
    for txt_path in glob(os.path.join(DATA_DIR, "*.txt")):
        print(f"   -> Memuat TXT: {os.path.basename(txt_path)}")
        loader = TextLoader(txt_path, encoding='utf-8')
        documents.extend(loader.load())
        
    print(f"✅ Total {len(documents)} halaman/dokumen berhasil dimuat.\n")
    return documents

def split_documents(documents):
    """
    Tahap 2: SPLIT
    Memecah dokumen besar menjadi potongan-potongan teks kecil (chunks)
    agar LLM tidak kelebihan muatan (overload konteks) saat membaca.
    """
    print("✂️ Memecah dokumen menjadi chunks...")
    
    # Pengaturan ukuran potongan: 1000 karakter per chunk, dengan overlap 200 karakter
    # Overlap berguna agar kalimat yang terpotong di tengah tidak kehilangan konteksnya
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Dokumen berhasil dipecah menjadi {len(chunks)} chunks.\n")
    return chunks

def build_vector_store(chunks):
    """
    Tahap 3: EMBEDDING & STORE
    Mengubah teks menjadi vektor angka menggunakan Hugging Face
    dan menyimpannya secara permanen di direktori lokal dengan ChromaDB.
    """
    print("🧠 Memulai proses Embedding menggunakan Hugging Face...")
    
    # Menggunakan model embedding lokal dari HuggingFace (Tanpa aplikasi Ollama)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Membuat atau memperbarui Vector Store Chroma
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_DIR
    )
    
    print(f"✅ Vector database berhasil dibuat dan disimpan di: {VECTOR_STORE_DIR}")
    return vector_store

if __name__ == "__main__":
    print("="*50)
    print("🚀 MEMULAI DATA INGESTION (RAG PIPELINE) TANPA OLLAMA")
    print("="*50)
    
    # 1. Pastikan folder data ada
    if not os.path.exists(DATA_DIR):
        print(f"❌ Error: Folder {DATA_DIR} tidak ditemukan!")
        sys.exit(1)
        
    # 2. Jalankan Pipa RAG
    docs = load_all_documents()
    
    if len(docs) == 0:
        print("⚠️ Tidak ada dokumen PDF atau TXT yang ditemukan di folder data/.")
        print("💡 Silakan masukkan file referensi (misal: fiqh_shalat.pdf) ke folder data/ terlebih dahulu.")
        sys.exit(0)
        
    chunks = split_documents(docs)
    build_vector_store(chunks)
    
    print("="*50)
    print("🎉 DATA INGESTION SELESAI!")
    print("Sekarang asisten AI kamu sudah memiliki 'otak' dan siap menjawab pertanyaan.")
    print("="*50)