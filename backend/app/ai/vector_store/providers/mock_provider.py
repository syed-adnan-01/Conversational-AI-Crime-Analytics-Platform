"""
============================================================
Mock Vector Store Provider
============================================================

Module  : AI Vector Store Layer
Purpose : In-memory cosine-similarity vector store for unit tests.
"""

import math
from typing import Optional

from app.ai.chunking.chunk_models import ContextChunk
from app.ai.embeddings.embedding_models import EmbeddingRecord
from app.ai.vector_store.providers.base import VectorStoreProvider
from app.ai.vector_store.vector_models import SearchFilter, VectorSearchResult


class MockVectorStoreProvider(VectorStoreProvider):
    """
    In-memory mock vector store implementing exact cosine similarity search.
    """
    _store: dict[str, dict] = {}

    def __init__(self):
        pass

    @property
    def provider_name(self) -> str:
        return "mock"

    def upsert(
        self, records: list[EmbeddingRecord], chunks: list[ContextChunk]
    ) -> bool:
        chunk_map = {c.chunk_id: c for c in chunks}
        for rec in records:
            chunk = chunk_map.get(rec.chunk_id)
            if chunk:
                self._store[rec.chunk_id] = {
                    "record": rec,
                    "chunk": chunk,
                    "case_id": chunk.case_id,
                }
        return True

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        raw_cos = dot / (norm1 * norm2)
        # Normalize [-1.0, 1.0] cosine range to [0.0, 1.0] similarity score
        return round((raw_cos + 1.0) / 2.0, 4)

    def search(
        self,
        query_vector: list[float],
        filter_criteria: SearchFilter,
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        results: list[tuple[float, dict]] = []

        for item in self._store.values():
            chunk: ContextChunk = item["chunk"]
            rec: EmbeddingRecord = item["record"]

            # Filter by case_id
            if filter_criteria.case_id and chunk.case_id != filter_criteria.case_id:
                continue

            # Filter by chunk_types
            if filter_criteria.chunk_types and chunk.chunk_type not in filter_criteria.chunk_types:
                continue

            score = self._cosine_similarity(query_vector, rec.vector)
            results.append((score, item))

        # Sort descending by score
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:top_k]

        return [
            VectorSearchResult(
                chunk_id=item["chunk"].chunk_id,
                case_id=item["chunk"].case_id,
                score=score,
                content=item["chunk"].content,
                chunk_type=item["chunk"].chunk_type.value,
                parent_entity_id=item["chunk"].parent_entity_id,
                metadata=item["chunk"].metadata.model_dump(mode="json"),
            )
            for score, item in top_results
        ]

    def delete(self, case_id: str) -> bool:
        to_delete = [cid for cid, val in self._store.items() if val["case_id"] == case_id]
        for cid in to_delete:
            self._store.pop(cid, None)
        return True

    def exists(self, case_id: str) -> bool:
        return any(val["case_id"] == case_id for val in self._store.values())

    def count(self, case_id: Optional[str] = None) -> int:
        if case_id:
            return sum(1 for val in self._store.values() if val["case_id"] == case_id)
        return len(self._store)

    def clear(self) -> bool:
        self._store.clear()
        return True

    def list_all_case_ids(self) -> list[str]:
        return sorted(list({val["case_id"] for val in self._store.values()}))
