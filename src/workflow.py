"""
Modul Workflow (LangGraph) - AI Islamic Assistant
Mengatur alur kerja agen AI menggunakan State, Nodes, dan Conditional Edges.
"""

import os
import sys
from typing import Dict, TypedDict, List

# --- Library LangGraph & LangChain ---
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Menambahkan path root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.retriever import get_llm, retrieve_documents, format_docs

# ==========================================
# 1. DEFINISI STATE (Memori Agen)
# ==========================================
class AgentState(TypedDict):
    """
    State adalah struktur memori yang dibawa dan diubah 
    sepanjang perjalanan dari Node satu ke Node lainnya.
    """
    question: str
    intent: str
    context: str
    references: List[str]
    answer: str

# ==========================================
# 2. DEFINISI NODES (Fungsi Pekerja)
# ==========================================
def detect_intent(state: AgentState):
    """
    Node 1: Menganalisis niat pengguna.
    Output-nya akan menentukan jalur mana yang akan diambil sistem.
    """
    print("🧠 [Node: Router] Mendeteksi niat pengguna...")
    question = state["question"]
    llm = get_llm()
    
    prompt = PromptTemplate.from_template(
        "Tugas Anda adalah mengklasifikasikan pertanyaan berikut ke dalam HANYA SATU dari 3 kategori:\n"
        "1. 'salam' (Jika pengguna hanya menyapa, cth: assalamualaikum, halo, hai)\n"
        "2. 'islam' (Jika pengguna bertanya seputar ibadah, zakat, sejarah nabi, akidah, fiqh, dll)\n"
        "3. 'luar_topik' (Jika pengguna bertanya di luar agama Islam, cth: politik, presiden, matematika, cuaca)\n\n"
        "Pertanyaan: {question}\n"
        "Kategori (jawab dengan satu kata saja):"
    )
    
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question}).strip().lower()
    
    # Sanitasi output LLM agar pasti sesuai dengan kunci dictionary
    if "salam" in result:
        intent = "salam"
    elif "luar" in result or "topik" in result:
        intent = "luar_topik"
    else:
        intent = "islam"
        
    print(f"   -> Hasil deteksi: {intent.upper()}")
    return {"intent": intent}

def retrieve_node(state: AgentState):
    """
    Node 2: Menarik data dari Vector DB (Hanya jalan jika intent == 'islam')
    """
    print("📚 [Node: Retriever] Mencari dokumen di database...")
    question = state["question"]
    
    docs = retrieve_documents(question)
    context = format_docs(docs)
    
    # Menyimpan metadata/nama file sumber untuk referensi
    refs = [doc.metadata.get("source", "Dokumen tidak diketahui") for doc in docs]
    
    return {"context": context, "references": refs}

def generate_node(state: AgentState):
    """
    Node 3: Membuat jawaban berdasarkan dokumen (RAG).
    """
    print("🤖 [Node: Generator] Merangkai jawaban Islami...")
    question = state["question"]
    context = state["context"]
    llm = get_llm()
    
    prompt_template = """
    Anda adalah 'AI Islamic Assistant' yang bertugas menjawab pertanyaan seputar Islam.
    Tugas Anda adalah menjawab pertanyaan HANYA berdasarkan 'Konteks Referensi' di bawah ini.
    
    ATURAN KETAT:
    1. Jawablah dengan sopan, terstruktur, dan gunakan bahasa Indonesia yang baku.
    2. JANGAN pernah mengarang (halusinasi) hukum fikih atau sejarah di luar konteks yang diberikan.
    3. Jika konteks tidak cukup untuk menjawab, katakan: "Maaf, saya tidak menemukan informasi tersebut dalam referensi saya. Wallahu A'lam."
    4. PASTIKAN Anda mengutip/menuliskan kembali "Sumber Referensi" di bagian paling akhir jawaban Anda persis seperti yang tertera di teks.

    Konteks Referensi:
    {context}

    Pertanyaan:
    {question}

    Jawaban:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({"context": context, "question": question})
    return {"answer": answer}

def salam_node(state: AgentState):
    """Node 4: Jalur khusus untuk merespons salam tanpa perlu RAG."""
    print("👋 [Node: Salam] Membalas sapaan...")
    return {"answer": "Waalaikumsalam warahmatullah wabarakatuh. Ada pertanyaan seputar hukum Islam, zakat, atau sejarah yang bisa saya bantu hari ini?"}

def out_of_topic_node(state: AgentState):
    """Node 5: Jalur khusus untuk menolak pertanyaan di luar topik Islam."""
    print("🚫 [Node: Out of Topic] Menolak pertanyaan dengan sopan...")
    return {"answer": "Maaf, sebagai AI Islamic Assistant, saya hanya diprogram untuk menjawab pertanyaan seputar agama Islam berdasarkan referensi tepercaya. Mohon tanyakan topik yang relevan, ya."}

# ==========================================
# 3. ROUTING LOGIC (Pengarah Jalur)
# ==========================================
def route_intent(state: AgentState):
    """Fungsi ini membaca state['intent'] dan menentukan edge mana yang dilalui."""
    return state["intent"]

# ==========================================
# 4. MEMBANGUN GRAPH (Arsitektur Utama LangGraph)
# ==========================================
workflow = StateGraph(AgentState)

# Mendaftarkan semua Node
workflow.add_node("router", detect_intent)
workflow.add_node("retriever", retrieve_node)
workflow.add_node("generator", generate_node)
workflow.add_node("salam", salam_node)
workflow.add_node("oot", out_of_topic_node)

# Mengatur Titik Awal (Entry Point)
workflow.set_entry_point("router")

# Mengatur Jalur Bersyarat (Conditional Edges)
workflow.add_conditional_edges(
    "router",          # Dari node router
    route_intent,      # Fungsi penentu
    {
        "salam": "salam",           # Jika intent 'salam', pergi ke node 'salam'
        "islam": "retriever",       # Jika intent 'islam', pergi ke node 'retriever'
        "luar_topik": "oot"         # Jika intent 'luar_topik', pergi ke node 'oot'
    }
)

# Mengatur Jalur Lanjutan
workflow.add_edge("retriever", "generator")
workflow.add_edge("generator", END)  # Selesai
workflow.add_edge("salam", END)      # Selesai
workflow.add_edge("oot", END)        # Selesai

# Mengkompilasi graf menjadi aplikasi yang bisa dijalankan
app_graph = workflow.compile()

# ==========================================
# TESTING LOKAL
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print("🧪 UJI COBA WORKFLOW LANGGRAPH")
    print("="*50)
    
    test_question = "Sebutkan rukun shalat beserta referensinya." 
    
    print(f"USER: {test_question}\n")
    final_state = app_graph.invoke({"question": test_question})
    
    print("\n" + "="*50)
    print("💡 JAWABAN AKHIR AI:")
    print("="*50)
    print(final_state["answer"])