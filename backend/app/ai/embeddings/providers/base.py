"""
============================================================
Embedding Provider Interface
============================================================

Module  : AI Embeddings Layer
Purpose : Abstract base class for embedding providers (Gemini, Mock, etc.).
"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Abstract Base Class for vector embedding providers.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of the embedding provider."""
        pass

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Vector dimensions produced by this provider."""
        pass

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Generate vector embedding for a single string."""
        pass

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate vector embeddings for a list of strings."""
        pass
