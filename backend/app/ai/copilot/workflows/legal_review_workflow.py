"""
Legal Review Workflow.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.base import BaseWorkflow


class LegalReviewWorkflow(BaseWorkflow):
    """Workflow for statutory legal review and penal code section evaluation."""

    @property
    def name(self) -> str:
        return "legal_review_workflow"

    @property
    def description(self) -> str:
        return "Reviews legal viability and cross-examines evidence against acts."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = SkillRegistry.execute("legal_skill", session_id, case_id, payload)
        return ActionResult(
            action_name="legal_review_workflow",
            success=res.success,
            message=f"Legal review workflow completed: {res.message}",
            data=res.data,
            confidence=0.96,
        )
