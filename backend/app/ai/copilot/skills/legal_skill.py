"""
Legal Skill. Orchestrates evidence analysis and legal section mapping.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.actions.action_registry import ActionRegistry
from app.ai.copilot.skills.base import BaseSkill


class LegalSkill(BaseSkill):
    """Skill orchestrating legal analysis and evidence cross-examination."""

    @property
    def name(self) -> str:
        return "legal_skill"

    @property
    def description(self) -> str:
        return "Orchestrates evidence analysis and statutory section mapping for prosecution opinion."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = ActionRegistry.execute("legal_analysis", session_id, case_id, payload)
        return ActionResult(
            action_name="legal_skill",
            success=res.success,
            message=f"Legal skill executed: {res.message}",
            data=res.data,
            confidence=0.95,
        )
