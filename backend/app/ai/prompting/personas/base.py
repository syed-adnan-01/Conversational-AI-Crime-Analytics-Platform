"""
Base class for AI Personas.
"""

from abc import ABC, abstractmethod
from app.ai.prompting.prompt_models import PromptPersona
from app.ai.prompting.prompt_profiles import PromptProfile


class BasePersona(ABC):
    """Abstract Base Class for persona system prompt generators."""

    @property
    @abstractmethod
    def persona_enum(self) -> PromptPersona:
        """Returns corresponding PromptPersona enum."""
        pass

    @property
    @abstractmethod
    def role_title(self) -> str:
        """Returns human readable role title."""
        pass

    @abstractmethod
    def get_system_instructions(self, profile: PromptProfile) -> str:
        """Generates system instruction prompt text tailored to the persona and workflow profile."""
        pass
