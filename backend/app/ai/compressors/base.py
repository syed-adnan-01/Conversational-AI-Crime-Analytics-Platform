"""
============================================================
Base Compressor Interface
============================================================

Module  : AI Compressors Subsystem
Purpose : Abstract base class for context window compression algorithms.
"""

from abc import ABC, abstractmethod
from app.ai.retrieval.retrieval_models import RetrievedChunk


class BaseCompressor(ABC):
    """
    Abstract Base Class for context compressors.
    """

    @property
    @abstractmethod
    def compressor_name(self) -> str:
        """Name of the compressor algorithm."""
        pass

    @abstractmethod
    def compress(
        self, chunks: list[RetrievedChunk], max_chunks: int = 10
    ) -> list[RetrievedChunk]:
        """Compress candidate chunks list to remove redundancy and reduce prompt tokens."""
        pass
