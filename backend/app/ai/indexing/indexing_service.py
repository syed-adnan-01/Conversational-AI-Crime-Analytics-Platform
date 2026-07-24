"""
============================================================
Indexing Service Layer
============================================================

Module  : AI Indexing Subsystem
Purpose : High-level Service Layer orchestrating case indexing,
          search execution, and index management.
"""

from typing import Optional

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.indexing.index_manager import IndexManager
from app.ai.indexing.index_models import IndexListResponse, IndexMetadata
from app.ai.vector_store.vector_models import (
    VectorSearchRequest,
    VectorSearchResult,
)
from app.ai.vector_store.vector_service import VectorService


class IndexingService:
    """
    Service Layer providing unified facade for index operations,
    plain text semantic search, and status tracking.
    """

    def __init__(
        self,
        manager: Optional[IndexManager] = None,
        embedding_service: Optional[EmbeddingService] = None,
        vector_service: Optional[VectorService] = None,
    ):
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_service = vector_service or VectorService()
        self.manager = manager or IndexManager(
            embedding_service=self.embedding_service,
            vector_service=self.vector_service,
        )

    @classmethod
    def index_case(cls, case_id: str, force: bool = False) -> IndexMetadata:
        """Build or update vector index for a case."""
        svc = cls()
        return svc.manager.index_case(case_id=case_id, force=force)

    @classmethod
    def reindex_case(cls, case_id: str) -> IndexMetadata:
        """Force rebuild case index."""
        svc = cls()
        return svc.manager.index_case(case_id=case_id, force=True)

    @classmethod
    def delete_index(cls, case_id: str) -> bool:
        """Delete case index."""
        svc = cls()
        return svc.manager.delete_index(case_id=case_id)

    @classmethod
    def get_status(cls, case_id: str) -> IndexMetadata:
        """Get index status metadata for a case."""
        svc = cls()
        return svc.manager.get_status(case_id=case_id)

    @classmethod
    def is_outdated(cls, case_id: str) -> bool:
        """Check if case index is outdated."""
        svc = cls()
        return svc.manager.is_outdated(case_id=case_id)

    @classmethod
    def list_indexes(cls) -> IndexListResponse:
        """List operational index status for all cases."""
        svc = cls()
        return svc.manager.list_all_indexes()

    @classmethod
    def search(cls, request: VectorSearchRequest) -> list[VectorSearchResult]:
        """
        Execute semantic vector search. Accepts plain text string query or pre-computed embedding vector.
        """
        svc = cls()

        # 1. Resolve query vector from plain text if supplied
        if request.query_vector:
            query_vector = request.query_vector
        elif request.query:
            query_vector = svc.embedding_service.generate_embedding_for_text(request.query)
        else:
            raise ValueError("Search request must contain either 'query' text or 'query_vector'")

        # 2. Execute vector search via VectorService
        return svc.vector_service.search(
            query_vector=query_vector,
            filter_criteria=request.filter,
            top_k=request.top_k,
        )
