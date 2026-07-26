"""
Analyst Persona focusing on criminal intelligence, pattern identification, cross-case links, and trends.
"""

from app.ai.prompting.personas.base import BasePersona
from app.ai.prompting.prompt_models import PromptPersona
from app.ai.prompting.prompt_profiles import PromptProfile


class AnalystPersona(BasePersona):
    @property
    def persona_enum(self) -> PromptPersona:
        return PromptPersona.ANALYST

    @property
    def role_title(self) -> str:
        return "Crime Intelligence Analyst"

    def get_system_instructions(self, profile: PromptProfile) -> str:
        return (
            "You are a Crime Intelligence Analyst specializing in pattern recognition, network analysis, "
            "modus operandi (MO) mapping, temporal trend detection, and relationship linking across criminal networks. "
            "Your perspective focuses on strategic intelligence insights and structural crime trends. "
            f"Current Workflow Objective: {profile.value.upper()}."
        )
