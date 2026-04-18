# Custom Semantic Search Engine

This project implements a semantic-style document search backend using:

- Manual TF-IDF vectorization
- Manual cosine similarity
- FastAPI for the backend API

It does not use pretrained embeddings, external NLP APIs, or vectorizer libraries such as `scikit-learn`, `gensim`, or `spaCy`.

## Features

- `GET /search?q=<query>` returns the top 3 most relevant documents
- `POST /index` rebuilds the document index when new files are added
- Returns:
  - document filename
  - similarity score
  - document snippet

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
├── requirements.txt
└── README.md
```

## How It Works

1. All `.txt` files inside `/documents` are loaded.
2. Each document is tokenized with a simple regex tokenizer.
3. TF is calculated manually using term counts divided by total token count.
4. IDF is calculated manually using:

```text
idf(term) = log((1 + total_documents) / (1 + documents_with_term)) + 1
```

5. Each document is converted into a TF-IDF vector.
6. The query is converted into the same vector space.
7. Cosine similarity is computed manually between the query and every document.
8. Results are ranked by score and the top 3 are returned.

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add documents

Place your `.txt` files inside:

```text
documents/
```

Example:

```text
documents/finance_ai.txt
documents/healthcare_ml.txt
documents/climate_data.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

The server will run at:

```text
http://127.0.0.1:8000
```

## API Usage

### Search

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
      "snippet": "AI systems are transforming investment research by automating market analysis and identifying patterns in large financial datasets."
    },
    {
      "document": "banking_automation.txt",
      "score": 0.7458,
      "snippet": "Financial institutions use intelligent automation to process documents, detect fraud, and improve customer support."
    },
    {
      "document": "fintech_innovation.txt",
      "score": 0.6914,
      "snippet": "Modern fintech platforms combine data engineering and machine learning to deliver faster risk modeling and portfolio insights."
    }
  ]
}
```

### Rebuild the index

```bash
curl -X POST "http://127.0.0.1:8000/index"
```

Example response:

```json
{
  "indexed_documents": 50,
  "vocabulary_size": 4128,
  "documents_directory": "/absolute/path/to/custom-semantic-search-engine/documents"
}
```

## Notes for Interview

- TF-IDF is implemented manually in `app/text_processing.py` and `app/vectorizer.py`
- Cosine similarity is implemented manually in `app/vectorizer.py`
- The search logic and ranking are implemented in `app/search_engine.py`
- The API layer is implemented in `app/main.py`
- The code is modular so it is easy to explain during an interview

## Suggested Interview Explanation

You can describe the solution like this:

> "I built a backend service in FastAPI that reads text files from a local folder, manually computes TF-IDF vectors for every document, converts the user query into the same vector space, and ranks documents using a cosine similarity function that I implemented from scratch. I also added a reindexing endpoint so the corpus can be refreshed without changing the code."

