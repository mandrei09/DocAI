import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os

# --- Configurare Initiala ---
st.set_page_config(page_title="Interogare PDF cu AI Open-Source", layout="wide")
st.title("📄 Interoghează Documentele Tale PDF (100% Open-Source)")

# --- Functii Utilitare ---

@st.cache_resource
def load_and_process_pdf(pdf_path):
    """Incarca PDF-ul, il imparte in bucati (chunks) si returneaza documentele."""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    return texts

@st.cache_resource
def create_vector_store(_texts, _embeddings):
    """Creeaza baza de date vectoriala (ChromaDB) din textele procesate."""
    db = Chroma.from_documents(_texts, _embeddings)
    return db

# --- Interfata Utilizator (UI) ---

st.sidebar.title("Configurare Model")
model_name = st.sidebar.selectbox(
    "Alege modelul LLM pe care l-ai descărcat cu Ollama:",
    ("llama3", "mistral", "gemma:7b")
)

uploaded_file = st.file_uploader("Încarcă un document PDF", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Fișierul '{uploaded_file.name}' a fost încărcat cu succes!")

    with st.spinner(f"Se procesează documentul și se rulează modelul '{model_name}'... (poate dura puțin)"):
        # 1. Proceseaza PDF-ul
        texts = load_and_process_pdf("temp.pdf")
        
        # 2. Defineste modelul de embedding (ruleaza local via Ollama)
        # Ollama foloseste acelasi model (ex: llama3) pentru a genera si embeddings
        embeddings_model = OllamaEmbeddings(model=model_name)
        
        # 3. Creeaza baza de date vectoriala
        vector_store = create_vector_store(texts, embeddings_model)
        
        # 4. Defineste LLM-ul local
        llm = Ollama(model=model_name)
        
        st.info("Documentul a fost procesat. Acum poți pune întrebări.")

    question = st.text_input("Pune o întrebare despre conținutul documentului:")

    if question:
        # Creeaza lantul de interogare (chain)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=vector_store.as_retriever(),
            return_source_documents=True
        )
        
        with st.spinner("Se generează răspunsul..."):
            result = qa_chain({"query": question})
            st.subheader("Răspuns:")
            st.write(result["result"])
            
            with st.expander("Vezi sursele din document pe care s-a bazat răspunsul"):
                st.write(result["source_documents"])
else:
    st.info("Te rog încarcă un document PDF pentru a începe.")