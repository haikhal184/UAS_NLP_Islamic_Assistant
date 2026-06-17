"""
CLI Mode - AI Islamic Assistant
Menjalankan chatbot murni di dalam terminal tanpa UI web.
"""

import warnings
from dotenv import load_dotenv

# Wajib di awal untuk menyembunyikan warning dan load API Key
warnings.filterwarnings("ignore")
load_dotenv()

# Import otak LangGraph-nya
from src.workflow import app_graph

def main():
    print("="*50)
    print("🕌 AI ISLAMIC ASSISTANT (CLI MODE) 🕌")
    print("="*50)
    print("Ketik 'keluar', 'exit', atau 'quit' untuk menghentikan program.\n")

    while True:
        # 1. Mengambil input dari pengguna di terminal
        user_input = input("👤 Kamu: ")
        
        # 2. Cek apakah pengguna ingin keluar
        if user_input.lower() in ['keluar', 'exit', 'quit']:
            print("\n👋 Waalaikumsalam. Sampai jumpa!")
            break
            
        # 3. Mencegah input kosong
        if not user_input.strip():
            continue

        print("🤖 AI sedang berpikir...")
        
        try:
            # 4. Melempar pertanyaan ke LangGraph
            final_state = app_graph.invoke({"question": user_input})
            
            # 5. Mencetak jawaban
            print(f"\n💡 Jawaban: \n{final_state['answer']}")
            print("-" * 50 + "\n")
            
        except Exception as e:
            print(f"\n⚠️ Terjadi kesalahan: {e}")
            print("Pastikan database vektor sudah dibuat!\n")

if __name__ == "__main__":
    main()