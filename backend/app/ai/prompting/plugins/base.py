"""
Base interface for Prompt Lifecycle Plugins.
"""

from typing import TYPE_CHECKING
from app.ai.prompting.prompt_models import PromptRequest, PromptResponse
from app.ai.prompting.prompt_variables import PromptVariables

if TYPE_CHECKING:
    pass


class PromptPlugin:
    """Base plugin class exposing lifecycle hooks for prompt construction customization."""

    name: str = "base_plugin"

    def before_build(self, request: PromptRequest) -> None:
        """Hook called before prompt building begins."""
        pass

    def before_render(self, request: PromptRequest, variables: PromptVariables) -> None:
        """Hook called before template variables are rendered into Markdown templates."""
        pass

    def after_render(self, request: PromptRequest, variables: PromptVariables, rendered_text: str) -> str:
        """Hook called after template variables are rendered; returns modified text."""
        return rendered_text

    def before_validate(self, request: PromptRequest, system_prompt: str, user_prompt: str) -> tuple[str, str]:
        """Hook called before prompt validation; returns modified (system_prompt, user_prompt)."""
        return system_prompt, user_prompt

    def after_validate(self, request: PromptRequest, response: PromptResponse) -> None:
        """Hook called after prompt validation succeeds."""
        pass

    def after_build(self, request: PromptRequest, response: PromptResponse) -> None:
        """Hook called after prompt building is complete."""
        pass
