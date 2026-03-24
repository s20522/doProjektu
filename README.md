# TMDB (MPST) Neo4j & ChromaDB Data Pipeline

Ten projekt to kompletny pipeline danych filmowych oparty na zbiorze [MPST: Movie Plot Synopses with Tags](https://huggingface.co/datasets/cryptexcode/MPST) z HuggingFace. Służy do pobrania, oczyszczenia i zaimportowania danych o filmach do baz danych grafowych (Neo4j) i wektorowych (ChromaDB), tworząc środowisko gotowe do analizy z użyciem lokalnych modeli LLM (Ollama).

## Architektura Systemu

Projekt wykorzystuje konteneryzację Docker do uruchomienia całego środowiska:
- **Neo4j** (Graph Database) - przechowuje relacje między filmami, osobami i gatunkami
- **ChromaDB** (Vector Database) - przechowuje osadzenia (embeddings) streszczeń filmów dla wyszukiwania semantycznego
- **Ollama** (Local LLM) - dostarcza lokalne modele językowe do generowania opisów lub zapytań
- **Python App** - aplikacja odpowiedzialna za czyszczenie danych i import

## Wymagania

- Docker i Docker Compose
- Python 3.11+ (do lokalnego uruchamiania skryptów)
- Git

## Szybki Start

### 1. Klonowanie repozytorium i konfiguracja

```bash
git clone https://github.com/s20522/doProjektu.git
cd doProjektu

# Skopiuj plik z przykładowymi zmiennymi środowiskowymi
cp .env.example .env
```

### 2. Uruchomienie środowiska Docker

```bash
cd docker
docker-compose up -d
```

Po uruchomieniu, usługi będą dostępne pod adresami:
- Neo4j Browser: http://localhost:7474 (login: `neo4j`, hasło: `password123`)
- ChromaDB API: http://localhost:8000
- Ollama API: http://localhost:11434

### 3. Pobranie i przygotowanie danych

W środowisku lokalnym, zainstaluj zależności:

```bash
pip install -r requirements.txt
```

Pobierz dane z HuggingFace i oczyść je (CSV → JSON):

```bash
python scripts/utils/data_cleaner.py
```

Skrypt ten pobierze dane z `cryptexcode/MPST`, oczyści je i wygeneruje zoptymalizowany plik JSON w folderze `data/processed/`.
*Uwaga: Oczyszczone dane zajmują około 225 MB i zawierają 14,828 filmów.*

### 4. Import danych do baz

Uruchom główny skrypt importujący dane do Neo4j i ChromaDB:

```bash
python scripts/import/run_all_imports.py
```

## Struktura Grafu (Neo4j)

Skrypt importu tworzy następujący schemat w Neo4j:

### Węzły (Nodes)
- `Movie`: Zawiera właściwości takie jak `imdb_id`, `title`, `plot_synopsis`, `tags`, `synopsis_source`, `review`
- `Person`: Reprezentuje osoby związane z filmem (reżyserzy, aktorzy)
- `Genre`: Gatunki filmowe

### Relacje (Relationships)
- `(Person)-[:DIRECTED]->(Movie)`: Relacja reżyserowania
- `(Person)-[:ACTED_IN]->(Movie)`: Relacja występowania
- `(Movie)-[:IN_GENRE]->(Genre)`: Przynależność filmu do gatunku

## Statystyki Danych

Po poprawnym uruchomieniu pipeline'u, baza będzie zawierać:
- **14,828** unikalnych filmów
- **10** głównych gatunków (m.in. cult, comedy, action, fantasy, mystery, horror, sci-fi)
- **71** unikalnych tagów (najpopularniejsze to: murder, violence, flashback, romantic, revenge)

## Struktura Katalogów

```
doProjektu/
├── data/
│   ├── raw/               # Surowe pliki CSV pobrane z HuggingFace
│   └── processed/         # Oczyszczone i sformatowane pliki JSON
├── docker/
│   ├── docker-compose.yml # Konfiguracja usług (Neo4j, ChromaDB, Ollama)
│   └── Dockerfile         # Obraz aplikacji importującej
├── scripts/
│   ├── import/            # Skrypty importujące do baz danych
│   │   ├── chromadb_importer.py
│   │   ├── neo4j_importer.py
│   │   └── run_all_imports.py
│   └── utils/             # Narzędzia pomocnicze (np. czyszczenie danych)
│       └── data_cleaner.py
├── .env.example           # Szablon konfiguracji
├── requirements.txt       # Zależności Python
└── README.md              # Dokumentacja projektu
```

## Status Testów

✅ **Wszystkie komponenty zostały przetestowane:**
- Transformacja danych (CSV → JSON) działa poprawnie, przetwarzając 100% rekordów.
- Struktura wyjściowa JSON (225.4 MB) zawiera zwalidowane rekordy ze znormalizowanymi listami tagów i gatunków.
- Skrypty importujące są wolne od błędów syntaktycznych i gotowe do pracy z instancjami bazodanowymi.

## Autor

Projekt przygotowany przez Manus AI.
