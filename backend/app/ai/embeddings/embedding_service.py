"""
============================================================
Embedding Service
============================================================

Module  : AI Embeddings Layer
Purpose : Service Layer orchestrating embedding generation, caching,
          dimension validation, and provider abstraction.
"""

import hashlib
from datetime import datetime
from typing import Optional

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.config import ai_config
from app.ai.embeddings.embedding_models import EmbeddingRecord
from app.ai.embeddings.exceptions import EmbeddingException
from app.ai.embeddings.providers import (
    EmbeddingProvider,
    GeminiEmbeddingProvider,
    MockEmbeddingProvider,
)


class EmbeddingService:
    """
    Service Layer responsible for generating vector embeddings from ContextChunks.
    Supports provider abstraction, caching, and dimension validation.
    """

    _cache: dict[str, list[float]] = {}

    def __init__(self, provider: Optional[EmbeddingProvider] = None):
        self.provider = provider or self.resolve_provider()

    @classmethod
    def resolve_provider(cls) -> EmbeddingProvider:
        """Resolve active provider based on AIConfig setting."""
        prov = ai_config.EMBEDDING_PROVIDER.lower()
        if prov == "gemini":
            return GeminiEmbeddingProvider()
        return MockEmbeddingProvider()

    @classmethod
    def get_cached_embedding(cls, content_hash: str) -> Optional[list[float]]:
        """Embedding cache lookup hook."""
        return cls._cache.get(content_hash)

    @classmethod
    def cache_embedding(cls, content_hash: str, vector: list[float]) -> None:
        """Cache generated vector embedding."""
        cls._cache[content_hash] = vector

    @classmethod
    def clear_cache(cls) -> None:
        """Clear embedding cache."""
        cls._cache.clear()

    def generate_embedding_for_text(self, text: str) -> list[float]:
        """Generate embedding vector for a single query text."""
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        cached = self.get_cached_embedding(content_hash)
        if cached is not None:
            return cached

        vector = self.provider.embed_text(text)

        # Dimension validation
        if len(vector) != self.provider.dimensions:
            raise EmbeddingException(
                f"Vector dimension mismatch: expected {self.provider.dimensions}, got {len(vector)}"
            )

        self.cache_embedding(content_hash, vector)
        return vector

    def generate_embeddings_for_chunks(
        self, chunks: list[ContextChunk]
    ) -> list[EmbeddingRecord]:
        """
        Generate list of EmbeddingRecord objects for a given list of ContextChunks.
        """
        records: list[EmbeddingRecord] = []

        try:
            for chunk in chunks:
                content_hash = hashlib.sha256(chunk.content.encode("utf-8")).hexdigest()
                cached_vec = self.get_cached_embedding(content_hash)

                if cached_vec is not None:
                    vector = cached_vec
                else:
                    vector = self.provider.embed_text(chunk.content)
                    if len(vector) != self.provider.dimensions:
                        raise EmbeddingException(
                            f"Dimension mismatch for chunk '{chunk.chunk_id}': expected {self.provider.dimensions}, got {len(vector)}"
                        )
                    self.cache_embedding(content_hash, vector)

                records.append(
                    EmbeddingRecord(
                        embedding_id=f"EMB-{chunk.chunk_id}",
                        chunk_id=chunk.chunk_id,
                        vector=vector,
                        model_name=ai_config.EMBEDDING_MODEL_NAME,
                        dimensions=self.provider.dimensions,
                        created_at=datetime.now(),
                    )
                )

            return records

        except Exception as exc:
            raise EmbeddingException(f"Failed to generate chunk embeddings: {exc}") from exc
