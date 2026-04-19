# Semantic Document Search Engine

This project is a small backend application built with FastAPI. It searches a folder of text documents and returns the top 3 most relevant files for a user query.

The search logic is implemented manually using:

- TF-IDF vectorization
- cosine similarity

No external NLP libraries like `scikit-learn`, `gensim`, `spaCy`, or pretrained embeddings are used.

## Project Structure

```text
custom-semantic-search-engine/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── search_engine.py
│   ├── text_processing.py
│   └── vectorizer.py
├── documents/
├── requirements.txt
├── Dockerfile
└── README.md
```

## How It Works

1. Read all `.txt` files from the `documents/` folder.
2. Tokenize the text using Python `re`.
3. Calculate TF manually for each term.
4. Calculate IDF manually across all documents.
5. Build TF-IDF vectors for documents and the query.
6. Compute cosine similarity between the query and each document.
7. Sort by score and return the top 3 matches.

## API Endpoints

### `GET /search?q=<query>`

Searches the indexed documents and returns the top 3 results.

Example:

```bash
curl "http://127.0.0.1:8000/search?q=artificial%20intelligence%20in%20finance"
```

Example response:

```json
{
  "query": "artificial intelligence in finance",
  "indexed_documents": 50,
  "results": [
    {
      "document": "finance_ai.txt",
      "score": 0.8721,
      "snippet": "AI systems are transforming investment research by automating market analysis and identifying patterns in financial data."
    }
  ]
}
```

### `POST /index`

Rebuilds the index after documents are added, removed, or updated.

Example:

```bash
curl -X POST "http://127.0.0.1:8000/index"
```

## Run Locally

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add documents

Put the `.txt` files inside the `documents/` folder.

### 4. Start the server

```bash
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`

## Run with Docker

Build:

```bash
docker build -t semantic-search-engine .
```

Run:

```bash
docker run -p 8000:8000 semantic-search-engine
```

If you want to use your local `documents/` folder:

```bash
docker run -p 8000:8000 -v "$(pwd)/documents:/app/documents" semantic-search-engine
```

## Notes

- Only `.txt` files are indexed.
- Empty files are skipped.
- If you change the document folder after the server starts, call `POST /index`.
- The main logic is in `app/text_processing.py`, `app/vectorizer.py`, and `app/search_engine.py`.
