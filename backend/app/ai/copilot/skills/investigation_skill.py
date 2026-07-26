"""
Investigation Skill. Orchestrates case summary and next steps.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.actions.action_registry import ActionRegistry
from app.ai.copilot.skills.base import BaseSkill


class InvestigationSkill(BaseSkill):
    """Skill orchestrating summary + next steps actions."""

    @property
    def name(self) -> str:
        return "investigation_skill"

    @property
    def description(self) -> str:
        return "Orchestrates comprehensive case summary and recommended next steps."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res1 = ActionRegistry.execute("summarize_case", session_id, case_id, payload)
        res2 = ActionRegistry.execute("suggest_next_steps", session_id, case_id, payload)

        return ActionResult(
            action_name="investigation_skill",
            success=res1.success and res2.success,
            message=f"Investigation skill executed: {res1.message} {res2.message}",
            data={"summary_data": res1.data, "next_steps_data": res2.data},
            confidence=0.94,
        )
