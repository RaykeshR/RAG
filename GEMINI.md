# Gemini Project: RAG Pipeline for Open Food Facts

## Project Overview

This project aims to build a Retrieval-Augmented Generation (RAG) pipeline in Python. The pipeline will process documents from Open Food Facts to answer user queries.

The core components of the pipeline are:

*   **Vectorization:** Documents from Open Food Facts will be transformed into vector embeddings using a model like BGE-M3.
*   **Vector Storage:** The generated vectors will be stored in a vector database such as Elasticsearch or Chroma.
*   **Semantic Search:** When a user asks a question, the query will be vectorized and used to perform a top-k similarity search in the vector database.
*   **Reranking:** The retrieved documents will be reranked to improve relevance.
*   **Response Generation:** The user's query and the relevant document chunks will be fed to a Large Language Model (LLM) to generate a final answer.

## Building and Running

### 1. Setup

It is recommended to use a Python virtual environment.

```bash
python -m venv venv
source venv/bin/activate # on Windows use `venv\Scripts\activate`
```

### 2. Installation

Install the required dependencies from `requirements.txt` (this file will need to be created).

```bash
# TODO: Create requirements.txt
pip install -r requirements.txt
```

### 3. Running the application

```bash
# TODO: Create the main application script
python main.py
```

## Development Conventions

*   All code should be written in Python.
*   A virtual environment should be used to manage project dependencies.
*   Dependencies should be listed in a `requirements.txt` file.
