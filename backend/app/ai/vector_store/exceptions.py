"""
============================================================
Vector Store Exceptions
============================================================

Module  : AI Vector Store Layer
Purpose : Custom exceptions for vector store operations.
"""

from app.core.exceptions import CrimeSphereException


class VectorStoreException(CrimeSphereException):
    """Base exception for vector store failures."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message=message, status_code=status_code)
