"""
============================================================
Diversity Reranker
============================================================

Module  : AI Rerankers Subsystem
Purpose : Diversity-aware reranking to prevent single entity type saturation.
"""

from app.ai.rerankers.base import BaseReranker
from app.ai.rerankers.score_reranker import ScoreReranker
from app.ai.retrieval.retrieval_models import RetrievedChunk


class DiversityReranker(BaseReranker):
    """
    Reranker selecting diverse candidate chunks across different domain entity types.
    """

    def __init__(self, max_per_type: int = 3):
        self.max_per_type = max_per_type
        self._score_reranker = ScoreReranker()

    @property
    def reranker_name(self) -> str:
        return "DiversityReranker"

    def rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        scored_chunks = self._score_reranker.rerank(query, chunks)

        type_counts: dict[str, int] = {}
        diverse_chunks: list[RetrievedChunk] = []
        overflow_chunks: list[RetrievedChunk] = []

        for chunk in scored_chunks:
            ctype = chunk.chunk_type
            cnt = type_counts.get(ctype, 0)

            if cnt < self.max_per_type:
                type_counts[ctype] = cnt + 1
                diverse_chunks.append(chunk)
            else:
                overflow_chunks.append(chunk)

        # Append remaining overflow chunks if total is small
        return diverse_chunks + overflow_chunks
