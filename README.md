# Custom Semantic Document Search Engine

A backend application that finds the most relevant text documents for a user query using:

- manual TF-IDF vectorization
- manual cosine similarity
- FastAPI for the API layer

This solution follows the task constraints strictly:

- no pretrained embeddings
- no external NLP APIs
- no `scikit-learn`, `gensim`, `spaCy`, or similar NLP/vectorizer libraries
- all text processing and similarity logic implemented manually in Python

## Features

- `GET /search?q=<query>` returns the top 3 most relevant documents
- `POST /index` rebuilds the document index if files are added or changed
- each result returns:
  - document filename
  - similarity score
  - short snippet

## Tech Stack

- Python
- FastAPI
- Standard Python libraries: `math`, `re`, `collections`, `pathlib`

## Project Structure

```text
custom-semantic-search-engine/
├── app/
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── search_engine.py
│   ├── text_processing.py
│   └── vectorizer.py
├── documents/
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## How It Works

1. The application reads all `.txt` files from the `documents/` folder.
2. Each document is normalized and tokenized using a regex-based tokenizer.
3. TF is calculated manually:

```text
TF(term) = count of term in document / total terms in document
```

4. IDF is calculated manually:

```text
IDF(term) = log((1 + total_documents) / (1 + documents_containing_term)) + 1
```

5. Each document is converted into a TF-IDF vector.
6. The query is converted into the same vector space.
7. Cosine similarity is computed manually between the query vector and each document vector.
8. Results are sorted by score and the top 3 are returned.

## API Endpoints

### `GET /search`

Searches the indexed documents for the given query.

Example:

```http
GET /search?q=artificial intelligence in finance
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
    },
    {
      "document": "banking_automation.txt",
      "score": 0.7458,
      "snippet": "Banks are using automation and machine learning to reduce fraud, improve compliance, and speed up operations."
    },
    {
      "document": "fintech_growth.txt",
      "score": 0.6914,
      "snippet": "Fintech companies use data-driven systems to improve forecasting, lending decisions, and customer experience."
    }
  ]
}
```

### `POST /index`

Rebuilds the document index after files are added, removed, or updated.

Example response:

```json
{
  "indexed_documents": 50,
  "vocabulary_size": 4128,
  "documents_directory": "/absolute/path/to/custom-semantic-search-engine/documents"
}
```

## Local Setup

### 1. Clone or open the project

```bash
cd /path/to/custom-semantic-search-engine
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add documents

Place the given `.txt` files inside:

```text
documents/
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Docker Setup

### Build the image

```bash
docker build -t semantic-search-engine .
```

### Run the container

```bash
docker run -p 8000:8000 semantic-search-engine
```

If you want the container to use your local `documents/` folder directly:

```bash
docker run -p 8000:8000 -v "$(pwd)/documents:/app/documents" semantic-search-engine
```

Then open:

- `http://127.0.0.1:8000/docs`

## Sample API Calls

### Rebuild the index

```bash
curl -X POST "http://127.0.0.1:8000/index"
```

### Search documents

```bash
curl "http://127.0.0.1:8000/search?q=artificial%20intelligence%20in%20finance"
```

## Important Notes

- The search engine indexes only `.txt` files.
- Empty files are skipped.
- If new files are added after startup, call `POST /index` to refresh the corpus.
- The optional UI mentioned in the task is not included, since the backend requirement is fully completed.

## Task Requirement Mapping

- Custom TF-IDF vectorization: completed
- Manual cosine similarity: completed
- Backend in FastAPI: completed
- `/search` endpoint: completed
- Top 3 results with filename, score, snippet: completed
- `/index` bonus endpoint: completed
- Structured modular source code: completed
- README with setup and sample calls: completed

## Interview Summary

You can explain the project like this:

> I built a FastAPI-based document search engine that manually implements TF-IDF and cosine similarity without using external NLP libraries. The system indexes text documents from a local folder, converts both documents and search queries into vectors, compares them using cosine similarity, and returns the top 3 most relevant documents with a score and snippet.
