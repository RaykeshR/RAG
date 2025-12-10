<div align="center">
  <h1>RAG Pipeline for Open Food Facts</h1>
  <p>
    This project implements a Retrieval-Augmented Generation (RAG) pipeline to answer questions about food products using documents from Open Food Facts.
  </p>
  <p>
    <a href="https://github.com/RaykeshR/RAG"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/RaykeshR/RAG/issues">Report Bug</a>
    ·
    <a href="https://github.com/RaykeshR/RAG/issues">Request Feature</a>
  </p>
</div>

<div align="center">

[![My Skills](https://skillicons.dev/icons?i=py)](https://www.python.org/)
[![My Skills](https://skillicons.dev/icons?i=fastapi)](https://fastapi.tiangolo.com/)
[![My Skills](https://skillicons.dev/icons?i=git)](https://git-scm.com/)
[![My Skills](https://skillicons.dev/icons?i=github)](https://github.com/RaykeshR/RAG)
[![My Skills](https://skillicons.dev/icons?i=md)](https://docs.github.com/fr/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
[![My Skills](https://skillicons.dev/icons?i=vscode)](https://code.visualstudio.com/)

</div>

## Table of Contents
<details>
  <summary>Click to expand</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project
This project implements a Retrieval-Augmented Generation (RAG) pipeline to answer questions about food products using documents from Open Food Facts. The pipeline is built with Python and Langchain, and exposed through a FastAPI application.

The core components of the pipeline are:
*   **Vectorization:** Documents are transformed into vector embeddings.
*   **Vector Storage:** Vectors are stored in a Chroma vector database.
*   **Semantic Search:** User queries are vectorized to perform a similarity search.
*   **Reranking:** Retrieved documents are reranked to improve relevance.
*   **Response Generation:** A Large Language Model (LLM) generates an answer based on the query and retrieved documents.

## Open Food Facts
This project uses data from [Open Food Facts](https://world.openfoodfacts.org/), a free, open, and collaborative database of food products from around the world. The data is used to build the knowledge base of the RAG pipeline, enabling it to answer a wide range of questions about food products, their ingredients, nutritional information, and more.

## Data
You will need to download the Open Food Facts dataset to use this project. You can choose from the following formats:

*   **CSV (Recommended)**: This is a single CSV file containing the entire dataset.
    *   **Link**: [en.openfoodfacts.org.products.csv](https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv)
    *   **Size**: `X.XX` GB (Please update with the correct size)
*   **MongoDB Dump (for advanced users)**: This is a compressed archive of the MongoDB database. You can extract it with WinRAR or `tar`.
    *   **Link**: [openfoodfacts-mongodb-dump.tar.gz](https://static.openfoodfacts.org/data/openfoodfacts-mongodbdump.tar.gz)
    *   **Size**: `X.XX` GB (Please update with the correct size)

Once downloaded, place the data in the `data` directory.

### Built With
*   [Python](https://www.python.org/)
*   [FastAPI](https://fastapi.tiangolo.com/)
*   [Langchain](https://www.langchain.com/)
*   [Chroma](https://www.trychroma.com/)
*   [Ollama](https://ollama.com/)

## Getting Started
<details>
<summary>Click to expand</summary>

To get a local copy up and running follow these simple steps.

### Prerequisites
*   Python 3.8+
*   [Ollama](https://ollama.com/) installed and running.

<details>
<summary>Création d'environnements virtuels : </summary>

## Un package manquant : 
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
```
.venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

### 1. Cloner le Repo

avec GitHub (Copie les fichiers localement)

### 2. `python -m venv .venv`

peut nécessiter le passage par CMD (Crée le Dossier .venv)

### 3. `.venv\Scripts\activate`
 

Créer un environnement virtuel Python (Sur Linux/Mac) :
```bash
source venv/bin/activate  # Sur Linux/Mac
```

Lancer avec le CMD peut éviter les erreurs. (Lance l'environnement virtuel)
EN ADMIN : `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned` en cas d'erreur
([détail](https://tutorial.djangogirls.org/fr/django_installation/))

Résultat : 

$\color{rgba(100,255,100, 0.75)}{\textsf{(.venv)}}$ PS C:\Users...\Portfolio_Django> |

On peut aussi (Si c'est un problème de l'éditeur) `$ . .venv\Scripts\activate.ps1`
(lance l'environnement virtuel)

### 4. `python -m pip install --upgrade pip`

(met à jour pip)

### 5. `python -m pip install -r requirements.txt`

```pip freeze > requirements.txt``` pour remplir automatiquement les requirements

Pour toutes les étapes précédentes (sur CMD ou powershell>=7) : 


```
python -m venv .venv && .venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

en cas d'erreur (supprimer le dossier .venv ou lancer): 

```.venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt```

Avec  pip freeze  :

    Pour toutes les étapes précédentes (sur CMD ou powershell>=7) : 
    ```python -m venv .venv && .venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt && pip freeze > requirements.txt```
    
    en cas d'erreur (supprimer le dossier .venv ou lancer): 
    ```.venv\Scripts\activate && python -m pip install --upgrade pip && python -m pip install -r requirements.txt && pip freeze > requirements.txt```
    
### 6. Modifier .git\info\exclude 

Ajouter : `.venv`
(Ne prend pas en compte la modification du dossier .venv)

### 7. Lancer le serveur FastAPI 

```bash
uvicorn api.main:app --reload
```
(Lance le fichier serveur principal avec python)

### Linux/Mac :

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```
Modifier .git\info\exclude 

</details>

### Download Mistral Model
1.  Download the Mistral model with Ollama:
    ```bash
    ollama pull mistral
    ```

</details>

## Usage
<details>
<summary>Click to expand</summary>

To start the FastAPI server, run the following command from the project's root directory:
```bash
uvicorn api.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger UI documentation at `http://127.0.0.1:8000/docs`.
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### API Endpoints
*   `GET /health`: Health check endpoint.
*   `POST /query`: Processes a natural language query.
*   `POST /upload_document`: Uploads a document to the knowledge base.
*   `GET /documents`: Retrieves information about indexed documents.

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

**Upload Document Example:**
```bash
curl -X POST "http://127.0.0.1:8000/upload_document" \
-H "Content-Type: multipart/form-data" \
-F "file=@my_document.txt"
```
</details>



## Project Structure
<details>
<summary>Click to expand</summary>

```
├── api
│   └── main.py
├── data
├── uploads
├── src
│   ├── document_processor.py
│   ├── generator.py
│   ├── rag_pipeline.py
│   ├── reranker.py
│   └── vector_store.py
├── venv
├── GEMINI.md
├── requirements.txt
├── TODO.txt
└── README.md
```
</details>

## Roadmap
- [ ] Add support for more document types.
- [ ] Implement a more advanced reranking model.
- [ ] Add user authentication.
- [ ] Create a web interface for easier interaction.

See the [open issues](https://github.com/RaykeshR/RAG/issues) for a full list of proposed features (and known issues).

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact
Project Link: [https://github.com/RaykeshR/RAG](https://github.com/RaykeshR/RAG)

## Acknowledgments
*   [Open Food Facts](https://world.openfoodfacts.org/)
*   [Langchain](https://www.langchain.com/)
*   [Best-README-Template](https://github.com/othneildrew/Best-README-Template)