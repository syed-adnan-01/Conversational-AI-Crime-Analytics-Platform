"""
Skill Registry managing discoverable skills.
"""

from typing import Any, Dict, List, Optional
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.skills.analytics_skill import AnalyticsSkill
from app.ai.copilot.skills.base import BaseSkill
from app.ai.copilot.skills.evidence_skill import EvidenceSkill
from app.ai.copilot.skills.investigation_skill import InvestigationSkill
from app.ai.copilot.skills.legal_skill import LegalSkill
from app.ai.copilot.skills.timeline_skill import TimelineSkill


class SkillRegistry:
    """Central registry for discovering and executing registered Copilot BaseSkill singletons."""

    _skills: Dict[str, BaseSkill] = {}

    @classmethod
    def _initialize(cls) -> None:
        if not cls._skills:
            cls.register(InvestigationSkill())
            cls.register(LegalSkill())
            cls.register(TimelineSkill())
            cls.register(EvidenceSkill())
            cls.register(AnalyticsSkill())

    @classmethod
    def register(cls, skill: BaseSkill) -> None:
        cls._skills[skill.name.lower()] = skill

    @classmethod
    def find(cls, name: str) -> Optional[BaseSkill]:
        cls._initialize()
        return cls._skills.get(name.lower())

    @classmethod
    def execute(cls, name: str, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        cls._initialize()
        skill = cls.find(name)
        if not skill:
            return ActionResult(
                action_name=name,
                success=False,
                error=f"Skill '{name}' is not registered.",
            )
        return skill.execute(session_id, case_id, payload)

    @classmethod
    def list_skills(cls) -> List[Dict[str, str]]:
        cls._initialize()
        return [{"name": s.name, "description": s.description} for s in cls._skills.values()]
