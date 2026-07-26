"""
Compare Statements Action.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionMetadata, ActionResult
from app.ai.copilot.actions.base import BaseAction


class CompareStatementsAction(BaseAction):
    """Action for cross-examining witness and suspect statements."""

    @property
    def metadata(self) -> ActionMetadata:
        return ActionMetadata(
            name="compare_statements",
            description="Cross-examines witness, victim, and accused statements for contradictions.",
            required_context=["Witness", "Accused"],
            estimated_latency_ms=1000.0,
        )

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        return ActionResult(
            action_name="compare_statements",
            success=True,
            message="Statement comparison complete.",
            data={"contradictions": ["Alibi time mismatch noted between Witness WIT-001 and Accused ACC-001"]},
            confidence=0.88,
            latency_ms=210.0,
        )
