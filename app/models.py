from __future__ import annotations

from pydantic import BaseModel


class SearchResult(BaseModel):
    document: str
    score: float
    snippet: str


class SearchResponse(BaseModel):
    query: str
    indexed_documents: int
    results: list[SearchResult]


class IndexResponse(BaseModel):
    indexed_documents: int
    vocabulary_size: int
    documents_directory: str
