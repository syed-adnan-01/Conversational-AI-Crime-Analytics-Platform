"""
============================================================
Mock Embedding Provider
============================================================

Module  : AI Embeddings Layer
Purpose : Deterministic pseudo-random embedding generator for fast unit tests.
"""

import hashlib
import math
import random
from app.ai.config import ai_config
from app.ai.embeddings.providers.base import EmbeddingProvider


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Mock embedding provider generating unit-normalized deterministic vectors.
    """

    def __init__(self, dims: int = ai_config.EMBEDDING_DIMENSIONS):
        self._dims = dims

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def dimensions(self) -> int:
        return self._dims

    def _generate_vector(self, text: str) -> list[float]:
        seed_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        seed = int(seed_hash[:16], 16)
        rng = random.Random(seed)

        raw = [rng.uniform(-1.0, 1.0) for _ in range(self._dims)]
        norm = math.sqrt(sum(x * x for x in raw)) or 1.0
        return [round(x / norm, 6) for x in raw]

    def embed_text(self, text: str) -> list[float]:
        return self._generate_vector(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._generate_vector(t) for t in texts]
