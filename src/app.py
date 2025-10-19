import streamlit as st
import os
import tempfile

# Importa functiile din modulele create
from document_processor import load_and_process_pdf
from vector_store import get_embeddings_model, create_vector_store
from chain_setup import create_qa_chain

# --- Configurare Initiala ---
st.set_page_config(page_title="DocAI", layout="wide")
st.title("📄 Interoghează Documentele Tale PDF")

# Initializarea starii sesiunii pentru a stoca lantul si numele fisierului procesat
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "processed_file_name" not in st.session_state:
    st.session_state.processed_file_name = None

# --- Interfata Utilizator (UI) ---
st.sidebar.title("Configurare")
model_name = st.sidebar.selectbox(
    "Alege modelul LLM:",
    ("gemma:2b", "llama3", "mistral")
)

uploaded_file = st.file_uploader("Încarcă un document PDF", type="pdf")

# Daca un fisier nou este incarcat, reseteaza starea
if uploaded_file and uploaded_file.name != st.session_state.processed_file_name:
    st.session_state.qa_chain = None
    st.session_state.processed_file_name = uploaded_file.name

if uploaded_file:
    # Afiseaza un buton pentru a incepe procesarea
    if st.button("Procesează Documentul"):
        with st.spinner(f"Se procesează '{uploaded_file.name}'..."):
            try:
                # Gestioneaza fisierul temporar
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    pdf_path = tmp_file.name

                # PASUL 1: Incarca, preproceseaza si imparte documentul
                texts = load_and_process_pdf(pdf_path)

                # PASUL 2: Defineste si creeaza embeddings
                embeddings_model = get_embeddings_model()

                # PASUL 3: Creeaza baza de date vectoriala
                vector_store = create_vector_store(texts, embeddings_model)

                # PASUL 4: Creeaza lantul de interogare si il salveaza in starea sesiunii
                ollama_base_url = os.getenv("OLLAMA_HOST")
                st.session_state.qa_chain = create_qa_chain(model_name, ollama_base_url, vector_store)
                
                st.success("Documentul a fost procesat. Acum poți pune întrebări.")

            finally:
                # Sterge fisierul temporar dupa procesare
                if 'pdf_path' in locals() and os.path.exists(pdf_path):
                    os.remove(pdf_path)

# Afiseaza sectiunea de intrebari doar daca documentul a fost procesat
if st.session_state.qa_chain is not None:
    st.header("Pune o întrebare")
    question = st.text_input("Scrie întrebarea ta despre conținutul documentului:", key="question_input")

    if question:
        with st.spinner("Se generează răspunsul..."):
            # Ruleaza lantul doar cu intrebarea
            result = st.session_state.qa_chain({"query": question})

            st.subheader("Răspuns:")
            st.write(result["result"])

            with st.expander("Vezi sursele din document pe care s-a bazat răspunsul"):
                st.write(result["source_documents"])
else:
    st.info("Te rog încarcă un document PDF și apasă pe 'Procesează Documentul' pentru a începe.")
