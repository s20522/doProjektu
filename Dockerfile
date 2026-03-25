FROM ollama/ollama:latest

# Zainstaluj niezbędne pakiety
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj requirements.txt
COPY requirements.txt .

# Zainstaluj zależności Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY entrypoint.sh /entrypoint.sh

# Uprawnienia do entrypoint
RUN chmod +x /entrypoint.sh

# Expose port Ollama
EXPOSE 11434

# Uruchom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
