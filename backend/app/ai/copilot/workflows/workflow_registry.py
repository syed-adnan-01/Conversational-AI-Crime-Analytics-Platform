"""
Workflow Registry for dynamic workflow lookup and dispatch.
"""

from typing import Any, Dict, List, Optional
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.workflows.base import BaseWorkflow
from app.ai.copilot.workflows.case_summary_workflow import CaseSummaryWorkflow
from app.ai.copilot.workflows.chargesheet_workflow import ChargesheetWorkflow
from app.ai.copilot.workflows.evidence_review_workflow import EvidenceReviewWorkflow
from app.ai.copilot.workflows.investigation_workflow import InvestigationWorkflow
from app.ai.copilot.workflows.legal_review_workflow import LegalReviewWorkflow


class WorkflowRegistry:
    """Central registry for discovering and executing registered Copilot BaseWorkflow singletons."""

    _workflows: Dict[str, BaseWorkflow] = {}

    @classmethod
    def _initialize(cls) -> None:
        if not cls._workflows:
            cls.register(CaseSummaryWorkflow())
            cls.register(ChargesheetWorkflow())
            cls.register(LegalReviewWorkflow())
            cls.register(InvestigationWorkflow())
            cls.register(EvidenceReviewWorkflow())

    @classmethod
    def register(cls, workflow: BaseWorkflow) -> None:
        cls._workflows[workflow.name.lower()] = workflow

    @classmethod
    def find(cls, name: str) -> Optional[BaseWorkflow]:
        cls._initialize()
        return cls._workflows.get(name.lower())

    @classmethod
    def execute(cls, name: str, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        cls._initialize()
        wf = cls.find(name)
        if not wf:
            return ActionResult(
                action_name=name,
                success=False,
                error=f"Workflow '{name}' is not registered.",
            )
        return wf.execute(session_id, case_id, payload)

    @classmethod
    def list_workflows(cls) -> List[Dict[str, str]]:
        cls._initialize()
        return [{"name": w.name, "description": w.description} for w in cls._workflows.values()]
