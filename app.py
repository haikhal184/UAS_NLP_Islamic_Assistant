import os
import time
import warnings
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
warnings.filterwarnings("ignore")

try:
    from src.workflow import app_graph
except ImportError:
    app_graph = None
    st.error("⚠️ Modul app_graph tidak ditemukan. Pastikan struktur folder src/workflow.py sudah benar.")

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

    .stApp {
        background-color: #F0FDF4;
    }

    [data-testid="stSidebar"] {
        background-color: #064E3B !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ECFDF5 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(16, 185, 129, 0.3);
        margin: 1rem 0;
    }

    .chat-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    
    .chat-header h1 {
        font-weight: 700;
        color: #064E3B;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    .chat-header p {
        color: #059669;
        font-size: 1.1rem;
    }

    .stChatMessage {
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.05);
        border: 1px solid #A7F3D0;
        background-color: #FFFFFF;
    }

    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        border-left: 4px solid #34D399;
    }
    
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #ECFDF5;
        border-left: 4px solid #059669;
    }

    .streamlit-expanderHeader {
        font-size: 0.9rem;
        color: #064E3B;
        background-color: #D1FAE5;
        border-radius: 8px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

icon_user = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
icon_ai = "https://cdn-icons-png.flaticon.com/512/6134/6134346.png"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalamu'alaikum! Saya adalah asisten cerdas yang siap membantu menjawab pertanyaan Anda seputar agama Islam berdasarkan referensi yang valid. Ada yang bisa saya bantu hari ini?", "sources": []}
    ]

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

st.markdown("""
<div class="chat-header">
    <h1>💬 Chat Assistant</h1>
    <p>Tanya Jawab Islam Berbasis LangGraph & RAG</p>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    ikon = icon_user if message["role"] == "user" else icon_ai
    with st.chat_message(message["role"], avatar=ikon):
        st.markdown(message["content"])
        if message.get("sources") and len(message["sources"]) > 0:
            with st.expander("📚 Lihat Referensi Dokumen"):
                for i, doc in enumerate(message["sources"]):
                    st.markdown(f"**Sumber {i+1}:**")
                    st.info(doc.page_content)

user_input = st.chat_input("Ketik pertanyaan Anda di sini...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input, "sources": []})
    with st.chat_message("user", avatar=icon_user):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=icon_ai):
        message_placeholder = st.empty()
        rag_docs = []
        
        with st.spinner("Mencari referensi..."):
            try:
                final_state = app_graph.invoke({"question": user_input})
                bot_response = final_state["answer"]
                
                if "documents" in final_state and final_state["documents"]:
                    rag_docs = final_state["documents"]
                
                full_response = ""
                for chunk in bot_response.split(" "):
                    full_response += chunk + " "
                    time.sleep(0.02) 
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                if len(rag_docs) > 0:
                    with st.expander("📚 Lihat Referensi Dokumen"):
                        for i, doc in enumerate(rag_docs):
                            st.markdown(f"**Sumber {i+1}:**")
                            st.info(doc.page_content)
                
            except Exception as e:
                bot_response = f"⚠️ Terjadi kesalahan sistem: {e}"
                message_placeholder.error(bot_response)
                
    st.session_state.messages.append({"role": "assistant", "content": bot_response, "sources": rag_docs})