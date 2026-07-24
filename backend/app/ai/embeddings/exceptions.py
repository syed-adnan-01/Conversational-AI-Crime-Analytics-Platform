"""
============================================================
Embedding Exceptions
============================================================

Module  : AI Embeddings Layer
Purpose : Custom exceptions for embedding providers and service failures.
"""

from app.core.exceptions import CrimeSphereException


class EmbeddingException(CrimeSphereException):
    """Base exception for embedding layer failures."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message=message, status_code=status_code)


class EmbeddingProviderException(EmbeddingException):
    """Raised when an embedding provider fails to generate vector embeddings."""

    def __init__(self, provider_name: str, reason: str):
        super().__init__(
            message=f"Embedding provider '{provider_name}' failure: {reason}",
            status_code=500,
        )
