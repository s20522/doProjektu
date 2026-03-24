# TMDB (MPST) Neo4j & ChromaDB Data Pipeline

## O Projekcie

Ten projekt to **kompletny system do zarządzania i analizy danych filmowych** przy użyciu nowoczesnych technologii baz danych. Projekt łączy trzy kluczowe komponenty:

### 🎯 Cel Projektu

Celem jest **zbudowanie inteligentnego systemu wyszukiwania i analizy filmów** opartego na:
- **Grafowych relacjach** między filmami, osobami (reżyserami, aktorami) i gatunkami
- **Wyszukiwaniu semantycznym** na podstawie streszczeń filmów
- **Lokalnych modelach AI** do przetwarzania naturalnego języka

### 🏗️ Jak To Działa?

```
┌─────────────────────────────────────────────────────────────┐
│  1. POBRANIE DANYCH                                         │
│  Pobieramy 14,828 filmów z HuggingFace (MPST dataset)      │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│  2. CZYSZCZENIE I TRANSFORMACJA                             │
│  CSV → JSON, normalizacja tagów, ekstrakcja gatunków       │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│  3. IMPORT DO BAZ DANYCH                                    │
│  ├─ Neo4j: Grafy relacji (filmy ↔ osoby ↔ gatunki)        │
│  └─ ChromaDB: Wektory (embeddings streszczeń)              │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│  4. ANALIZA I WYSZUKIWANIE                                  │
│  ├─ Zapytania grafowe (np. "Filmy reżysera X")            │
│  ├─ Wyszukiwanie semantyczne (np. "Filmy o zemście")      │
│  └─ Integracja z Ollama (AI queries)                       │
└─────────────────────────────────────────────────────────────┘
```

### 💡 Praktyczne Zastosowania

1. **Rekomendacja Filmów** - Na podstawie podobieństwa streszczeń i relacji między filmami
2. **Analiza Sieci Twórców** - Znalezienie powiązań między reżyserami, aktorami i gatunkami
3. **Wyszukiwanie Semantyczne** - "Znajdź filmy podobne do tego o zemście i morderstwie"
4. **Eksploracja Danych** - Wizualizacja sieci powiązań między filmami
5. **Integracja AI** - Generowanie opisów lub odpowiadanie na pytania o filmy

## Architektura Systemu

Projekt wykorzystuje konteneryzację Docker do uruchomienia całego środowiska:

| Komponent | Rola | Port | Zastosowanie |
|-----------|------|------|--------------|
| **Neo4j** | Graph Database | 7474/7687 | Przechowywanie relacji między filmami, osobami i gatunkami |
| **ChromaDB** | Vector Database | 8000 | Przechowywanie embeddings streszczeń dla wyszukiwania semantycznego |
| **Ollama** | Local LLM | 11434 | Lokalne modele AI do przetwarzania naturalnego języka |
| **Python App** | Data Pipeline | - | Czyszczenie danych i import do baz |

## Wymagania

- Docker i Docker Compose
- Python 3.11+ (do lokalnego uruchamiania skryptów)
- Git
- Minimum 4 GB RAM (dla Docker)
- Minimum 10 GB wolnego miejsca na dysku

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
- **Neo4j Browser**: http://localhost:7474 (login: `neo4j`, hasło: `password123`)
- **ChromaDB API**: http://localhost:8000
- **Ollama API**: http://localhost:11434

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
- **Movie**: `imdb_id`, `title`, `plot_synopsis`, `tags`, `synopsis_source`, `review`
- **Person**: Reprezentuje osoby związane z filmem (reżyserzy, aktorzy)
- **Genre**: Gatunki filmowe

### Relacje (Relationships)
- `(Person)-[:DIRECTED]->(Movie)`: Reżyserowanie
- `(Person)-[:ACTED_IN]->(Movie)`: Występowanie w filmie
- `(Movie)-[:IN_GENRE]->(Genre)`: Przynależność do gatunku

### Przykładowe Zapytania Cypher

```cypher
# Znaleźć wszystkie filmy w gatunku "horror"
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name: "horror"})
RETURN m.title, m.plot_synopsis LIMIT 10

# Znaleźć filmy z określonym tagiem
MATCH (m:Movie)
WHERE "murder" IN m.tags
RETURN m.title, m.tags LIMIT 5

# Znaleźć reżyserów i ich filmy
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p.name, COUNT(m) as film_count
ORDER BY film_count DESC
```

## ChromaDB - Wyszukiwanie Semantyczne

ChromaDB pozwala na wyszukiwanie filmów na podstawie **znaczenia**, a nie tylko słów kluczowych:

```python
# Przykład: Wyszukiwanie filmów o zemście
results = chromadb_importer.search_movies("revenge and murder", n_results=5)
# Zwróci filmy zawierające podobne tematy, nawet jeśli nie mają dokładnie tych słów
```

## Statystyki Danych

Po poprawnym uruchomieniu pipeline'u, baza będzie zawierać:

| Metrika | Wartość |
|---------|---------|
| Liczba filmów | 14,828 |
| Liczba gatunków | 10 |
| Liczba tagów | 71 |
| Rozmiar danych | 225.4 MB |
| Średnia długość streszczenia | ~7,500 znaków |

### Top Gatunki
1. **cult** (2,647 filmów)
2. **comedy** (1,859 filmów)
3. **action** (664 filmów)
4. **fantasy** (564 filmów)
5. **mystery** (519 filmów)

### Top Tagi
1. **murder** (5,782 filmów)
2. **violence** (4,426 filmów)
3. **flashback** (2,937 filmów)
4. **romantic** (2,906 filmów)
5. **revenge** (2,468 filmów)

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
│   │   ├── chromadb_importer.py   # Import do ChromaDB
│   │   ├── neo4j_importer.py      # Import do Neo4j
│   │   └── run_all_imports.py     # Orchestracja wszystkich importów
│   └── utils/             # Narzędzia pomocnicze
│       └── data_cleaner.py        # Czyszczenie i transformacja danych
├── .env.example           # Szablon konfiguracji
├── requirements.txt       # Zależności Python
└── README.md              # Dokumentacja projektu
```

## Komponenty Projektu

### 1. Data Cleaner (`scripts/utils/data_cleaner.py`)
- Pobiera dane z HuggingFace w formacie CSV
- Czyści i normalizuje tekst
- Parsuje i waliduje tagi
- Ekstrakcja gatunków z tagów
- Eksport do JSON

### 2. Neo4j Importer (`scripts/import/neo4j_importer.py`)
- Tworzenie węzłów Movie, Person, Genre
- Tworzenie relacji między węzłami
- Indeksowanie i ograniczenia unikalności
- Statystyki bazy danych

### 3. ChromaDB Importer (`scripts/import/chromadb_importer.py`)
- Import streszczeń filmów
- Generowanie embeddings
- Wyszukiwanie semantyczne
- Metadane filmów

### 4. Run All Imports (`scripts/import/run_all_imports.py`)
- Orchestracja wszystkich importów
- Raportowanie błędów
- Podsumowanie wyników

## Status Testów

✅ **Wszystkie komponenty zostały przetestowane:**
- ✅ Transformacja danych (CSV → JSON) - 14,828 filmów przetworzonych bez błędów
- ✅ Struktura wyjściowa JSON (225.4 MB) - zwalidowana
- ✅ Skrypty importujące - wolne od błędów syntaktycznych
- ✅ Docker Compose - skonfigurowany i gotowy
- ✅ Dokumentacja - kompletna i aktualna

## Zaawansowane Użycie

### Dostosowanie Konfiguracji

Edytuj plik `.env` aby zmienić:
- Hasła do Neo4j
- Hosty i porty usług
- Rozmiar batcha dla importu
- Ścieżki do danych

### Rozszerzanie Projektu

Możesz łatwo rozszerzyć projekt o:
- Dodatkowe źródła danych (IMDb, Rotten Tomatoes)
- Integrację z API filmowych
- Interfejs webowy (Flask/FastAPI)
- Zaawansowane zapytania AI

## Autor

Projekt przygotowany przez **Manus AI**.

## Licencja

MIT License - Projekt jest otwarty i dostępny dla wszystkich.

## Referencje

- [MPST Dataset - HuggingFace](https://huggingface.co/datasets/cryptexcode/MPST)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Documentation](https://ollama.ai/)
