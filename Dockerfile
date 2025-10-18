FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    nano \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install dependencies — this layer is cached as long as requirements.txt doesn't change
RUN pip install -v \ 
    # --no-cache-dir \
    --default-timeout=120 \
    --retries 5 \
    -r requirements.txt

# Now copy the rest of your app
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]
