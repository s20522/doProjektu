# 🎬 TMDB Neo4j Pipeline - Przewodnik dla Początkujących

Witaj! Ten przewodnik wyjaśni Ci **krok po kroku** co znajduje się w tym projekcie i jak wszystko działa.

---

## 📁 Struktura Projektu - Mapa Repozytorium

```
doProjektu/
│
├── 📂 data/                          # Folder z danymi (tworzony automatycznie)
│   ├── raw/                          # Surowe dane (pobierane z HuggingFace)
│   │   ├── mpst_train.csv           # 9,489 filmów treningowych
│   │   ├── mpst_validation.csv      # 2,373 filmy walidacyjne
│   │   └── mpst_test.csv            # 2,966 filmów testowych
│   │
│   └── processed/                    # Oczyszczone dane (generowane przez skrypt)
│       ├── movies_train.json        # Oczyszczone dane treningowe
│       ├── movies_validation.json   # Oczyszczone dane walidacyjne
│       ├── movies_test.json         # Oczyszczone dane testowe
│       └── movies_all.json          # Wszystkie filmy w jednym pliku
│
├── 📂 scripts/                       # Skrypty do przetwarzania danych
│   ├── utils/
│   │   └── data_cleaner.py          # 🔑 GŁÓWNY SKRYPT - pobiera i czyszcza dane
│   │
│   └── import/
│       ├── neo4j_importer.py        # Import danych do Neo4j (bazy grafowej)
│       ├── chromadb_importer.py     # Import wektorów do ChromaDB (wyszukiwanie)
│       └── run_all_imports.py       # Uruchamia wszystkie importery
│
├── 📂 app/                           # Aplikacja Python (integracja z Ollama)
│   ├── config/
│   │   └── config.py                # Konfiguracja połączeń z bazami
│   └── main.py                      # Główna aplikacja
│
├── 📂 docker/                        # Konfiguracja Docker (jeśli używasz)
│   ├── docker-compose.yml           # Uruchamia Neo4j, ChromaDB, Ollama
│   └── Dockerfile                   # Obraz Docker dla aplikacji
│
├── 📄 requirements.txt               # Lista zależności Python
├── 📄 .env.example                   # Przykład zmiennych środowiskowych
├── 📄 README.md                      # Dokumentacja projektu
├── 📄 TUTORIAL.md                    # Szczegółowy tutorial
├── 📄 QUICK_START.md                 # Szybki start
└── 📄 BEGINNER_GUIDE.md             # Ten plik!
```

---

## 🎯 Co To Jest Ten Projekt?

### Cel Projektu

Ten projekt to **system do analizy i wyszukiwania filmów** używając:
- **Bazy grafowej (Neo4j)** - przechowuje relacje między filmami, gatunkami i tagami
- **Bazy wektorowej (ChromaDB)** - pozwala wyszukiwać filmy po znaczeniu (nie tylko słowa kluczowe)
- **Modelu AI (Ollama)** - do generowania opisów i odpowiadania na pytania

### Prosty Przykład

Wyobraź sobie, że chcesz znaleźć film:
- **Tradycyjnie**: "Szukaj filmów z słowem 'morderstwo'"
- **Z tym projektem**: "Szukaj filmów o tajemniczych zbrodniach" (wyszukiwanie semantyczne!)

---

## 🚀 Jak Uruchomić Projekt - Krok po Kroku

### Krok 1: Instalacja Zależności

Najpierw zainstaluj wszystkie wymagane pakiety Python:

```bash
pip install -r requirements.txt
```

**Co to robi?**
- Instaluje biblioteki do pracy z danymi (pandas, numpy)
- Instaluje sterowniki do baz danych (neo4j, chromadb)
- Instaluje narzędzia do pobierania danych (datasets)

### Krok 2: Uruchomienie Data Cleanera

To jest **najważniejszy krok**! Skrypt `data_cleaner.py` robi 3 rzeczy:

```bash
python scripts/utils/data_cleaner.py
```

**Co się dzieje:**

1. **Pobieranie danych** 📥
   - Pobiera dataset MPST z HuggingFace
   - Zapisuje do `data/raw/` (3 pliki CSV)
   - Zajmuje ~5-10 minut (zależy od internetu)

2. **Czyszczenie danych** 🧹
   - Usuwa białe znaki i znaki specjalne
   - Parsuje tagi i gatunki
   - Waliduje dane
   - Zajmuje ~30 sekund

3. **Generowanie JSON** 📄
   - Konwertuje CSV → JSON
   - Tworzy `data/processed/movies_all.json`
   - Zawiera 14,828 filmów

**Wynik:**
```
✅ Liczba filmów: 14,828
✅ Gatunki: 10 (horror, comedy, action, itp.)
✅ Tagi: 71 (murder, violence, romantic, itp.)
✅ Plik: data/processed/movies_all.json
```

---

## 📊 Struktura Danych - Co Zawiera Każdy Film?

Po uruchomieniu `data_cleaner.py` każdy film w `movies_all.json` wygląda tak:

```json
{
  "imdb_id": "tt0057603",
  "title": "I tre volti della paura",
  "plot_synopsis": "Boris Karloff introduces three horror tales...",
  "tags": ["cult", "horror", "gothic", "murder", "atmospheric"],
  "genres": ["cult", "horror", "gothic"],
  "synopsis_source": "imdb",
  "review": "A classic horror anthology...",
  "split": "train"
}
```

**Wyjaśnienie pól:**
- `imdb_id` - unikalny identyfikator IMDb
- `title` - nazwa filmu
- `plot_synopsis` - streszczenie fabuły (używane do wyszukiwania semantycznego)
- `tags` - tagi opisujące film (71 możliwych wartości)
- `genres` - gatunki filmowe (10 możliwych wartości)
- `synopsis_source` - źródło streszczenia
- `review` - recenzja
- `split` - czy to dane treningowe/walidacyjne/testowe

---

## 🗄️ Bazy Danych - Po Co Każda?

### 1. Neo4j (Baza Grafowa) 🕸️

**Po co?** Przechowuje relacje między filmami, gatunkami i tagami.

**Jak działa?**
- Węzły (nodes): `Movie`, `Genre`, `Tag`
- Relacje (edges): `Movie -[IN_GENRE]-> Genre`, `Movie -[HAS_TAG]-> Tag`

**Przykład zapytania:**
```cypher
// Znajdź wszystkie horrory
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
WHERE g.name = 'horror'
RETURN m.title, m.imdb_id
LIMIT 10
```

**Kiedy używać?**
- Szukanie filmów po gatunku
- Analiza sieci (jakie gatunki są powiązane?)
- Złożone zapytania relacyjne

### 2. ChromaDB (Baza Wektorowa) 🔍

**Po co?** Przechowuje "wektory" (liczby reprezentujące znaczenie) streszczań filmów.

**Jak działa?**
- Konwertuje tekst → liczby (embedding)
- Pozwala wyszukiwać po **znaczeniu**, nie po słowach

**Przykład:**
- Zapytanie: "straszne filmy o zabójstwach"
- ChromaDB znajduje filmy z podobnym znaczeniem (nawet jeśli słowa są inne!)

**Kiedy używać?**
- Wyszukiwanie semantyczne
- "Znajdź filmy podobne do tego"
- Rekomendacje

### 3. Ollama (Model AI) 🤖

**Po co?** Generuje odpowiedzi i opisy na podstawie danych.

**Jak działa?**
- Uruchamia model Mistral (LLM - Large Language Model)
- Może odpowiadać na pytania o filmy
- Może generować opisy

**Kiedy używać?**
- Pytania w języku naturalnym
- Generowanie opisów
- Czatbot o filmach

---

## 🔧 Skrypty - Co Robi Każdy?

### `data_cleaner.py` - Przygotowanie Danych

**Lokalizacja:** `scripts/utils/data_cleaner.py`

**Co robi:**
1. Pobiera dane z HuggingFace
2. Czyści i waliduje dane
3. Konwertuje CSV → JSON
4. Wypisuje statystyki

**Kiedy uruchamiać:**
- Pierwszy raz (pobieranie danych)
- Gdy chcesz odświeżyć dane

**Uruchomienie:**
```bash
python scripts/utils/data_cleaner.py
```

---

### `neo4j_importer.py` - Import do Neo4j

**Lokalizacja:** `scripts/import/neo4j_importer.py`

**Co robi:**
1. Wczytuje `movies_all.json`
2. Tworzy węzły `Movie`, `Genre`, `Tag`
3. Tworzy relacje między nimi
4. Importuje do Neo4j

**Wymagania:**
- Neo4j musi być uruchomiony (Docker lub lokalnie)
- Plik `movies_all.json` musi istnieć

**Kiedy uruchamiać:**
- Po uruchomieniu Neo4j
- Gdy chcesz załadować dane do bazy

**Uruchomienie:**
```bash
python scripts/import/neo4j_importer.py
```

---

### `chromadb_importer.py` - Import do ChromaDB

**Lokalizacja:** `scripts/import/chromadb_importer.py`

**Co robi:**
1. Wczytuje `movies_all.json`
2. Konwertuje streszczenia → wektory (embeddings)
3. Importuje do ChromaDB

**Wymagania:**
- ChromaDB musi być uruchomiony
- Plik `movies_all.json` musi istnieć

**Kiedy uruchamiać:**
- Po uruchomieniu ChromaDB
- Gdy chcesz włączyć wyszukiwanie semantyczne

**Uruchomienie:**
```bash
python scripts/import/chromadb_importer.py
```

---

### `run_all_imports.py` - Uruchomienie Wszystkich

**Lokalizacja:** `scripts/import/run_all_imports.py`

**Co robi:**
- Uruchamia `neo4j_importer.py` i `chromadb_importer.py` po kolei

**Kiedy uruchamiać:**
- Gdy chcesz załadować dane do obu baz naraz

**Uruchomienie:**
```bash
python scripts/import/run_all_imports.py
```

---

## 🐳 Docker - Jak Uruchomić Bazy Danych?

Docker to narzędzie do uruchamiania aplikacji w "kontenerach" (izolowanych środowiskach).

### Instalacja Docker

1. Pobierz z https://www.docker.com/products/docker-desktop
2. Zainstaluj i uruchom

### Uruchomienie Baz

```bash
docker-compose up -d
```

**Co się uruchamia:**
- **Neo4j** na `http://localhost:7474`
- **ChromaDB** na `http://localhost:8000`
- **Ollama** na `http://localhost:11434`

### Dostęp do Neo4j Browser

1. Otwórz `http://localhost:7474`
2. Login: `neo4j` / hasło: `password123`
3. Możesz pisać zapytania Cypher!

### Zatrzymanie Baz

```bash
docker-compose down
```

---

## 📚 Pełny Workflow - Jak Wszystko Razem Działa?

### Scenariusz: Chcę Znaleźć Horrory

**Krok 1: Przygotowanie Danych**
```bash
python scripts/utils/data_cleaner.py
# ✅ Tworzy data/processed/movies_all.json
```

**Krok 2: Uruchomienie Baz**
```bash
docker-compose up -d
# ✅ Neo4j, ChromaDB, Ollama działają
```

**Krok 3: Import Danych**
```bash
python scripts/import/run_all_imports.py
# ✅ Dane są w Neo4j i ChromaDB
```

**Krok 4: Wyszukiwanie w Neo4j**
```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
WHERE g.name = 'horror'
RETURN m.title
LIMIT 10
```

**Krok 5: Wyszukiwanie Semantyczne w ChromaDB**
```python
results = collection.query(
    query_texts=["scary horror films"],
    n_results=10
)
# ✅ Znajduje filmy podobne do "scary horror films"
```

---

## 🎓 Wyjaśnienie Pojęć

### CSV vs JSON

**CSV** (Comma-Separated Values):
```
imdb_id,title,plot_synopsis
tt0057603,"I tre volti della paura","Boris Karloff introduces..."
```
- Format tabelaryczny (jak Excel)
- Łatwy do czytania dla ludzi
- Używany do przechowywania danych surowych

**JSON** (JavaScript Object Notation):
```json
{
  "imdb_id": "tt0057603",
  "title": "I tre volti della paura",
  "plot_synopsis": "Boris Karloff introduces..."
}
```
- Format strukturyzowany
- Łatwy do przetwarzania przez programy
- Używany do przechowywania danych oczyszczonych

### Embedding (Wektor)

**Embedding** to reprezentacja tekstu jako lista liczb:
```
"scary horror film" → [0.234, -0.512, 0.891, ...]
```

**Po co?**
- Komputery rozumieją liczby lepiej niż tekst
- Pozwala porównywać podobieństwo tekstów
- Umożliwia wyszukiwanie semantyczne

### Cypher (Język Zapytań Neo4j)

**Cypher** to język do pisania zapytań do Neo4j:
```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
WHERE g.name = 'horror'
RETURN m.title
```

**Wyjaśnienie:**
- `MATCH` - szukaj wzorca
- `(m:Movie)` - węzeł typu Movie
- `-[:IN_GENRE]->` - relacja IN_GENRE
- `WHERE` - warunek
- `RETURN` - zwróć wynik

---

## 💡 Porady dla Początkujących

### 1. Zacznij od `data_cleaner.py`
To jest punkt wejścia. Najpierw przygotuj dane.

### 2. Sprawdź Strukturę JSON
```bash
# Otwórz data/processed/movies_all.json w edytorze
# Zobaczysz jak wyglądają dane
```

### 3. Eksperymentuj z Neo4j Browser
```bash
# Otwórz http://localhost:7474
# Pisz zapytania Cypher i zobacz wyniki
```

### 4. Czytaj Logi
Skrypty wypisują logi - czytaj je! Mówią co się dzieje.

### 5. Nie Bój Się Błędów
- Błędy to część nauki
- Czytaj komunikaty błędów
- Szukaj rozwiązań online

---

## 🆘 Rozwiązywanie Problemów

### Problem: "0 filmów pobranych"
**Przyczyna:** Folder `data/raw` jest pusty
**Rozwiązanie:** Uruchom `data_cleaner.py` - pobierze dane z HuggingFace

### Problem: "Neo4j connection refused"
**Przyczyna:** Neo4j nie jest uruchomiony
**Rozwiązanie:** Uruchom `docker-compose up -d`

### Problem: "ModuleNotFoundError: No module named 'datasets'"
**Przyczyna:** Pakiet `datasets` nie jest zainstalowany
**Rozwiązanie:** `pip install -r requirements.txt`

### Problem: "Permission denied"
**Przyczyna:** Brak uprawnień do folderu
**Rozwiązanie:** Sprawdź uprawnienia folderu lub uruchom z `sudo`

---

## 📖 Następne Kroki

1. **Przeczytaj README.md** - bardziej techniczny opis
2. **Przeczytaj TUTORIAL.md** - szczegółowy tutorial
3. **Przeczytaj QUICK_START.md** - szybki start dla doświadczonych
4. **Eksperymentuj!** - zmień kod i zobacz co się stanie

---

## 🔗 Przydatne Linki

- **Neo4j Dokumentacja**: https://neo4j.com/docs/
- **ChromaDB Dokumentacja**: https://docs.trychroma.com/
- **Ollama**: https://ollama.ai/
- **HuggingFace Datasets**: https://huggingface.co/datasets
- **Docker**: https://www.docker.com/

---

## ❓ Pytania?

Jeśli masz pytania:
1. Sprawdź README.md
2. Sprawdź TUTORIAL.md
3. Przeczytaj logi błędów
4. Szukaj w Google
5. Pytaj na Stack Overflow

---

**Powodzenia! 🚀 Teraz jesteś gotów do pracy z tym projektem!**
