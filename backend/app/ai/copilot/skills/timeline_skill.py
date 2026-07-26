"""
Timeline Skill.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.actions.action_registry import ActionRegistry
from app.ai.copilot.skills.base import BaseSkill


class TimelineSkill(BaseSkill):
    """Skill for timeline reconstruction and gap analysis."""

    @property
    def name(self) -> str:
        return "timeline_skill"

    @property
    def description(self) -> str:
        return "Reconstructs chronological timeline and highlights timeline gaps."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = ActionRegistry.execute("timeline_analysis", session_id, case_id, payload)
        return ActionResult(
            action_name="timeline_skill",
            success=res.success,
            message=f"Timeline skill executed: {res.message}",
            data=res.data,
            confidence=0.92,
        )
