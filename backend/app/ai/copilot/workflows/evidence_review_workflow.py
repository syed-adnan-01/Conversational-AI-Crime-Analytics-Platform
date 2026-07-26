"""
Evidence Review Workflow.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.base import BaseWorkflow


class EvidenceReviewWorkflow(BaseWorkflow):
    """Workflow for physical and digital evidence review."""

    @property
    def name(self) -> str:
        return "evidence_review_workflow"

    @property
    def description(self) -> str:
        return "Executes thorough evidence examination workflow."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = SkillRegistry.execute("evidence_skill", session_id, case_id, payload)
        return ActionResult(
            action_name="evidence_review_workflow",
            success=res.success,
            message=f"Evidence review workflow completed: {res.message}",
            data=res.data,
            confidence=0.94,
        )
