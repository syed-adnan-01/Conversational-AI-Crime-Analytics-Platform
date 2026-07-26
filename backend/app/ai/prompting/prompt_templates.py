"""
Template Engine rendering Markdown templates with typed PromptVariables.
"""

from typing import Dict
from app.ai.prompting.exceptions import PromptValidationException
from app.ai.prompting.prompt_variables import PromptVariables


class TemplateEngine:
    """Renders Markdown template files using PromptVariables."""

    @classmethod
    def render(cls, template_content: str, variables: PromptVariables) -> str:
        """Renders placeholders in template_content using variables."""
        if not template_content:
            return ""

        rendered = template_content
        var_dict = variables.to_dict()

        for key, val in var_dict.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, val)

        return rendered

    @classmethod
    def find_unresolved_placeholders(cls, text: str) -> list[str]:
        """Finds any unresolved {{placeholder}} tokens remaining in text."""
        import re
        return re.findall(r"\{\{[a-zA-Z0-9_]+\}\}", text)
