"""
============================================================
Vector Service Layer
============================================================

Module  : AI Vector Store Layer
Purpose : Service Layer facade for vector store operations.
"""

from typing import Optional

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.config import ai_config
from app.ai.embeddings.embedding_models import EmbeddingRecord
from app.ai.vector_store.exceptions import VectorStoreException
from app.ai.vector_store.providers import (
    ChromaDBProvider,
    MockVectorStoreProvider,
    VectorStoreProvider,
)
from app.ai.vector_store.vector_models import SearchFilter, VectorSearchResult


class VectorService:
    """
    Service Layer wrapping the active VectorStoreProvider implementation.
    """

    def __init__(self, provider: Optional[VectorStoreProvider] = None):
        self.provider = provider or self.resolve_provider()

    @classmethod
    def resolve_provider(cls) -> VectorStoreProvider:
        """Resolve active vector store provider from AIConfig setting."""
        prov = ai_config.VECTOR_STORE_PROVIDER.lower()
        if prov == "chromadb":
            return ChromaDBProvider()
        return MockVectorStoreProvider()

    def upsert(
        self, records: list[EmbeddingRecord], chunks: list[ContextChunk]
    ) -> bool:
        """Upsert vector records and chunk metadata into vector store."""
        try:
            return self.provider.upsert(records, chunks)
        except Exception as exc:
            raise VectorStoreException(f"Failed to upsert vectors: {exc}") from exc

    def search(
        self,
        query_vector: list[float],
        filter_criteria: SearchFilter,
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        """Search vector database."""
        try:
            return self.provider.search(query_vector, filter_criteria, top_k)
        except Exception as exc:
            raise VectorStoreException(f"Vector search failed: {exc}") from exc

    def delete(self, case_id: str) -> bool:
        """Delete all vectors associated with a case_id."""
        try:
            return self.provider.delete(case_id)
        except Exception as exc:
            raise VectorStoreException(f"Failed to delete vectors for case '{case_id}': {exc}") from exc

    def exists(self, case_id: str) -> bool:
        """Check if vectors exist for a case_id."""
        return self.provider.exists(case_id)

    def count(self, case_id: Optional[str] = None) -> int:
        """Return total vector count."""
        return self.provider.count(case_id)

    def clear(self) -> bool:
        """Clear all vectors from store."""
        return self.provider.clear()

    def list_all_case_ids(self) -> list[str]:
        """List distinct indexed case_ids."""
        return self.provider.list_all_case_ids()
