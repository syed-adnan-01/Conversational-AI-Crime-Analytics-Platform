"""
============================================================
Index Manager
============================================================

Module  : AI Indexing Subsystem
Purpose : Manages indexing lifecycle, context hash change detection,
          redundancy skipping, and chunk-to-vector pipeline.
"""

import time
from datetime import datetime
from typing import Optional

from app.ai.chunking.chunk_builder import ChunkBuilder
from app.ai.config import ai_config
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.indexing.exceptions import IndexingException
from app.ai.indexing.index_models import IndexListResponse, IndexMetadata, IndexStatus
from app.ai.services.context_service import ContextService
from app.ai.vector_store.vector_service import VectorService


class IndexManager:
    """
    Manager orchestrating context-to-vector transformation, change detection,
    and metadata persistence.
    """

    _metadata_store: dict[str, IndexMetadata] = {}

    def __init__(
        self,
        context_service=ContextService,
        chunk_builder=ChunkBuilder,
        embedding_service: Optional[EmbeddingService] = None,
        vector_service: Optional[VectorService] = None,
    ):
        self.context_service = context_service
        self.chunk_builder = chunk_builder
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_service = vector_service or VectorService()

    @classmethod
    def clear_metadata_store(cls) -> None:
        """Clear stored index metadata."""
        cls._metadata_store.clear()

    def get_status(self, case_id: str) -> IndexMetadata:
        """Get index status metadata for a case."""
        if case_id in self._metadata_store:
            return self._metadata_store[case_id]

        # Check if vectors exist in datastore
        if self.vector_service.exists(case_id):
            return IndexMetadata(
                case_id=case_id,
                context_hash="",
                indexed_at=datetime.now(),
                provider=self.embedding_service.provider.provider_name,
                embedding_model=ai_config.EMBEDDING_MODEL_NAME,
                vector_store=self.vector_service.provider.provider_name,
                chunk_count=self.vector_service.count(case_id),
                status=IndexStatus.INDEXED,
            )

        return IndexMetadata(
            case_id=case_id,
            context_hash="",
            provider=self.embedding_service.provider.provider_name,
            embedding_model=ai_config.EMBEDDING_MODEL_NAME,
            vector_store=self.vector_service.provider.provider_name,
            status=IndexStatus.NOT_INDEXED,
        )

    def is_outdated(self, case_id: str) -> bool:
        """Check if case index is outdated compared to current context hash."""
        context = self.context_service.build_context(case_id)
        current_meta = self.get_status(case_id)
        if current_meta.status != IndexStatus.INDEXED:
            return True
        return current_meta.context_hash != context.metadata.context_hash

    def index_case(self, case_id: str, force: bool = False) -> IndexMetadata:
        """
        Build or update vector index for a given case_id.
        Skips indexing if context_hash is unchanged and force=False.
        """
        start_time = time.perf_counter()

        # 1. Fetch current context
        context = self.context_service.build_context(case_id)
        context_hash = context.metadata.context_hash

        existing_meta = self._metadata_store.get(case_id)

        # 2. Skip indexing if hash matches and status is INDEXED
        if (
            not force
            and existing_meta
            and existing_meta.status == IndexStatus.INDEXED
            and existing_meta.context_hash == context_hash
        ):
            return existing_meta

        # 3. Update status to INDEXING
        indexing_meta = IndexMetadata(
            case_id=case_id,
            context_hash=context_hash,
            provider=self.embedding_service.provider.provider_name,
            embedding_model=ai_config.EMBEDDING_MODEL_NAME,
            vector_store=self.vector_service.provider.provider_name,
            status=IndexStatus.INDEXING,
        )
        self._metadata_store[case_id] = indexing_meta

        try:
            # 4. Delete existing vectors for clean re-indexing
            self.vector_service.delete(case_id)

            # 5. Build chunks
            chunks = self.chunk_builder.build_chunks(context)

            # 6. Generate embeddings
            embedding_records = self.embedding_service.generate_embeddings_for_chunks(chunks)

            # 7. Upsert to vector store
            self.vector_service.upsert(embedding_records, chunks)

            # 8. Measure completion duration
            end_time = time.perf_counter()
            duration_ms = round((end_time - start_time) * 1000, 2)

            # 9. Update final INDEXED metadata
            final_meta = IndexMetadata(
                case_id=case_id,
                context_hash=context_hash,
                indexed_at=datetime.now(),
                provider=self.embedding_service.provider.provider_name,
                embedding_model=ai_config.EMBEDDING_MODEL_NAME,
                vector_store=self.vector_service.provider.provider_name,
                embedding_version="1.0.0",
                schema_version="1.0.0",
                index_version="1.0.0",
                chunk_count=len(chunks),
                indexing_duration_ms=duration_ms,
                status=IndexStatus.INDEXED,
            )
            self._metadata_store[case_id] = final_meta
            return final_meta

        except Exception as exc:
            failed_meta = IndexMetadata(
                case_id=case_id,
                context_hash=context_hash,
                provider=self.embedding_service.provider.provider_name,
                embedding_model=ai_config.EMBEDDING_MODEL_NAME,
                vector_store=self.vector_service.provider.provider_name,
                status=IndexStatus.FAILED,
            )
            self._metadata_store[case_id] = failed_meta
            raise IndexingException(f"Failed to index case '{case_id}': {exc}") from exc

    def delete_index(self, case_id: str) -> bool:
        """Delete case vectors and clear metadata."""
        self.vector_service.delete(case_id)
        self._metadata_store.pop(case_id, None)
        return True

    def list_all_indexes(self) -> IndexListResponse:
        """List index status and operational stats for all cases."""
        items = list(self._metadata_store.values())
        total_cases = len(items)
        total_vectors = self.vector_service.count()
        return IndexListResponse(
            total_cases_indexed=total_cases,
            total_vectors_stored=total_vectors,
            items=items,
        )
