"""
============================================================
Base Reranker Interface
============================================================

Module  : AI Rerankers Subsystem
Purpose : Abstract base class for chunk reranking algorithms.
"""

from abc import ABC, abstractmethod
from app.ai.retrieval.retrieval_models import RetrievedChunk


class BaseReranker(ABC):
    """
    Abstract Base Class for context rerankers.
    """

    @property
    @abstractmethod
    def reranker_name(self) -> str:
        """Name of the reranker algorithm."""
        pass

    @abstractmethod
    def rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """Rerank candidate chunks in-place or return reordered list."""
        pass
