"""
High-level PromptService providing public API for building, previewing, and inspecting prompts.
"""

from typing import Dict, List, Any
from app.ai.prompting.llm_profiles import get_llm_profile
from app.ai.prompting.output_schema_registry import OutputSchemaRegistry
from app.ai.prompting.prompt_builder import PromptBuilder
from app.ai.prompting.prompt_intents import PromptIntent
from app.ai.prompting.prompt_metrics import PromptMetrics
from app.ai.prompting.prompt_models import (
    PromptPersona,
    PromptRequest,
    PromptResponse,
    PromptType,
    PromptVersion,
)
from app.ai.prompting.prompt_profiles import PromptProfile
from app.ai.prompting.prompt_registry import PromptRegistry
from app.ai.prompting.prompt_validator import PromptValidator
from app.ai.prompting.token_budget_manager import TokenBudgetManager
from app.ai.prompting.prompt_cache import PromptCache


class PromptService:
    """Service layer exposing high-level entry points for prompt engineering operations."""

    def __init__(self, builder: PromptBuilder | None = None):
        self.builder = builder or PromptBuilder()

    def build_prompt(self, request: PromptRequest, use_cache: bool = True) -> PromptResponse:
        """Builds a complete PromptResponse for an input PromptRequest."""
        return self.builder.build(request, use_cache=use_cache)

    def preview_prompt(self, request: PromptRequest) -> Dict[str, Any]:
        """Generates raw preview of system and user prompts without caching."""
        resp = self.build_prompt(request, use_cache=False)
        return {
            "prompt_id": resp.metadata.prompt_id,
            "system_prompt": resp.system_prompt,
            "user_prompt": resp.user_prompt,
            "estimated_tokens": resp.metadata.estimated_tokens,
            "quality_score": resp.metadata.quality_score,
            "provider_hints": resp.metadata.provider_hints,
        }

    def estimate_tokens(self, text: str) -> int:
        """Estimates token count for arbitrary text."""
        return TokenBudgetManager.estimate_tokens(text)

    def validate(self, request: PromptRequest) -> bool:
        """Validates if a prompt request can be built within constraints."""
        try:
            resp = self.build_prompt(request, use_cache=False)
            return PromptValidator.validate(
                resp.system_prompt,
                resp.user_prompt,
                max_budget=request.max_token_budget or 4096,
                raise_on_error=False,
            )
        except Exception:
            return False

    def list_templates(self) -> List[Dict[str, str]]:
        """Returns list of registered prompt templates."""
        return PromptRegistry.list_templates()

    def list_personas(self) -> List[str]:
        """Returns list of supported persona roles."""
        return [p.value for p in PromptPersona]

    def list_profiles(self) -> List[str]:
        """Returns list of supported workflow profiles."""
        return [pr.value for pr in PromptProfile]

    def list_intents(self) -> List[str]:
        """Returns list of supported prompt intents."""
        return [i.value for i in PromptIntent]

    def list_versions(self) -> List[PromptVersion]:
        """Returns list of available template versions."""
        return PromptRegistry.list_versions()

    def get_metrics(self) -> Dict[str, Any]:
        """Returns current operational metrics."""
        return PromptMetrics.get_summary()

    def clear_cache(self) -> None:
        """Clears in-memory prompt cache."""
        PromptCache.clear()
