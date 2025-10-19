from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

def create_qa_chain(model_name: str, ollama_base_url: str, vector_store):
    """Creeaza si returneaza lantul RetrievalQA configurat corect."""
    # 1. Defineste sablonul pentru prompt
    prompt_template = """Folosește următoarele bucăți de context pentru a răspunde la întrebare la final. Dacă nu știi răspunsul, spune doar că nu știi, nu încerca să inventezi un răspuns. Răspunde în limba română.

    Context: {context}

    Întrebare: {question}

    Răspuns util:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # 2. Initializeaza LLM-ul local
    llm = Ollama(model=model_name, base_url=ollama_base_url)

    # 3. Creeaza lantul RetrievalQA, pasand prompt-ul la initializare
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(
            search_kwargs={"k": 5},
            search_type="mmr"
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain
