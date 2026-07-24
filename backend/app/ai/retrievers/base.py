"""
============================================================
Base Retriever Interface
============================================================

Module  : AI Retrievers Subsystem
Purpose : Abstract base class for candidate retrieval algorithms.
"""

from abc import ABC, abstractmethod
from app.ai.retrieval.retrieval_models import RetrievedChunk, SearchQuery


class BaseRetriever(ABC):
    """
    Abstract Base Class for information retrievers.
    """

    @property
    @abstractmethod
    def retriever_name(self) -> str:
        """Name of the retriever algorithm."""
        pass

    @abstractmethod
    def retrieve(self, query: SearchQuery) -> list[RetrievedChunk]:
        """Execute candidate chunk retrieval for a SearchQuery."""
        pass
