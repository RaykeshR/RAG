import sys
import os

# 1. Ajouter le dossier 'src' au chemin de recherche (PYTHONPATH)
# Cela permet à Python de trouver 'rag_pipeline', 'document_processor', etc.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 2. Importer depuis 'rag_pipeline' (maintenant accessible directement)
from rag_pipeline import RAGPipeline

def clean():
    print("Initialisation du pipeline...")
    # On s'assure d'utiliser le chemin relatif correct pour la DB depuis la racine
    pipeline = RAGPipeline(chroma_db_path="chroma_db")
    
    print("Lancement du nettoyage...")
    pipeline.vector_store.remove_duplicates()

if __name__ == "__main__":
    clean()