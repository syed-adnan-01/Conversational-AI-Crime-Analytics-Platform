"""
============================================================
Score Reranker
============================================================

Module  : AI Rerankers Subsystem
Purpose : Score-based relevance reranking and deduplication.
"""

from app.ai.rerankers.base import BaseReranker
from app.ai.retrieval.retrieval_models import RetrievedChunk


class ScoreReranker(BaseReranker):
    """
    Reranker deduplicating candidate chunks and ordering by composite relevance score.
    """

    @property
    def reranker_name(self) -> str:
        return "ScoreReranker"

    def rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        seen_ids: set[str] = set()
        deduped: list[RetrievedChunk] = []

        for chunk in chunks:
            if chunk.chunk_id in seen_ids:
                continue
            seen_ids.add(chunk.chunk_id)

            # Composite rerank score blending vector similarity and domain entity priority
            priority_weight = chunk.priority / 100.0
            composite_score = round(0.65 * chunk.similarity_score + 0.35 * priority_weight, 4)

            chunk.rerank_score = composite_score
            overall_conf = round((composite_score + chunk.source_reliability) / 2.0, 4)
            chunk.overall_confidence = overall_conf
            chunk.confidence_level = "HIGH" if overall_conf >= 0.8 else ("MEDIUM" if overall_conf >= 0.6 else "LOW")

            deduped.append(chunk)

        deduped.sort(key=lambda c: c.rerank_score, reverse=True)
        return deduped
