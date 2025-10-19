from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def get_embeddings_model():
    """Returneaza un model de embedding dedicat si performant."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vector_store(texts, embeddings_model):
    """Creeaza baza de date vectoriala (ChromaDB) din textele procesate."""
    vector_store = Chroma.from_documents(texts, embeddings_model)
    return vector_store
