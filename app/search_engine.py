from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import DOCUMENTS_DIR, SNIPPET_LENGTH, TOP_K_RESULTS
from app.vectorizer import ManualTfidfVectorizer, cosine_similarity


@dataclass
class IndexedDocument:
    filename: str
    path: Path
    content: str
    vector: list[float]

    @property
    def snippet(self) -> str:
        lines = [line.strip() for line in self.content.splitlines() if line.strip()]
        if len(lines) >= 2:
            snippet = " ".join(lines[:2])
        else:
            snippet = self.content.strip().replace("\n", " ")
        return snippet[:SNIPPET_LENGTH]


class SemanticSearchEngine:
    def __init__(self, documents_dir: Path = DOCUMENTS_DIR) -> None:
        self.documents_dir = documents_dir
        self.vectorizer = ManualTfidfVectorizer()
        self.documents: list[IndexedDocument] = []
        self.index_documents()

    def index_documents(self) -> int:
        if not self.documents_dir.exists():
            self.documents_dir.mkdir(parents=True, exist_ok=True)
            self.documents = []
            self.vectorizer = ManualTfidfVectorizer()
            return 0

        document_paths = sorted(self.documents_dir.glob("*.txt"))
        raw_documents: list[tuple[Path, str]] = []

        for path in document_paths:
            content = path.read_text(encoding="utf-8", errors="ignore").strip()
            if content:
                raw_documents.append((path, content))

        self.vectorizer = ManualTfidfVectorizer()
        vectors = self.vectorizer.fit_transform([content for _, content in raw_documents])
        self.documents = [
            IndexedDocument(
                filename=path.name,
                path=path,
                content=content,
                vector=vector,
            )
            for (path, content), vector in zip(raw_documents, vectors)
        ]
        return len(self.documents)

    def search(self, query: str, top_k: int = TOP_K_RESULTS) -> list[dict[str, float | str]]:
        cleaned_query = query.strip()
        if not cleaned_query or not self.documents:
            return []

        query_vector = self.vectorizer.transform(cleaned_query)
        scored_results: list[dict[str, float | str]] = []

        for document in self.documents:
            score = cosine_similarity(query_vector, document.vector)
            if score <= 0:
                continue
            scored_results.append(
                {
                    "document": document.filename,
                    "score": round(score, 4),
                    "snippet": document.snippet,
                }
            )

        scored_results.sort(key=lambda item: item["score"], reverse=True)
        return scored_results[:top_k]

    @property
    def indexed_documents(self) -> int:
        return len(self.documents)

    @property
    def vocabulary_size(self) -> int:
        return len(self.vectorizer.vocabulary)
