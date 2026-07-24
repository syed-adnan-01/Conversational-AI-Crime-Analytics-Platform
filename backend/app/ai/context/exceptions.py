"""
============================================================
AI Context Exceptions
============================================================

Module  : AI Context Builder
Purpose : Dedicated exception hierarchy for AI context errors.
"""

from app.core.exceptions import CrimeSphereException


class AIContextException(CrimeSphereException):
    """Base exception for all AI Context related failures."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message=message, status_code=status_code)


class AIContextBuildException(AIContextException):
    """Raised when building an InvestigationContext fails."""

    def __init__(self, case_id: str, reason: str):
        super().__init__(
            message=f"Failed to build AI context for case '{case_id}': {reason}",
            status_code=500,
        )


class AIContextSerializationException(AIContextException):
    """Raised when serializing an InvestigationContext fails."""

    def __init__(self, format_type: str, reason: str):
        super().__init__(
            message=f"Failed to serialize AI context to '{format_type}': {reason}",
            status_code=500,
        )
