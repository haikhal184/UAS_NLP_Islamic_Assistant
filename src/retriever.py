"""
=======================================================================
MODUL MESIN PENCARI & GENERATOR (RAG ENGINE)
=======================================================================
Identitas   : 233510516 (UAS NLP)
Fungsi      : Melakukan semantic search pada ruang vektor dan
              menginjeksi konteks ke dalam prompt LLM Groq.
=======================================================================
"""

import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

lokasi_skrip_saat_ini = os.path.dirname(os.path.abspath(__file__))
lokasi_induk = os.path.dirname(lokasi_skrip_saat_ini)
sys.path.append(lokasi_induk)

from src.config import DIREKTORI_BASISDATA_VEKTOR


def koneksi_basisdata_pengetahuan_lokal():
    """
    Membuka koneksi ke ChromaDB lokal.
    """

    if not os.path.exists(DIREKTORI_BASISDATA_VEKTOR):
        raise FileNotFoundError(
            f"[FATAL] Basis data tidak ditemukan di {DIREKTORI_BASISDATA_VEKTOR}. "
            f"Jalankan data_ingestion.py terlebih dahulu."
        )

    model_pengukur_semantic = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    return Chroma(
        persist_directory=DIREKTORI_BASISDATA_VEKTOR,
        embedding_function=model_pengukur_semantic
    )


def inisiator_mesin_inferensi_groq():
    """
    Membuat instance LLM Groq.
    """

    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.0
    )


def pencari_konteks_relevan_233510516(
    kueri_pengguna,
    batas_output=3
):
    """
    Mengambil dokumen paling relevan dari vector store.
    """

    print(f"[*] Menelusuri ruang vektor untuk: '{kueri_pengguna}'")

    db_aktif = koneksi_basisdata_pengetahuan_lokal()

    mesin_retriever = db_aktif.as_retriever(
        search_kwargs={"k": batas_output}
    )

    fragmen_terjaring = mesin_retriever.invoke(kueri_pengguna)

    print("\n===== HASIL RETRIEVAL =====")

    for i, doc in enumerate(fragmen_terjaring):
        print(f"\n[Dokumen {i+1}]")
        print(doc.page_content[:500])

    print("===========================\n")

    return fragmen_terjaring


def sintesis_teks_dokumen(daftar_fragmen):
    """
    Menggabungkan seluruh dokumen menjadi satu konteks.
    """

    if not daftar_fragmen:
        return ""

    return "\n\n".join(
        fragmen.page_content
        for fragmen in daftar_fragmen
    )


def produksi_jawaban_berbasis_fakta(input_tanya):
    """
    Pipeline utama RAG.
    """

    hasil_dokumen = pencari_konteks_relevan_233510516(
        input_tanya
    )

    teks_sintesis = sintesis_teks_dokumen(
        hasil_dokumen
    )

    if not teks_sintesis.strip():
        return (
            "Mohon maaf, data referensi saya tidak memuat informasi tersebut. Wallahu A'lam.",
            []
        )

    mesin_llm = inisiator_mesin_inferensi_groq()

    instruksi_sistem = """
Anda adalah AI Islamic Assistant.

ATURAN WAJIB:

1. Gunakan HANYA informasi yang terdapat pada DATA BUKTI.
2. DILARANG menggunakan pengetahuan umum atau informasi dari luar DATA BUKTI.
3. DILARANG menambah, mengurangi, mengubah, atau mengarang informasi.
4. Jika jawaban tidak ditemukan pada DATA BUKTI maka jawab:

"MoHon maaf, data referensi saya tidak memuat informasi tersebut. Wallahu A'lam."

5. Jika DATA BUKTI berisi daftar langkah, tampilkan langkah tersebut sebagaimana terdapat pada DATA BUKTI.
6. Cantumkan sumber jika memang tersedia pada DATA BUKTI.

================================================================

DATA BUKTI:
{konteks_rujukan}

================================================================

PERTANYAAN:
{pertanyaan_user}

================================================================

JAWABAN:
"""

    kerangka_prompt = PromptTemplate.from_template(
        instruksi_sistem
    )

    rantai_proses = (
        kerangka_prompt
        | mesin_llm
        | StrOutputParser()
    )

    print("[*] Menginstruksikan LLM...")

    jawaban_final = rantai_proses.invoke({
        "konteks_rujukan": teks_sintesis,
        "pertanyaan_user": input_tanya
    })

    return jawaban_final, hasil_dokumen


def uji_coba_sistem_retriever():

    kueri_tes = "Apa itu Zakat Fitrah?"

    try:

        teks_jawab, bukti_referensi = (
            produksi_jawaban_berbasis_fakta(
                kueri_tes
            )
        )

        print("\n" + "=" * 50)
        print("💡 OUTPUT GENERATOR")
        print("=" * 50)
        print(teks_jawab)

        print("\n" + "=" * 50)
        print(
            f"📚 METRIK: {len(bukti_referensi)} fragmen digunakan"
        )
        print("=" * 50)

    except Exception as kendala:

        print(
            f"[!] Terjadi Kegagalan Sistem: {kendala}"
        )


if __name__ == "__main__":
    uji_coba_sistem_retriever()