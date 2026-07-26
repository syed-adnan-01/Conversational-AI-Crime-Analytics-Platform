"""
LLM Provider Registry.
Manages provider lifecycle and retrieves active provider singletons.
"""

from typing import Dict, List, Type
from app.ai.llm.config import llm_config
from app.ai.llm.exceptions import ProviderNotFoundException
from app.ai.llm.providers.base import BaseLLMProvider
from app.ai.llm.providers.catalyst_quickml_provider import CatalystQuickMLProvider
from app.ai.llm.providers.claude_provider import ClaudeProvider
from app.ai.llm.providers.gemini_provider import GeminiProvider
from app.ai.llm.providers.mock_provider import MockLLMProvider
from app.ai.llm.providers.openai_provider import OpenAIProvider


class ProviderRegistry:
    """Registry maintaining active LLM Provider instances."""

    _providers: Dict[str, BaseLLMProvider] = {}

    @classmethod
    def _initialize(cls) -> None:
        """Initializes default providers if registry is empty."""
        if not cls._providers:
            cls.register("quickml", CatalystQuickMLProvider())
            cls.register("gemini", GeminiProvider())
            cls.register("openai", OpenAIProvider())
            cls.register("claude", ClaudeProvider())
            cls.register("mock", MockLLMProvider())

    @classmethod
    def register(cls, name: str, provider: BaseLLMProvider) -> None:
        """Registers a provider singleton."""
        cls._providers[name.lower()] = provider

    @classmethod
    def get(cls, name: str | None = None) -> BaseLLMProvider:
        """Retrieves provider by name, defaulting to config ACTIVE_PROVIDER."""
        cls._initialize()
        target = (name or llm_config.ACTIVE_PROVIDER).lower()
        if target not in cls._providers:
            # Fallback to quickml or mock if requested provider is unknown
            if "quickml" in cls._providers:
                return cls._providers["quickml"]
            elif "mock" in cls._providers:
                return cls._providers["mock"]
            raise ProviderNotFoundException(f"Provider '{target}' is not registered.")
        return cls._providers[target]

    @classmethod
    def list_providers(cls) -> List[str]:
        """Returns list of registered provider names."""
        cls._initialize()
        return list(cls._providers.keys())

    @classmethod
    def clear(cls) -> None:
        cls._providers.clear()
