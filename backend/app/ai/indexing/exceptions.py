"""
============================================================
Indexing Exceptions
============================================================

Module  : AI Indexing Subsystem
Purpose : Custom exceptions for context indexing operations.
"""

from app.core.exceptions import CrimeSphereException


class IndexingException(CrimeSphereException):
    """Base exception for indexing failures."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message=message, status_code=status_code)
