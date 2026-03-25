# ⚡ Quick Start - Szybki Start

Jeśli już masz WSL i Docker zainstalowany, użyj tego przewodnika.

## 1️⃣ Klonuj Projekt

```bash
cd ~
git clone https://github.com/s20522/doProjektu.git
cd doProjektu
```

## 2️⃣ Zainstaluj Zależności

```bash
pip install -r requirements.txt
```

## 3️⃣ Pobierz i Oczyść Dane

```bash
python3 scripts/utils/data_cleaner.py
```

⏱️ Czeka: ~5-10 minut

## 4️⃣ Uruchom Docker

```bash
cd docker
docker-compose up -d
cd ..
```

⏱️ Czeka: ~2 minuty

## 5️⃣ Importuj Dane

```bash
python3 scripts/import/run_all_imports.py
```

⏱️ Czeka: ~10-20 minut

## 6️⃣ Otwórz Neo4j Browser

Przejdź do: http://localhost:7474

Login: `neo4j`
Hasło: `password123`

## 7️⃣ Testuj Zapytania

W Neo4j Browser wpisz:

```cypher
MATCH (m:Movie) RETURN m.title, m.genres LIMIT 5
```

## ✅ Gotowe!

Projekt jest uruchomiony. Teraz możesz:
- Eksplorować dane w Neo4j
- Wyszukiwać w ChromaDB
- Pisać własne skrypty

---

## Przydatne Polecenia

```bash
# Sprawdź status Docker
docker-compose ps

# Zatrzymaj Docker
docker-compose down

# Uruchom ponownie
docker-compose up -d

# Pokaż logi
docker-compose logs -f

# Wejdź do kontenera
docker-compose exec neo4j bash
```

---

## Potrzebujesz Pomocy?

Przeczytaj [TUTORIAL.md](TUTORIAL.md) dla pełnych wyjaśnień.
