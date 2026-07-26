"""
LLM Capability Profiles defining provider limits and recommended parameters.
"""

from typing import Any
from pydantic import BaseModel, Field


class LLMCapabilityProfile(BaseModel):
    """Base capability profile for an LLM provider."""
    provider_name: str
    maximum_context: int = 1048576
    supports_json: bool = True
    supports_tools: bool = True
    supports_images: bool = True
    recommended_temperature: float = 0.2
    recommended_top_p: float = 0.95
    recommended_output_tokens: int = 2048

    def get_provider_hints(self, override_hints: dict[str, Any] | None = None) -> dict[str, Any]:
        """Returns effective provider hints merging profile defaults with overrides."""
        base_hints = {
            "temperature": self.recommended_temperature,
            "top_p": self.recommended_top_p,
            "max_output_tokens": self.recommended_output_tokens,
            "supports_json": self.supports_json,
            "supports_tools": self.supports_tools,
        }
        if override_hints:
            base_hints.update(override_hints)
        return base_hints


class GeminiProfile(LLMCapabilityProfile):
    provider_name: str = "gemini"
    maximum_context: int = 1048576
    supports_json: bool = True
    supports_tools: bool = True
    supports_images: bool = True
    recommended_temperature: float = 0.2
    recommended_top_p: float = 0.95
    recommended_output_tokens: int = 4096


class QuickMLProfile(LLMCapabilityProfile):
    provider_name: str = "catalyst_quickml"
    maximum_context: int = 128000
    supports_json: bool = True
    supports_tools: bool = False
    supports_images: bool = False
    recommended_temperature: float = 0.1
    recommended_top_p: float = 0.90
    recommended_output_tokens: int = 2048


class OpenAIProfile(LLMCapabilityProfile):
    provider_name: str = "openai"
    maximum_context: int = 128000
    supports_json: bool = True
    supports_tools: bool = True
    supports_images: bool = True
    recommended_temperature: float = 0.2
    recommended_top_p: float = 1.0
    recommended_output_tokens: int = 4096


class ClaudeProfile(LLMCapabilityProfile):
    provider_name: str = "claude"
    maximum_context: int = 200000
    supports_json: bool = True
    supports_tools: bool = True
    supports_images: bool = True
    recommended_temperature: float = 0.2
    recommended_top_p: float = 0.99
    recommended_output_tokens: int = 4096


class GenericLLMProfile(LLMCapabilityProfile):
    provider_name: str = "generic"
    maximum_context: int = 32768
    supports_json: bool = True
    supports_tools: bool = False
    supports_images: bool = False
    recommended_temperature: float = 0.3
    recommended_top_p: float = 0.9
    recommended_output_tokens: int = 2048


_PROFILES: dict[str, LLMCapabilityProfile] = {
    "gemini": GeminiProfile(),
    "quickml": QuickMLProfile(),
    "openai": OpenAIProfile(),
    "claude": ClaudeProfile(),
    "generic": GenericLLMProfile(),
}


def get_llm_profile(provider: str = "gemini") -> LLMCapabilityProfile:
    """Retrieve capability profile for a provider name."""
    return _PROFILES.get(provider.lower(), GenericLLMProfile(provider_name=provider))
