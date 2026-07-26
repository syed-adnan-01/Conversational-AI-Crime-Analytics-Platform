"""
Supervisor Persona focusing on case quality audit, risk assessment, and supervisory oversight.
"""

from app.ai.prompting.personas.base import BasePersona
from app.ai.prompting.prompt_models import PromptPersona
from app.ai.prompting.prompt_profiles import PromptProfile


class SupervisorPersona(BasePersona):
    @property
    def persona_enum(self) -> PromptPersona:
        return PromptPersona.SUPERVISOR

    @property
    def role_title(self) -> str:
        return "Superintendent of Police & Case Quality Auditor"

    def get_system_instructions(self, profile: PromptProfile) -> str:
        return (
            "You are a Senior Officer (Superintendent of Police) reviewing case files for supervisory oversight. "
            "Your focus is on overall investigation quality, accountability, risk assessment, procedural delays, "
            "and ensuring comprehensive case preparation before formal court submission. "
            f"Current Workflow Objective: {profile.value.upper()}."
        )
