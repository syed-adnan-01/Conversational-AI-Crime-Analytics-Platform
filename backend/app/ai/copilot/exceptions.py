"""
Exceptions for CrimeSphere AI Copilot.
"""


class CopilotException(Exception):
    """Base exception for all Copilot operations."""
    pass


class SessionNotFoundException(CopilotException):
    """Raised when a Copilot session or workspace is not found."""
    pass


class PlannerException(CopilotException):
    """Raised when CopilotPlanner fails to resolve an execution plan."""
    pass


class ActionExecutionException(CopilotException):
    """Raised when an action or skill execution fails."""
    pass


class MemoryLimitExceededException(CopilotException):
    """Raised when session memory usage exceeds capacity limits."""
    pass
