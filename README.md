# RAG Pipeline for Open Food Facts

This project implements a Retrieval-Augmented Generation (RAG) pipeline to answer questions about food products. The pipeline is built using Langchain and is exposed through a FastAPI application.

## Features

*   **Langchain-Native Architecture:** The pipeline is built using core Langchain components, including document loaders, text splitters, embedding models, and vector stores.
*   **FastAPI:** A FastAPI application to expose the RAG pipeline's functionality through a simple API, including file uploads for dynamic knowledge base updates.
*   **Multi-file type support:** Utilizes Langchain's document loaders to ingest various file types (e.g., `.txt`, `.pdf`).
*   **Pluggable Embeddings and Vector Stores:** Uses Langchain's `Chroma` vector store and `HuggingFaceBgeEmbeddings`, making it easy to swap with other Langchain-compatible components.
*   **Reranking for Relevance:** Includes a reranking step after retrieval to improve the quality of the context provided to the LLM.
*   **Local LLM Integration:** Integrates with local LLMs via Ollama (e.g., Mistral), making it free to run and keeping data private.

## Project Structure

```
├── api
│   └── main.py         # FastAPI application
├── data                # Optional: Directory for initial documents loaded at startup
├── uploads             # Temporary directory for uploaded files via API
├── src
│   ├── document_processor.py
│   ├── generator.py
│   ├── rag_pipeline.py # Core RAG pipeline logic
│   ├── reranker.py
│   └── vector_store.py
├── venv                # Python virtual environment
├── GEMINI.md
├── requirements.txt
├── TODO.txt
└── README.md
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    ```
    On Windows:
    ```powershell
    .\venv\Scripts\activate
    ```
    On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up a Local LLM with Ollama:**
    This project is configured to use a local LLM running via [Ollama](https://ollama.com/).
    
    a. **Install Ollama:** Follow the instructions on their website to download and install Ollama for your operating system.

    b. **Download the Mistral model:** Once Ollama is running, open your terminal and pull the Mistral model:
    ```bash
    ollama pull mistral
    ```
    Ensure the Ollama application is running in the background before starting the FastAPI server.

## Running the Application

To start the FastAPI server, run the following command from the project's root directory:

```bash
uvicorn api.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger UI documentation at `http://127.0.0.1:8000/docs`.

**Initial Data Loading:** If a `data` directory exists in the project root, the RAG pipeline will attempt to load and index documents from it during startup.

## API Endpoints

The FastAPI server provides the following endpoints:

*   `GET /health`: Health check endpoint to verify API status and RAG pipeline initialization.
*   `POST /query`: Processes a natural language query using the RAG pipeline.
*   `POST /upload_document`: Uploads a document (e.g., `.txt`, `.pdf`), processes it, and adds it to the RAG pipeline's vector store.
*   `GET /documents`: Retrieves basic information about all documents currently indexed in the RAG pipeline's vector store.

### How to Use the API

You can use a tool like `curl` to interact with the API, or the interactive Swagger UI at `http://127.0.0.1:8000/docs`.

**Query Example:**

```bash
curl -X POST "http://127.0.0.1:8000/query" \
-H "Content-Type: application/json" \
-d 
'{ 
  "query": "What are the benefits of olive oil?",
  "top_k": 2
}'
```

**Upload Document Example (using a dummy text file named `my_document.txt`):**

```bash
# First, create a dummy file for testing:
echo "This is a new test document about organic vegetables." > my_document.txt

# Then, upload it:
curl -X POST "http://127.0.0.1:8000/upload_document" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "file=@my_document.txt"
```

**Get All Indexed Documents Example:**

```bash
curl -X GET "http://127.0.0.1:8000/documents"
```