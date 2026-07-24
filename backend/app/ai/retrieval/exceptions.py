"""
============================================================
Retrieval Exceptions
============================================================

Module  : AI Retrieval Engine
Purpose : Exception hierarchy for retrieval, reranking, context assembly,
          and pipeline execution.
"""

from app.core.exceptions import CrimeSphereException


class RetrievalException(CrimeSphereException):
    """Base exception for retrieval layer failures."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message=message, status_code=status_code)


class RetrieverException(RetrievalException):
    """Exception raised when a retriever strategy fails."""

    def __init__(self, retriever_name: str, reason: str):
        super().__init__(
            message=f"Retriever '{retriever_name}' failure: {reason}",
            status_code=500,
        )


class RerankerException(RetrievalException):
    """Exception raised when a reranker fails."""

    def __init__(self, reranker_name: str, reason: str):
        super().__init__(
            message=f"Reranker '{reranker_name}' failure: {reason}",
            status_code=500,
        )


class ContextAssemblyException(RetrievalException):
    """Exception raised during prompt context assembly or budget allocation."""

    def __init__(self, reason: str):
        super().__init__(
            message=f"Context assembly failure: {reason}",
            status_code=500,
        )
