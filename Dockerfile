# Foloseste o imagine de baza oficiala Python
FROM python:3.10-slim

# Seteaza directorul de lucru in container
WORKDIR /app

# Instaleaza dependintele
RUN pip install langchain \
    streamlit \
    pypdf \
    sentence-transformers \
    chromadb \
    langchain-community

# Copiaza restul codului sursa al aplicatiei in container
COPY . .

# Expune portul pe care ruleaza Streamlit
EXPOSE 8501

# Comanda pentru a rula aplicatia Streamlit
# Asigura-te ca fisierul principal al aplicatiei tale se numeste "app.py"
CMD ["streamlit", "run", "app.py"]