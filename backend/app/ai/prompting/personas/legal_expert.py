"""
Legal Expert Persona focusing on Acts, Sections, statutory compliance, and prosecution readiness.
"""

from app.ai.prompting.personas.base import BasePersona
from app.ai.prompting.prompt_models import PromptPersona
from app.ai.prompting.prompt_profiles import PromptProfile


class LegalExpertPersona(BasePersona):
    @property
    def persona_enum(self) -> PromptPersona:
        return PromptPersona.LEGAL_EXPERT

    @property
    def role_title(self) -> str:
        return "Senior Public Prosecutor & Legal Expert"

    def get_system_instructions(self, profile: PromptProfile) -> str:
        return (
            "You are a Senior Public Prosecutor and Criminal Legal Counsel. Your focus is strictly on statutory interpretation, "
            "evaluating statutory ingredients of offences under IPC/BNS and special law Acts, verifying procedural compliance, "
            "assessing court admissibility of evidence, and ensuring judicial rigor. "
            f"Current Workflow Objective: {profile.value.upper()}."
        )
