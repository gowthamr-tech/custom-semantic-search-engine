import math
import re
from collections import Counter


TOKEN_PATTERN = re.compile(r"\b[a-z0-9]+\b")


def normalize_text(text: str) -> str:
    return text.lower()


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    return TOKEN_PATTERN.findall(normalized)


def term_frequency(tokens: list[str]) -> dict[str, float]:
    if not tokens:
        return {}

    counts = Counter(tokens)
    total_tokens = len(tokens)
    return {term: count / total_tokens for term, count in counts.items()}


def inverse_document_frequency(
    document_tokens: list[list[str]],
) -> dict[str, float]:
    total_documents = len(document_tokens)
    if total_documents == 0:
        return {}

    document_counts: Counter[str] = Counter()
    for tokens in document_tokens:
        document_counts.update(set(tokens))

    return {
        term: math.log((1 + total_documents) / (1 + count)) + 1.0
        for term, count in document_counts.items()
    }

