"""
============================================================
Chunking Exceptions
============================================================

Module  : AI Chunking Engine
Purpose : Custom exceptions for context chunking operations.
"""

from app.core.exceptions import CrimeSphereException


class ChunkingException(CrimeSphereException):
    """Base exception for chunking failures."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message=message, status_code=status_code)
