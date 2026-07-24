"""
============================================================
Retrieval Evaluation Metrics
============================================================

Module  : AI Evaluation Subsystem
Purpose : Standard metrics calculations for Precision@K, Recall@K, and MRR.
"""

from typing import Iterable, Set


class RetrievalMetrics:
    """
    Calculates information retrieval quality metrics.
    """

    @classmethod
    def precision_at_k(cls, retrieved_ids: list[str], relevant_ids: Set[str], k: int) -> float:
        """Calculate Precision@K."""
        if not retrieved_ids or k <= 0:
            return 0.0
        top_k = retrieved_ids[:k]
        hits = sum(1 for cid in top_k if cid in relevant_ids)
        return round(hits / k, 4)

    @classmethod
    def recall_at_k(cls, retrieved_ids: list[str], relevant_ids: Set[str], k: int) -> float:
        """Calculate Recall@K."""
        if not relevant_ids or k <= 0:
            return 0.0
        top_k = retrieved_ids[:k]
        hits = sum(1 for cid in top_k if cid in relevant_ids)
        return round(hits / len(relevant_ids), 4)

    @classmethod
    def mean_reciprocal_rank(cls, retrieved_ids: list[str], relevant_ids: Set[str]) -> float:
        """Calculate Reciprocal Rank (RR)."""
        for rank, cid in enumerate(retrieved_ids, start=1):
            if cid in relevant_ids:
                return round(1.0 / rank, 4)
        return 0.0
