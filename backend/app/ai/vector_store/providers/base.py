"""
============================================================
Vector Store Provider Interface
============================================================

Module  : AI Vector Store Layer
Purpose : Abstract base class for vector database providers (ChromaDB, Mock, pgvector, etc.).
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.embeddings.embedding_models import EmbeddingRecord
from app.ai.vector_store.vector_models import SearchFilter, VectorSearchResult


class VectorStoreProvider(ABC):
    """
    Abstract Base Class for vector datastores.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the vector store provider."""
        pass

    @abstractmethod
    def upsert(
        self, records: list[EmbeddingRecord], chunks: list[ContextChunk]
    ) -> bool:
        """Insert or replace vector records and associated chunk metadata."""
        pass

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        filter_criteria: SearchFilter,
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        """Search vector database using cosine/Euclidean similarity."""
        pass

    @abstractmethod
    def delete(self, case_id: str) -> bool:
        """Delete all vectors and metadata for a specific case_id."""
        pass

    @abstractmethod
    def exists(self, case_id: str) -> bool:
        """Check whether vectors exist for a case_id."""
        pass

    @abstractmethod
    def count(self, case_id: Optional[str] = None) -> int:
        """Return count of vectors stored globally or for a specific case_id."""
        pass

    @abstractmethod
    def clear(self) -> bool:
        """Clear all stored vectors."""
        pass

    @abstractmethod
    def list_all_case_ids(self) -> list[str]:
        """List distinct case_ids indexed in the vector store."""
        pass
