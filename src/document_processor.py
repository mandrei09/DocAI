import re
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def preprocess_text(document: Document) -> Document:
    """Curăță conținutul text al unui obiect Document LangChain."""
    # Extrage textul din atributul .page_content
    text = document.page_content
    
    # Aplica toate operatiunile de curatare pe variabila 'text'
    text = text.lower()
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text) # Uneste cuvintele cu cratima
    text = re.sub(r'\s+', ' ', text).strip() # Elimina spatiile goale in plus
    text = re.sub(r'\s*pag(?:ina|\.)\s*\d+\s*', ' ', text, flags=re.IGNORECASE) # Elimina numerele de pagina
    
    # Actualizeaza continutul documentului cu textul curatat
    document.page_content = text
    return document

def load_and_process_pdf(pdf_path: str) -> List[Document]:
    """Încarcă un PDF, îl preprocesează, îl împarte în bucăți și returnează documentele."""
    loader = UnstructuredPDFLoader(
        file_path=pdf_path, 
        mode="elements"
    )
    documents = loader.load()
        
    # Aplica preprocesarea pe fiecare document din lista
    processed_documents = [preprocess_text(doc) for doc in documents]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=160,
        separators=["\n\n", "\n", " ", ""]
    )
    texts = text_splitter.split_documents(processed_documents)
    
    return texts
