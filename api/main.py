from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict
import shutil

# Assuming src is in the PYTHONPATH or relative path is handled
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from rag_pipeline import RAGPipeline

app = FastAPI(title="RAG Pipeline API",
              description="API for Retrieval-Augmented Generation using Open Food Facts documents.",
              version="0.1.0")

# Define a directory for temporary file uploads
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOADS_DIR, exist_ok=True)


# Initialize the RAG pipeline globally to avoid re-initialization on each request
# For API, these paths should be absolute or relative to where the API is run
rag_pipeline = RAGPipeline(chroma_db_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'chroma_db')))

@app.on_event("startup")
async def startup_event():
    """
    Initializes the RAG pipeline when the FastAPI application starts up.
    """
    print("Starting up RAG Pipeline API...")
    try:
        # Initial documents from 'data' directory (if exists)
        initial_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        if os.path.exists(initial_data_path) and os.path.isdir(initial_data_path):
            rag_pipeline.initialize(initial_data_dir=initial_data_path)
        else:
            rag_pipeline.initialize() # Initialize without initial data if directory doesn't exist
        print("RAG Pipeline API started successfully.")
    except Exception as e:
        print(f"Failed to initialize RAG Pipeline: {e}")
        # Depending on desired behavior, might raise HTTPException or handle differently
        # For now, allowing startup even if RAG init fails, but requests will fail.

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.post("/query", response_model=Dict)
async def query_rag(request: QueryRequest):
    """
    Processes a natural language query using the RAG pipeline.
    """
    if not rag_pipeline.initialized:
        raise HTTPException(status_code=503, detail="RAG Pipeline not initialized.")
    try:
        # result contient maintenant {"answer": ..., "sources": ...}
        result = rag_pipeline.query(request.query, request.top_k)
        
        return {
            "query": request.query,
            "response": result["answer"], # La réponse textuelle du LLM
            "sources": result["sources"]  # La liste des documents utilisés (top k)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_document")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document, processes it, and adds it to the RAG pipeline's vector store.
    """
    if not rag_pipeline.initialized:
        raise HTTPException(status_code=503, detail="RAG Pipeline not initialized.")
    
    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOADS_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process and add to RAG pipeline
        success = rag_pipeline.add_document_from_file(file_path)
        
        if success:
            return {"message": f"Document '{file.filename}' uploaded and processed successfully."}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to process document '{file.filename}'.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading or processing file: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/documents", response_model=Dict)
async def get_documents():
    """
    Retrieves basic information about all documents currently indexed in the RAG pipeline's vector store.
    """
    if not rag_pipeline.initialized:
        raise HTTPException(status_code=503, detail="RAG Pipeline not initialized.")
    try:
        indexed_docs = rag_pipeline.get_all_indexed_documents()
        return {"documents": indexed_docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status and RAG pipeline initialization.
    """
    status = "initialized" if rag_pipeline.initialized else "not_initialized"
    return {"status": "ok", "rag_pipeline_status": status}