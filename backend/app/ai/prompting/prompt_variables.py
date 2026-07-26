"""
Typed PromptVariables model replacing untyped dictionaries for template rendering.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PromptVariables(BaseModel):
    """Container for template substitution variables."""

    system_instructions: str = ""
    case_summary: str = ""
    victims: str = ""
    accused: str = ""
    evidence: str = ""
    timeline: str = ""
    legal: str = ""
    officers: str = ""
    arrest: str = ""
    chargesheet: str = ""
    question: str = ""
    citations: str = ""
    guardrails: str = ""
    output_instructions: str = ""
    history: str = ""
    language: str = "en"
    locale: str = "en_IN"
    custom_context: str = ""

    def to_dict(self) -> dict[str, str]:
        """Converts variables into a string dictionary for Jinja / format rendering."""
        return {key: str(val) for key, val in self.model_dump().items()}
