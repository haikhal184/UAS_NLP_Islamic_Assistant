"""
Modul Retriever & Generator (RAG) - AI Islamic Assistant
Menangani pencarian dokumen di Vector DB (Tanpa Ollama).
"""

import os
import sys

# --- Library python-dotenv (Wajib diaktifkan di awal) ---
from dotenv import load_dotenv
load_dotenv()

# --- Library LangChain ---
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings # Pengganti Ollama
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Menambahkan path root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import VECTOR_STORE_DIR

def get_vector_store():
    """
    Menghubungkan sistem dengan ChromaDB yang sudah dibuat oleh data_ingestion.py.
    """
    if not os.path.exists(VECTOR_STORE_DIR):
        raise FileNotFoundError(f"⚠️ Vector store tidak ditemukan. Jalankan data_ingestion.py terlebih dahulu!")

    # Menggunakan model embedding ringan dari HuggingFace (Tanpa aplikasi Ollama)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load database lokal
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embeddings
    )
    return vector_store

def get_llm():
    """
    Menginisialisasi model bahasa (LLM) menggunakan Groq (Cloud API).
    Sangat ringan untuk RAM dan memberikan respons secepat kilat.
    """
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        # Menggunakan model Llama 3.1 terbaru yang didukung Groq
        model_name="llama-3.1-8b-instant", 
        temperature=0.1 
    )

def retrieve_documents(query, k=3):
    """
    Mencari `k` dokumen (chunks) yang paling relevan dengan pertanyaan pengguna.
    """
    print(f"🔍 Mencari referensi untuk: '{query}'...")
    vector_store = get_vector_store()
    
    # Menggunakan metode pencarian standar (similarity search)
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    
    return docs

def format_docs(docs):
    """
    Menggabungkan isi dari beberapa dokumen menjadi satu teks panjang 
    agar bisa dimasukkan ke dalam prompt.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def generate_rag_answer(query):
    """
    Fungsi RAG Utama: 
    1. Tarik dokumen relevan.
    2. Masukkan ke Prompt.
    3. Minta LLM menjawab.
    """
    # 1. Proses Retrieval
    docs = retrieve_documents(query)
    context = format_docs(docs)
    
    # 2. Inisialisasi LLM
    llm = get_llm()
    
    # 3. Setup Prompt (SANGAT PENTING UNTUK ASISTEN ISLAMI)
    prompt_template = """
    Anda adalah 'AI Islamic Assistant' yang bertugas menjawab pertanyaan seputar Islam.
    Tugas Anda adalah menjawab pertanyaan HANYA berdasarkan 'Konteks Referensi' di bawah ini.
    
    ATURAN KETAT:
    1. Jawablah dengan sopan, akurat, dan terstruktur.
    2. Jika jawaban tidak ada di dalam Konteks Referensi, JANGAN mengarang jawaban.
    3. Jika tidak tahu, katakan: "Maaf, saya tidak menemukan informasi tersebut dalam referensi saya. Wallahu A'lam."
    4. Dilarang keras mengarang (halusinasi) ayat, hadis, atau hukum fikih.
    5. PASTIKAN Anda mengutip/menuliskan kembali "Sumber Referensi" di bagian paling akhir jawaban Anda.

    Konteks Referensi:
    {context}

    Pertanyaan:
    {question}

    Jawaban:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    
    # 4. Chain (Membangun Rantai dengan LCEL - LangChain Expression Language)
    chain = prompt | llm | StrOutputParser()
    
    # 5. Eksekusi
    print("🤖 Menghasilkan jawaban menggunakan LLM...")
    answer = chain.invoke({
        "context": context,
        "question": query
    })
    
    return answer, docs

# ==========================================
# TESTING LOKAL (Opsional)
# ==========================================
if __name__ == "__main__":
    # Script ini hanya berjalan jika file ini dieksekusi langsung
    test_question = "Apa itu Zakat Fitrah?"
    
    try:
        jawaban, referensi = generate_rag_answer(test_question)
        print("\n" + "="*40)
        print("💡 JAWABAN AI:")
        print("="*40)
        print(jawaban)
        print("\n" + "="*40)
        print(f"📚 JUMLAH REFERENSI DIGUNAKAN: {len(referensi)} chunks")
        print("="*40)
    except Exception as e:
        print(f"Error: {e}")