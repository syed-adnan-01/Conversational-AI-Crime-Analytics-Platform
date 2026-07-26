"""
Abstract Base Class for all LLM Providers.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any

from app.ai.llm.capabilities import ProviderCapabilities
from app.ai.llm.llm_models import LLMRequest, LLMResponse


class BaseLLMProvider(ABC):
    """Abstract interface enforcing uniform contract for every LLM provider."""

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        """Returns the provider capability matrix."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns provider string identifier."""
        pass

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Executes generation request and returns strongly typed LLMResponse."""
        pass

    @abstractmethod
    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Yields streaming text chunks as an AsyncGenerator."""
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Counts or estimates token length of text."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Returns True if provider connection and credentials are valid."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Returns metadata about active model and provider features."""
        pass
