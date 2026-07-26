"""Shared text pattern helpers for investigation analysis."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable


_STOPWORDS = {
    "a",
    "an",
    "and",
    "at",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "was",
    "were",
    "with",
    "within",
    "without",
}


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokenize(text: str | None) -> list[str]:
    normalized = normalize_text(text)
    if not normalized:
        return []
    tokens = re.findall(r"[a-z0-9][a-z0-9\-_/]*", normalized)
    return [token for token in tokens if token not in _STOPWORDS and len(token) > 2]


def unique_terms(text: str | None) -> set[str]:
    return set(tokenize(text))


def shared_terms(left: str | None, right: str | None) -> list[str]:
    return sorted(unique_terms(left) & unique_terms(right))


def term_overlap_score(left: str | None, right: str | None) -> float:
    left_terms = unique_terms(left)
    right_terms = unique_terms(right)
    if not left_terms or not right_terms:
        return 0.0
    shared = left_terms & right_terms
    total = max(len(left_terms), len(right_terms))
    return len(shared) / total if total else 0.0


def compact_phrases(texts: Iterable[str | None], limit: int = 6) -> list[str]:
    counter: Counter[str] = Counter()
    for text in texts:
        counter.update(tokenize(text))
    return [term for term, _ in counter.most_common(limit)]
