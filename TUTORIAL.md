# 📚 Tutorial dla Początkujących - TMDB Neo4j & ChromaDB Pipeline

Ten tutorial wyjaśnia wszystkie pojęcia używane w projekcie i pokazuje krok po kroku jak zainstalować i uruchomić projekt na Windows z WSL.

## Spis Treści

1. [Wyjaśnienie Pojęć](#wyjaśnienie-pojęć)
2. [Instalacja WSL na Windows](#instalacja-wsl-na-windows)
3. [Instalacja Docker na WSL](#instalacja-docker-na-wsl)
4. [Uruchomienie Projektu](#uruchomienie-projektu)
5. [Dodatkowe Zasoby](#dodatkowe-zasoby)

---

## Wyjaśnienie Pojęć

### 🗄️ Bazy Danych

#### Neo4j - Baza Grafowa

**Co to jest?**
Neo4j to baza danych, która przechowuje dane w formie **grafów** - czyli sieci powiązań między obiektami.

**Analogia:**
Wyobraź sobie sieć społeczną (Facebook):
- **Węzły** (nodes) = osoby
- **Krawędzie** (edges/relationships) = przyjaźnie między osobami

W naszym projekcie:
- **Węzły**: Filmy, Osoby (reżyserzy, aktorzy), Gatunki
- **Krawędzie**: "Film X został wyreżyserowany przez osobę Y", "Film X należy do gatunku Z"

**Dlaczego to przydatne?**
- Szybkie odpowiadanie na pytania typu: "Jakie filmy wyreżyserował reżyser X?"
- Znalezienie powiązań między filmami (np. filmy tego samego reżysera)
- Analiza sieci powiązań

**Przykład zapytania:**
```
Znajdź wszystkie filmy gatunku "horror" wyreżyserowane przez osobę X
```

📖 **Więcej informacji:**
- [Neo4j Official Documentation](https://neo4j.com/docs/)
- [Neo4j Beginner's Guide](https://neo4j.com/developer/get-started/)
- [Cypher Query Language Tutorial](https://neo4j.com/developer/cypher/)

---

#### ChromaDB - Baza Wektorowa

**Co to jest?**
ChromaDB to baza danych, która przechowuje **embeddings** - czyli matematyczne reprezentacje tekstu.

**Analogia:**
Wyobraź sobie, że każde słowo ma swoje "miejsce" w przestrzeni:
- Słowa o podobnym znaczeniu są blisko siebie
- Słowa o różnym znaczeniu są daleko od siebie

Przykład:
```
"morderstwo" i "zabójstwo" - blisko siebie (podobne znaczenie)
"morderstwo" i "miłość" - daleko od siebie (różne znaczenie)
```

**Dlaczego to przydatne?**
- Wyszukiwanie semantyczne: "Znajdź filmy o zemście" - znajdzie też filmy o "odwecie" czy "pomszczeniu"
- Znalezienie filmów podobnych do danego
- Rekomendacje oparte na znaczeniu, a nie tylko słowach kluczowych

**Jak to działa?**
1. Tekst (streszczenie filmu) → Embedding (liczby)
2. Nowe zapytanie → Embedding (liczby)
3. Porównanie: które embeddingi są najbliżej zapytania?

📖 **Więcej informacji:**
- [ChromaDB Official Documentation](https://docs.trychroma.com/)
- [What are Embeddings?](https://platform.openai.com/docs/guides/embeddings)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)

---

### 🤖 AI i Modele Języka

#### Ollama - Lokalne Modele AI

**Co to jest?**
Ollama to narzędzie, które pozwala uruchamiać **duże modele języka (LLM)** na twoim komputerze bez wysyłania danych do internetu.

**Analogia:**
Zamiast pytać ChatGPT online (wysyłając dane), masz swojego "ChatGPT" na komputerze.

**Dostępne modele:**
- `llama2` - ogólny model
- `mistral` - szybki i lekki
- `neural-chat` - specjalizowany w rozmowach

**Dlaczego to przydatne?**
- Prywatność: dane zostają na twoim komputerze
- Szybkość: nie czekasz na odpowiedź z internetu
- Koszt: darmowe (bez subskrypcji)

**Zastosowanie w projekcie:**
- Generowanie opisów filmów
- Odpowiadanie na pytania o filmy
- Analiza sentimentu streszczeń

📖 **Więcej informacji:**
- [Ollama Official Website](https://ollama.ai/)
- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Large Language Models Explained](https://www.ibm.com/topics/large-language-models)

---

### 📦 Docker i Konteneryzacja

#### Co to jest Docker?

**Analogia:**
Docker to jak **kontener transportowy** dla oprogramowania:
- Zamiast wysyłać komputer, wysyłasz kontener z aplikacją
- Kontener zawiera wszystko co potrzebne: kod, biblioteki, konfiguracja
- Kontener działa identycznie na każdym komputerze

**Dlaczego to przydatne?**
- Nie musisz instalować Neo4j, ChromaDB, Ollama ręcznie
- Wszystko jest już skonfigurowane w kontenerze
- Łatwe uruchamianie i zatrzymywanie

**Docker Compose**
- Plik YAML, który definiuje wiele kontenerów naraz
- W naszym projekcie: Neo4j + ChromaDB + Ollama w jednym poleceniu

**Przykład:**
```bash
docker-compose up -d
# Zamiast instalować 3 usługi ręcznie, wszystko się uruchamia automatycznie
```

📖 **Więcej informacji:**
- [Docker Official Documentation](https://docs.docker.com/)
- [Docker for Beginners](https://docker-curriculum.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)

---

### 🐍 Python i Skrypty

#### Co to jest Python?

**Analogia:**
Python to język programowania, który jest łatwy do nauki i czytania - jak instrukcja w języku naturalnym.

**Dlaczego Python?**
- Łatwy do nauki dla początkujących
- Doskonały do przetwarzania danych
- Duża ilość bibliotek do pracy z bazami danych

**Biblioteki używane w projekcie:**
- `pandas` - przetwarzanie danych (CSV, JSON)
- `neo4j` - komunikacja z Neo4j
- `requests` - wysyłanie zapytań HTTP do ChromaDB

📖 **Więcej informacji:**
- [Python Official Website](https://www.python.org/)
- [Python for Data Science](https://www.python.org/jobs/resource/guide-to-python-for-data-science/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

### 📊 Dane i Formaty

#### CSV vs JSON

**CSV (Comma-Separated Values)**
```
imdb_id,title,plot_synopsis
tt0057603,"I tre volti della paura","Note: this synopsis..."
tt1733125,"Another Movie","Plot description..."
```
- Prosty format tabelaryczny
- Łatwy do czytania w Excelu
- Ograniczony do płaskich struktur

**JSON (JavaScript Object Notation)**
```json
[
  {
    "imdb_id": "tt0057603",
    "title": "I tre volti della paura",
    "plot_synopsis": "Note: this synopsis...",
    "tags": ["cult", "horror", "gothic"],
    "genres": ["cult", "horror", "gothic"]
  }
]
```
- Bardziej elastyczny format
- Obsługuje zagnieżdżone struktury (listy, obiekty)
- Łatwy do przetwarzania w programach

**Dlaczego konwersja?**
CSV jest prosty, ale JSON lepiej reprezentuje złożone dane z tagami i gatunkami.

📖 **Więcej informacji:**
- [CSV Format Explanation](https://en.wikipedia.org/wiki/Comma-separated_values)
- [JSON Format Explanation](https://www.json.org/)

---

### 🔍 Wyszukiwanie Semantyczne vs Słów Kluczowych

**Wyszukiwanie Słów Kluczowych (tradycyjne)**
```
Szukasz: "morderstwo"
Wynik: Tylko filmy zawierające dokładnie słowo "morderstwo"
```

**Wyszukiwanie Semantyczne (ChromaDB)**
```
Szukasz: "morderstwo"
Wynik: Filmy zawierające "morderstwo", "zabójstwo", "zbrodnia", "czyn zły"
       - nawet jeśli nie zawierają dokładnie tego słowa
```

**Dlaczego to lepsze?**
- Bardziej naturalne wyniki
- Rozumie kontekst i znaczenie
- Lepsze rekomendacje

---

## Instalacja WSL na Windows

WSL (Windows Subsystem for Linux) pozwala uruchamiać Linux na Windows bez maszyny wirtualnej.

### Krok 1: Włączenie WSL

1. Otwórz **PowerShell** jako Administrator
   - Kliknij Start
   - Wpisz "PowerShell"
   - Kliknij prawym przyciskiem myszy
   - Wybierz "Uruchom jako administrator"

2. Wpisz polecenie:
```powershell
wsl --install
```

3. Czekaj na instalację (może potrwać kilka minut)

4. Po zakończeniu, **uruchom ponownie komputer**

### Krok 2: Konfiguracja WSL

Po restarcie:

1. Otwórz **PowerShell** ponownie

2. Sprawdź zainstalowane dystrybucje:
```powershell
wsl --list --verbose
```

Powinieneś zobaczyć coś takiego:
```
NAME      STATE           VERSION
Ubuntu    Running         2
```

3. Jeśli Ubuntu nie jest zainstalowany, zainstaluj go:
```powershell
wsl --install -d Ubuntu
```

### Krok 3: Uruchomienie WSL

Otwórz **Windows Terminal** (lub PowerShell) i wpisz:
```powershell
wsl
```

Lub kliknij na Ubuntu w Windows Terminal.

Powinieneś zobaczyć prompt:
```
ubuntu@TWOJA-NAZWA:~$
```

✅ **WSL jest zainstalowany!**

📖 **Więcej informacji:**
- [Microsoft WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)

---

## Instalacja Docker na WSL

### Krok 1: Aktualizacja Pakietów

W WSL (Ubuntu) wpisz:
```bash
sudo apt update
sudo apt upgrade -y
```

### Krok 2: Instalacja Docker

```bash
# Zainstaluj Docker
sudo apt install -y docker.io

# Zainstaluj Docker Compose
sudo apt install -y docker-compose

# Dodaj użytkownika do grupy docker (aby nie używać sudo)
sudo usermod -aG docker $USER

# Aktywuj zmianę grupy
newgrp docker
```

### Krok 3: Weryfikacja Instalacji

```bash
docker --version
docker-compose --version
```

Powinieneś zobaczyć wersje:
```
Docker version 24.x.x
Docker Compose version 2.x.x
```

### Krok 4: Uruchomienie Docker Daemon

```bash
# Uruchom Docker w tle
sudo service docker start

# Sprawdź status
sudo service docker status
```

✅ **Docker jest zainstalowany!**

📖 **Więcej informacji:**
- [Docker Installation on WSL](https://docs.docker.com/desktop/install/windows-install/)
- [Docker Compose Installation](https://docs.docker.com/compose/install/)

---

## Uruchomienie Projektu

### Krok 1: Klonowanie Repozytorium

W WSL:
```bash
# Przejdź do katalogu domowego
cd ~

# Sklonuj projekt
git clone https://github.com/s20522/doProjektu.git

# Przejdź do katalogu projektu
cd doProjektu
```

### Krok 2: Instalacja Zależności Python

```bash
# Zainstaluj pip (jeśli nie masz)
sudo apt install -y python3-pip

# Zainstaluj zależności projektu
pip install -r requirements.txt
```

### Krok 3: Pobranie i Czyszczenie Danych

```bash
# Uruchom skrypt czyszczenia danych
python3 scripts/utils/data_cleaner.py
```

**Co robi ten skrypt?**
- Pobiera dane z HuggingFace (MPST dataset)
- Czyści i normalizuje tekst
- Konwertuje CSV na JSON
- Ekstrakcja tagów i gatunków

**Oczekiwany wynik:**
```
2026-03-24 17:02:00,028 - INFO - Liczba filmów: 14828
2026-03-24 17:02:00,038 - INFO - Gatunki (10):
2026-03-24 17:02:00,038 - INFO -   cult: 2647
2026-03-24 17:02:00,038 - INFO -   comedy: 1859
...
```

⏱️ **Czas wykonania:** ~5-10 minut (zależy od szybkości internetu)

### Krok 4: Uruchomienie Docker

```bash
# Przejdź do katalogu docker
cd docker

# Uruchom usługi
docker-compose up -d
```

**Co się dzieje?**
- Neo4j uruchamia się na porcie 7474
- ChromaDB uruchamia się na porcie 8000
- Ollama uruchamia się na porcie 11434

**Sprawdzenie statusu:**
```bash
docker-compose ps
```

Powinieneś zobaczyć:
```
NAME                COMMAND             STATUS
tmdb-neo4j          "/startup/docker-e…"   Up 2 minutes
tmdb-chromadb       "python -m uvicorn…"   Up 2 minutes
tmdb-ollama         "/bin/ollama serve"     Up 2 minutes
```

### Krok 5: Import Danych do Baz

Wróć do głównego katalogu:
```bash
cd ..
```

Uruchom import:
```bash
python3 scripts/import/run_all_imports.py
```

**Co robi ten skrypt?**
1. Łączy się z Neo4j
2. Tworzy węzły i relacje dla filmów
3. Łączy się z ChromaDB
4. Importuje embeddings streszczeń
5. Wyświetla statystyki

**Oczekiwany wynik:**
```
============================================================
URUCHOMIENIE WSZYSTKICH IMPORTÓW
============================================================

1. IMPORT DO NEO4J
============================================================
✓ Połączenie z Neo4j potwierdzone
✓ Ograniczenie utworzone
✓ Indeks utworzony
Zaimportowano 14828/14828 filmów
✓ Import do Neo4j zakończony pomyślnie

2. IMPORT DO CHROMADB
============================================================
✓ Połączenie z ChromaDB potwierdzone
✓ Kolekcja 'movies' gotowa
Zaimportowano 14828/14828 filmów
✓ Import do ChromaDB zakończony pomyślnie

============================================================
✓ WSZYSTKIE IMPORTY ZAKOŃCZONE POMYŚLNIE
============================================================
```

⏱️ **Czas wykonania:** ~10-20 minut (zależy od wydajności)

### Krok 6: Dostęp do Usług

Teraz możesz uzyskać dostęp do:

**Neo4j Browser:**
- URL: http://localhost:7474
- Login: `neo4j`
- Hasło: `password123`

**ChromaDB API:**
- URL: http://localhost:8000
- Dokumentacja: http://localhost:8000/docs

**Ollama API:**
- URL: http://localhost:11434
- Dostępne modele: http://localhost:11434/api/tags

### Krok 7: Testowanie Neo4j

W Neo4j Browser (http://localhost:7474):

1. Zaloguj się

2. Wpisz w edytorze:
```cypher
MATCH (m:Movie) RETURN m.title, m.genres LIMIT 5
```

3. Kliknij "Run"

Powinieneś zobaczyć 5 filmów z ich gatunkami.

### Krok 8: Testowanie ChromaDB

W terminalu WSL:
```bash
# Wyszukaj filmy podobne do "murder and revenge"
curl -X POST "http://localhost:8000/api/v1/collections/movies/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query_texts": ["murder and revenge"],
    "n_results": 3
  }'
```

Powinieneś zobaczyć 3 filmy podobne do "murder and revenge".

---

## Rozwiązywanie Problemów

### Problem: "docker: command not found"

**Rozwiązanie:**
```bash
sudo apt install -y docker.io
```

### Problem: "Permission denied while trying to connect to Docker daemon"

**Rozwiązanie:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Problem: "Neo4j connection refused"

**Rozwiązanie:**
```bash
# Sprawdź czy Neo4j się uruchomił
docker-compose ps

# Jeśli nie, uruchom go
docker-compose up -d neo4j

# Czekaj 30 sekund na uruchomienie
sleep 30

# Spróbuj ponownie
python3 scripts/import/run_all_imports.py
```

### Problem: "No space left on device"

**Rozwiązanie:**
Projekt potrzebuje ~500 MB wolnego miejsca. Sprawdź:
```bash
df -h
```

---

## Dodatkowe Zasoby

### Dokumentacja Projektów

| Projekt | Link | Opis |
|---------|------|------|
| Neo4j | https://neo4j.com/docs/ | Oficjalna dokumentacja Neo4j |
| ChromaDB | https://docs.trychroma.com/ | Oficjalna dokumentacja ChromaDB |
| Ollama | https://ollama.ai/ | Oficjalna strona Ollama |
| Docker | https://docs.docker.com/ | Oficjalna dokumentacja Docker |
| Python | https://www.python.org/doc/ | Oficjalna dokumentacja Python |

### Kursy Online

| Temat | Link | Poziom |
|-------|------|--------|
| Python dla Początkujących | https://www.codecademy.com/learn/learn-python-3 | Początkujący |
| Docker Basics | https://docker-curriculum.com/ | Początkujący |
| Neo4j Fundamentals | https://neo4j.com/graphacademy/ | Początkujący |
| SQL & Databases | https://www.udemy.com/course/the-complete-sql-bootcamp/ | Początkujący |
| Machine Learning | https://www.coursera.org/learn/machine-learning | Średniozaawansowany |

### Artykuły i Blogi

- [What is a Graph Database?](https://neo4j.com/developer/graph-database/)
- [Understanding Vector Embeddings](https://www.pinecone.io/learn/vector-embeddings/)
- [Docker for Developers](https://www.docker.com/blog/)
- [Python Data Science Guide](https://realpython.com/learning-paths/data-science-python/)

### Narzędzia Pomocnicze

| Narzędzie | Opis | Link |
|-----------|------|------|
| VS Code | Edytor kodu | https://code.visualstudio.com/ |
| Postman | Testowanie API | https://www.postman.com/ |
| Git | Kontrola wersji | https://git-scm.com/ |
| GitHub Desktop | GUI dla Git | https://desktop.github.com/ |

---

## Podsumowanie

Gratulacje! 🎉 Pomyślnie:
1. ✅ Zainstalowałeś WSL na Windows
2. ✅ Zainstalowałeś Docker
3. ✅ Sklonowałeś projekt
4. ✅ Pobrałeś i oczyściłeś dane
5. ✅ Uruchomiłeś Neo4j, ChromaDB i Ollama
6. ✅ Zaimportowałeś 14,828 filmów

Teraz możesz:
- Eksplorować dane w Neo4j Browser
- Wyszukiwać filmy w ChromaDB
- Pisać własne skrypty Python
- Rozszerzać projekt o nowe funkcjonalności

---

## Następne Kroki

1. **Zapoznaj się z Cypher** - język zapytań Neo4j
2. **Eksploruj dane** - spróbuj różnych zapytań
3. **Napisz własny skrypt** - dodaj nową funkcjonalność
4. **Przeczytaj dokumentację** - pogłęb swoją wiedzę
5. **Dołącz do społeczności** - dziel się swoimi projektami

---

## Autor

Tutorial przygotowany przez **Manus AI**.

## Licencja

MIT License - Projekt jest otwarty i dostępny dla wszystkich.
