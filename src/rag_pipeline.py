import os
import shutil
from document_processor import DocumentProcessor
from vector_store import VectorStore
from reranker import Reranker
from generator import Generator
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document as LangchainDocument

class RAGPipeline:
    def __init__(self, chroma_db_path: str = "chroma_db", embedding_model_name="BAAI/bge-small-en-v1.5"):
        self.chroma_db_path = chroma_db_path
        
        # 1. Embeddings Model
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        self.embeddings_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        
        # 2. Vector Store
        self.vector_store = VectorStore(
            embeddings_model=self.embeddings_model,
            persist_directory=self.chroma_db_path
        )
        
        # 3. Document Processor
        self.document_processor = DocumentProcessor()
        
        # 4. Reranker
        self.reranker = Reranker()
        
        # 5. Generator
        self.generator = Generator()
        
        self.initialized = False

    def initialize(self, initial_data_dir: str = None):
        """
        Initializes the RAG pipeline. Loads initial documents if a directory is provided.
        """
        if self.initialized:
            print("RAG pipeline already initialized.")
            return

        print("Initializing RAG pipeline...")
        
        if initial_data_dir and not self.vector_store.collection_count:
            print(f"Vector store is empty. Loading initial documents from {initial_data_dir}...")
            chunks = self.document_processor.load_and_chunk_directory(initial_data_dir)
            if chunks:
                self.vector_store.add_documents(chunks)
                print(f"Added {len(chunks)} initial documents to vector store.")
            else:
                print("No initial documents found or processed.")
        elif self.vector_store.collection_count:
            print(f"Vector store already contains {self.vector_store.collection_count} documents. Skipping initial document load.")
        
        self.initialized = True
        print("RAG pipeline initialized successfully.")

    def query(self, query_text: str, top_k: int = 3):
        """
        Runs a single query through the RAG pipeline.
        """
        if not self.initialized:
            raise RuntimeError("RAG pipeline not initialized. Call .initialize() first.")

        print(f"\nProcessing query: '{query_text}'")

        # 1. Retrieve
        retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k * 2})
        retrieved_docs = retriever.invoke(query_text)
        print(f"Retrieved {len(retrieved_docs)} documents.")

        if not retrieved_docs:
            return self.generator.generate_response(query_text, [])

        # 2. Rerank
        reranked_docs = self.reranker.rerank(query_text, retrieved_docs)[:top_k]
        print(f"Reranked and selected top {len(reranked_docs)} documents.")
        
        # Convert LangchainDocument objects to dictionaries for the generator
        docs_for_generator = [{"content": doc.page_content, "metadata": doc.metadata} for doc in reranked_docs]

        # 3. Generate
        final_response = self.generator.generate_response(query_text, docs_for_generator)
        return final_response

    def add_document_from_file(self, file_path: str):
        """
        Loads, chunks, and adds a document from a specified file path to the vector store.
        """
        if not self.initialized:
            raise RuntimeError("RAG pipeline not initialized. Call .initialize() first.")
        
        print(f"Adding document from file: {file_path}")
        chunks = self.document_processor.load_and_chunk_file(file_path)
        if chunks:
            self.vector_store.add_documents(chunks)
            print(f"Added {len(chunks)} chunks from '{file_path}' to vector store.")
            return True
        else:
            print(f"No chunks processed from '{file_path}'.")
            return False

    def get_all_indexed_documents(self):
        """
        Retrieves basic information about all documents currently indexed in the vector store.
        """
        if not self.initialized:
            raise RuntimeError("RAG pipeline not initialized. Call .initialize() first.")
        
        all_docs = self.vector_store.get_all_documents()
        # Convert LangchainDocument objects to a serializable format for the API
        return [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in all_docs
        ]

