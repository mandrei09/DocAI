# Dockerfile with persistent pip cache
# You need to add "#syntax=docker/dockerfile:1" at the top
#syntax=docker/dockerfile:1

FROM python:3.10.13-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    nano \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# This is the key change: --mount=type=cache...
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -v \
    --default-timeout=120 \
    --retries 5 \
    -r requirements.txt

COPY . .

EXPOSE 8501
# CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]
CMD ["tail", "-f", "/dev/null"]