"""
Investigation Workflow.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.base import BaseWorkflow


class InvestigationWorkflow(BaseWorkflow):
    """Workflow orchestrating full investigation pipeline."""

    @property
    def name(self) -> str:
        return "investigation_workflow"

    @property
    def description(self) -> str:
        return "Orchestrates investigation skill, timeline reconstruction, and next steps."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = SkillRegistry.execute("investigation_skill", session_id, case_id, payload)
        return ActionResult(
            action_name="investigation_workflow",
            success=res.success,
            message=f"Investigation workflow completed: {res.message}",
            data=res.data,
            confidence=0.95,
        )
