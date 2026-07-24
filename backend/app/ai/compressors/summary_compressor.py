"""
============================================================
Summary Compressor
============================================================

Module  : AI Compressors Subsystem
Purpose : Context compression algorithm filtering near-duplicate passages.
"""

from app.ai.compressors.base import BaseCompressor
from app.ai.retrieval.retrieval_models import RetrievedChunk


class SummaryCompressor(BaseCompressor):
    """
    Compressor eliminating near-duplicate passages based on word set overlap.
    """

    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold

    @property
    def compressor_name(self) -> str:
        return "SummaryCompressor"

    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    def compress(
        self, chunks: list[RetrievedChunk], max_chunks: int = 10
    ) -> list[RetrievedChunk]:
        compressed: list[RetrievedChunk] = []

        for chunk in chunks:
            is_duplicate = False
            for existing in compressed:
                if (
                    chunk.chunk_type == existing.chunk_type
                    and self._jaccard_similarity(chunk.content, existing.content) >= self.similarity_threshold
                ):
                    is_duplicate = True
                    break

            if not is_duplicate:
                compressed.append(chunk)

            if len(compressed) >= max_chunks:
                break

        return compressed
