from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document as LangchainDocument
from typing import List

class VectorStore:
    def __init__(self, embeddings_model: Embeddings, persist_directory: str = "chroma_db"):
        self.embeddings_model = embeddings_model
        self.persist_directory = persist_directory
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings_model
        )

    def add_documents(self, documents: List[LangchainDocument]):
        """
        Adds a list of Langchain Document objects to the ChromaDB collection.
        """
        if not documents:
            return
        
        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to ChromaDB and persisted.")

    def as_retriever(self, search_type="similarity", search_kwargs=None):
        """
        Returns a Langchain retriever object from the vector store.
        """
        if search_kwargs is None:
            search_kwargs = {"k": 5}
        return self.vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

    def get_all_documents(self) -> List[LangchainDocument]:
        """
        Retrieves all documents currently stored in the ChromaDB collection.
        Note: This can be inefficient for very large collections.
        """
        # The .get() method returns a dictionary with 'ids', 'embeddings', 'metadatas', 'documents'
        all_docs_data = self.vector_store.get()
        
        documents = []
        for i in range(len(all_docs_data['ids'])):
            doc = LangchainDocument(
                page_content=all_docs_data['documents'][i],
                metadata=all_docs_data['metadatas'][i]
            )
            documents.append(doc)
        return documents

    @property
    def collection_count(self) -> int:
        """
        Returns the number of documents in the collection.
        """
        return self.vector_store._collection.count()
