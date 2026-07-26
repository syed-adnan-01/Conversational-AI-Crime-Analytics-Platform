"""
Exceptions for the CrimeSphere LLM Gateway.
"""


class LLMGatewayException(Exception):
    """Base exception for all LLM Gateway errors."""
    pass


class ProviderNotFoundException(LLMGatewayException):
    """Raised when a requested LLM provider is not registered."""
    pass


class ProviderExecutionException(LLMGatewayException):
    """Raised when an LLM provider fails during request execution."""
    pass


class ResponseValidationException(LLMGatewayException):
    """Raised when LLM output fails schema parsing or safety validation."""
    pass


class LLMTimeoutException(LLMGatewayException):
    """Raised when an LLM provider call times out."""
    pass


class RateLimitExceededException(LLMGatewayException):
    """Raised when an LLM provider returns a 429 Rate Limit error."""
    pass
