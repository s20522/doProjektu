"""
ChromaDB Importer - Import danych filmowych do ChromaDB
Generowanie embeddings dla plot synopsis i tagów
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import requests

# Załadowanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja loggingu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChromaDBImporter:
    """Klasa do importu danych do ChromaDB"""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        """Inicjalizacja klienta ChromaDB"""
        self.base_url = f"http://{host}:{port}"
        self.collection_name = "movies"
        logger.info(f"Połączenie z ChromaDB: {self.base_url}")
    
    def verify_connection(self) -> bool:
        """Weryfikacja połączenia z ChromaDB"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/heartbeat", timeout=5)
            if response.status_code == 200:
                logger.info("✓ Połączenie z ChromaDB potwierdzone")
                return True
        except Exception as e:
            logger.error(f"✗ Błąd połączenia: {e}")
        return False
    
    def get_or_create_collection(self):
        """Pobranie lub utworzenie kolekcji"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/collections",
                json={
                    "name": self.collection_name,
                    "metadata": {"hnsw:space": "cosine"}
                }
            )
            if response.status_code in [200, 201]:
                logger.info(f"✓ Kolekcja '{self.collection_name}' gotowa")
                return True
        except Exception as e:
            logger.debug(f"Kolekcja już istnieje: {e}")
            return True
        return False
    
    def import_movies(self, json_file: str, batch_size: int = 100):
        """Import filmów do ChromaDB"""
        
        logger.info(f"Czytanie pliku: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            movies = json.load(f)
        
        logger.info(f"Liczba filmów do importu: {len(movies)}")
        
        # Przygotowanie danych
        documents = []
        metadatas = []
        ids = []
        
        for movie in movies:
            # Dokument - plot synopsis
            documents.append(movie['plot_synopsis'])
            
            # Metadane
            metadata = {
                'imdb_id': movie['imdb_id'],
                'title': movie['title'],
                'genres': ','.join(movie.get('genres', [])),
                'tags': ','.join(movie.get('tags', [])),
                'synopsis_source': movie['synopsis_source']
            }
            metadatas.append(metadata)
            
            # ID
            ids.append(movie['imdb_id'])
        
        # Import w batchach
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            self._import_batch(batch_docs, batch_meta, batch_ids)
            logger.info(f"Zaimportowano {min(i+batch_size, len(documents))}/{len(documents)} filmów")
        
        logger.info(f"✓ Import do ChromaDB zakończony")
    
    def _import_batch(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Import batcha do ChromaDB"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/collections/{self.collection_name}/add",
                json={
                    "ids": ids,
                    "documents": documents,
                    "metadatas": metadatas
                }
            )
            if response.status_code not in [200, 201]:
                logger.error(f"Błąd importu batcha: {response.text}")
        except Exception as e:
            logger.error(f"Błąd podczas importu batcha: {e}")
    
    def search_movies(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Wyszukiwanie filmów na podstawie zapytania"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/collections/{self.collection_name}/query",
                json={
                    "query_texts": [query],
                    "n_results": n_results
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if data.get('ids') and len(data['ids']) > 0:
                    for i, movie_id in enumerate(data['ids'][0]):
                        result = {
                            'imdb_id': movie_id,
                            'distance': data['distances'][0][i] if data.get('distances') else None,
                            'metadata': data['metadatas'][0][i] if data.get('metadatas') else {}
                        }
                        results.append(result)
                
                return results
        except Exception as e:
            logger.error(f"Błąd wyszukiwania: {e}")
        
        return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Pobranie statystyk kolekcji"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/collections/{self.collection_name}"
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data.get('name'),
                    'count': data.get('metadata', {}).get('count', 0)
                }
        except Exception as e:
            logger.error(f"Błąd pobrania statystyk: {e}")
        
        return {}
    
    def print_statistics(self):
        """Wydrukowanie statystyk"""
        stats = self.get_collection_stats()
        logger.info("\n=== STATYSTYKI CHROMADB ===")
        logger.info(f"Kolekcja: {stats.get('name', 'N/A')}")
        logger.info(f"Liczba dokumentów: {stats.get('count', 'N/A')}")


def main():
    """Główna funkcja"""
    
    # Konfiguracja z zmiennych środowiskowych
    chromadb_host = os.getenv('CHROMADB_HOST', 'localhost')
    chromadb_port = int(os.getenv('CHROMADB_PORT', '8000'))
    
    data_processed_dir = os.getenv('DATA_PROCESSED_DIR', './data/processed')
    batch_size = int(os.getenv('BATCH_SIZE', '100'))
    
    # Inicjalizacja importera
    importer = ChromaDBImporter(chromadb_host, chromadb_port)
    
    try:
        # Weryfikacja połączenia
        if not importer.verify_connection():
            logger.error("Nie można połączyć się z ChromaDB")
            return
        
        # Pobranie lub utworzenie kolekcji
        if not importer.get_or_create_collection():
            logger.error("Nie można utworzyć kolekcji")
            return
        
        # Import filmów
        movies_file = Path(data_processed_dir) / 'movies_all.json'
        if movies_file.exists():
            importer.import_movies(str(movies_file), batch_size=batch_size)
        else:
            logger.error(f"Plik nie znaleziony: {movies_file}")
            return
        
        # Wydrukowanie statystyk
        importer.print_statistics()
        
        # Przykładowe wyszukiwanie
        logger.info("\n=== PRZYKŁADOWE WYSZUKIWANIE ===")
        results = importer.search_movies("murder and revenge", n_results=3)
        for result in results:
            logger.info(f"Film: {result['metadata'].get('title', 'N/A')}")
            logger.info(f"  IMDB ID: {result['imdb_id']}")
            logger.info(f"  Tagi: {result['metadata'].get('tags', 'N/A')}")
        
        logger.info("\n✓ Import do ChromaDB zakończony pomyślnie!")
        
    except Exception as e:
        logger.error(f"Błąd podczas importu: {e}", exc_info=True)


if __name__ == '__main__':
    main()
