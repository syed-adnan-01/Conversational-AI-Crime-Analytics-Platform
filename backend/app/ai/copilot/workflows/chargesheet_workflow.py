"""
Chargesheet Workflow.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.base import BaseWorkflow


class ChargesheetWorkflow(BaseWorkflow):
    """Workflow orchestrating LegalSkill + EvidenceSkill for chargesheet prep."""

    @property
    def name(self) -> str:
        return "chargesheet_workflow"

    @property
    def description(self) -> str:
        return "Executes chargesheet preparation workflow mapping statutory evidence."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = SkillRegistry.execute("legal_skill", session_id, case_id, payload)
        return ActionResult(
            action_name="chargesheet_workflow",
            success=res.success,
            message=f"Chargesheet workflow executed: {res.message}",
            data=res.data,
            confidence=0.95,
        )
