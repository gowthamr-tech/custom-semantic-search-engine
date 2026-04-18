from __future__ import annotations

import math

from app.text_processing import inverse_document_frequency, term_frequency, tokenize


class ManualTfidfVectorizer:
    def __init__(self) -> None:
        self.vocabulary: dict[str, int] = {}
        self.idf: dict[str, float] = {}

    def fit_transform(self, documents: list[str]) -> list[list[float]]:
        tokenized_documents = [tokenize(document) for document in documents]
        self.idf = inverse_document_frequency(tokenized_documents)
        self.vocabulary = {
            term: index for index, term in enumerate(sorted(self.idf.keys()))
        }
        return [self._build_vector(tokens) for tokens in tokenized_documents]

    def transform(self, text: str) -> list[float]:
        tokens = tokenize(text)
        return self._build_vector(tokens)

    def _build_vector(self, tokens: list[str]) -> list[float]:
        vector = [0.0] * len(self.vocabulary)
        tf_values = term_frequency(tokens)

        for term, tf_value in tf_values.items():
            if term not in self.vocabulary:
                continue
            vector[self.vocabulary[term]] = tf_value * self.idf[term]

        return vector


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    if len(vector_a) != len(vector_b) or not vector_a:
        return 0.0

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(value * value for value in vector_a))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b))

    if magnitude_a == 0.0 or magnitude_b == 0.0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)
