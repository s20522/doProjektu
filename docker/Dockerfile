FROM python:3.11-slim

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie requirements
COPY requirements.txt .

# Instalacja zależności Python
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu
COPY scripts/ /app/scripts/
COPY data/ /app/data/

# Ustawienie zmiennych środowiskowych
ENV PYTHONUNBUFFERED=1
ENV NEO4J_URI=bolt://neo4j:7687
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=password123
ENV CHROMADB_HOST=chromadb
ENV CHROMADB_PORT=8000
ENV OLLAMA_HOST=http://ollama:11434

# Domyślna komenda
CMD ["python", "scripts/import/neo4j_importer.py"]
