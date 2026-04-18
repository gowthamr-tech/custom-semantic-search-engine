from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from app.config import DOCUMENTS_DIR
from app.models import IndexResponse, SearchResponse, SearchResult
from app.search_engine import SemanticSearchEngine


app = FastAPI(
    title="Custom Semantic Search Engine",
    description="Manual TF-IDF and cosine similarity based document search.",
    version="1.0.0",
)

search_engine = SemanticSearchEngine()


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Semantic search service is running. Use /search?q=your+query or POST /index.",
    }


@app.get("/search", response_model=SearchResponse)
def search(q: str = Query(..., min_length=1, description="Search query")) -> SearchResponse:
    if search_engine.indexed_documents == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No text documents found in {DOCUMENTS_DIR}. Add .txt files and call /index.",
        )

    results = search_engine.search(q)
    return SearchResponse(
        query=q,
        indexed_documents=search_engine.indexed_documents,
        results=[SearchResult(**result) for result in results],
    )


@app.post("/index", response_model=IndexResponse)
def reindex() -> IndexResponse:
    indexed_count = search_engine.index_documents()
    return IndexResponse(
        indexed_documents=indexed_count,
        vocabulary_size=search_engine.vocabulary_size,
        documents_directory=str(DOCUMENTS_DIR),
    )
