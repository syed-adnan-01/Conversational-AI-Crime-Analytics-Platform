"""
Analytics Skill.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.actions.action_registry import ActionRegistry
from app.ai.copilot.skills.base import BaseSkill


class AnalyticsSkill(BaseSkill):
    """Skill for cross-case semantic pattern analysis."""

    @property
    def name(self) -> str:
        return "analytics_skill"

    @property
    def description(self) -> str:
        return "Executes semantic vector search and pattern analytics."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = ActionRegistry.execute("semantic_search", session_id, case_id, payload)
        return ActionResult(
            action_name="analytics_skill",
            success=res.success,
            message=f"Analytics skill executed: {res.message}",
            data=res.data,
            confidence=0.90,
        )
