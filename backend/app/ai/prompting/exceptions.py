"""
Exceptions for the CrimeSphere AI Prompt Engine.
"""


class PromptEngineException(Exception):
    """Base exception for all Prompt Engine errors."""
    pass


class PromptValidationException(PromptEngineException):
    """Raised when a prompt fails validation (e.g. empty content, missing fields, unresolved placeholders)."""
    pass


class TemplateNotFoundException(PromptEngineException):
    """Raised when a requested prompt template or version manifest cannot be found."""
    pass


class PersonaNotFoundException(PromptEngineException):
    """Raised when a requested persona is not registered."""
    pass


class TokenBudgetExceededException(PromptEngineException):
    """Raised when prompt token count exceeds the allocated maximum token budget."""
    pass
