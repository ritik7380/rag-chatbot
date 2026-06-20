# RAG Chatbot with FastAPI and Ollama

An AI-powered Retrieval-Augmented Generation (RAG) chatbot built using FastAPI, Ollama, LangChain, and FAISS.

## Features

- PDF Upload & Processing
- Semantic Search using Vector Embeddings
- Retrieval-Augmented Generation (RAG)
- Session-based Chat History
- Local LLM Integration with Ollama (Llama 3)
- FastAPI Backend
- FAISS Vector Database

## Tech Stack

- Python
- FastAPI
- LangChain
- Ollama
- FAISS
- SQLite
- Sentence Transformers

## Installation

```bash
git clone <repo-url>
cd rag-chatbot

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

## API Endpoints

### Upload PDF

```http
POST /upload
```

### Create Session

```http
POST /session/{pdf_id}
```

### Ask Question

```http
GET /ask
```

### Chat History

```http
GET /history/{session_id}
```

## Author

Ritik Kumar Yadav
