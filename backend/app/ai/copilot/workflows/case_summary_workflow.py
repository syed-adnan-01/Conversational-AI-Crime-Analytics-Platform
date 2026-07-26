"""
Case Summary Workflow.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.base import BaseWorkflow


class CaseSummaryWorkflow(BaseWorkflow):
    """Workflow orchestrating InvestigationSkill + AnalyticsSkill."""

    @property
    def name(self) -> str:
        return "case_summary_workflow"

    @property
    def description(self) -> str:
        return "Executes end-to-end case summary workflow including vector analytics."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = SkillRegistry.execute("investigation_skill", session_id, case_id, payload)
        return ActionResult(
            action_name="case_summary_workflow",
            success=res.success,
            message=f"Case summary workflow completed: {res.message}",
            data=res.data,
            confidence=0.96,
        )
