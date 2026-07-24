"""
============================================================
Retrieval Statistics Tracker
============================================================

Module  : AI Retrieval Engine
Purpose : Utility tracking performance statistics across pipeline stages.
"""

import time
from app.ai.retrieval.retrieval_models import RetrievalStatistics, RetrievedChunk


class RetrievalStatisticsTracker:
    """
    Timer and aggregator for RetrievalStatistics metrics.
    """

    def __init__(self):
        self.stats = RetrievalStatistics()

    def calculate_average_similarity(self, chunks: list[RetrievedChunk]) -> float:
        if not chunks:
            return 0.0
        avg = sum(c.similarity_score for c in chunks) / len(chunks)
        return round(avg, 4)
