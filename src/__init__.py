"""
Package 'src' - Core Logic AI Islamic Assistant (UAS NLP)

File __init__.py ini menginisialisasi folder 'src' sebagai modul Python.
Di sini kita juga bisa mengatur fungsi apa saja yang diekspos agar 
import di file app.py utama menjadi lebih rapi dan singkat.
"""

__version__ = "1.0.0"
__description__ = "Agentic RAG Assistant menggunakan LangChain, LangGraph, dan LangSmith"

# -------------------------------------------------------------------
# CATATAN: 
# Kode di bawah ini di-comment (dimatikan) terlebih dahulu karena 
# file config.py dan workflow.py belum kita isi kodenya. 
# 
# Nanti, setelah fungsi di workflow.py selesai dibuat (misalnya 
# variabel graf/state bernama 'app_graph'), kamu bisa menghilangkan 
# tanda '#' agar bisa di-import langsung di app.py seperti ini:
# -> from src import app_graph
# -------------------------------------------------------------------

# from .config import init_environment
# from .workflow import app_graph

# __all__ = [
#     "init_environment",
#     "app_graph"
# ]