from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document as LangchainDocument
from typing import List
import hashlib  # <--- AJOUT : Nécessaire pour le hachage

class VectorStore:
    def __init__(self, embeddings_model: Embeddings, persist_directory: str = "chroma_db"):
        self.embeddings_model = embeddings_model
        self.persist_directory = persist_directory
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings_model
        )

    # --- MODIFICATION DE CETTE MÉTHODE POUR PRÉVENIR LES DOUBLONS ---
    def add_documents(self, documents: List[LangchainDocument]):
        """
        Adds a list of Langchain Document objects to the ChromaDB collection.
        Uses content hash as ID to prevent duplicates.
        """
        if not documents:
            return
        
        # Générer des IDs uniques basés sur le contenu du document
        # Si le même contenu est ajouté à nouveau, il écrasera l'existant (ou sera ignoré) au lieu de créer un doublon.
        ids = [hashlib.md5(doc.page_content.encode('utf-8')).hexdigest() for doc in documents]
        
        self.vector_store.add_documents(documents=documents, ids=ids)
        print(f"Added {len(documents)} documents to ChromaDB and persisted.")

    def as_retriever(self, search_type="similarity", search_kwargs=None):
        if search_kwargs is None:
            search_kwargs = {"k": 5}
        return self.vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

    def get_all_documents(self) -> List[LangchainDocument]:
        all_docs_data = self.vector_store.get()
        documents = []
        # Vérification de sécurité si la liste est vide
        if not all_docs_data['ids']:
            return []
            
        for i in range(len(all_docs_data['ids'])):
            # Parfois 'documents' peut être None dans Chroma si on ne demande que les embeddings, 
            # mais .get() par défaut renvoie tout.
            content = all_docs_data['documents'][i] if all_docs_data['documents'] else ""
            meta = all_docs_data['metadatas'][i] if all_docs_data['metadatas'] else {}
            
            doc = LangchainDocument(
                page_content=content,
                metadata=meta
            )
            documents.append(doc)
        return documents

    @property
    def collection_count(self) -> int:
        return self.vector_store._collection.count()

    # --- AJOUT DE CETTE NOUVELLE MÉTHODE ---
    def remove_duplicates(self):
        """
        Scans the existing database and removes duplicate documents based on content hash.
        """
        print("Scanning vector store for duplicates...")
        # Récupère tous les documents existants
        all_docs = self.vector_store.get()
        
        if not all_docs['ids']:
            print("Vector store is empty.")
            return

        ids = all_docs['ids']
        documents = all_docs['documents']
        
        unique_hashes = set()
        ids_to_delete = []
        
        for i, doc_content in enumerate(documents):
            # Crée un hash unique du contenu
            if doc_content:
                doc_hash = hashlib.md5(doc_content.encode('utf-8')).hexdigest()
            else:
                continue # Ignore les documents vides

            if doc_hash in unique_hashes:
                # Si on a déjà vu ce hash, c'est un doublon
                ids_to_delete.append(ids[i])
            else:
                unique_hashes.add(doc_hash)
        
        if ids_to_delete:
            print(f"Found {len(ids_to_delete)} duplicates. Deleting...")
            self.vector_store.delete(ids=ids_to_delete)
            print(f"Successfully removed {len(ids_to_delete)} duplicate documents.")
        else:
            print("No duplicates found.")