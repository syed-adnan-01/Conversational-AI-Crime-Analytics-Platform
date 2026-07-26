"""
AI Personas Package.
"""

from app.ai.prompting.personas.base import BasePersona
from app.ai.prompting.personas.investigator import InvestigatorPersona
from app.ai.prompting.personas.legal_expert import LegalExpertPersona
from app.ai.prompting.personas.analyst import AnalystPersona
from app.ai.prompting.personas.supervisor import SupervisorPersona

__all__ = [
    "BasePersona",
    "InvestigatorPersona",
    "LegalExpertPersona",
    "AnalystPersona",
    "SupervisorPersona",
]
