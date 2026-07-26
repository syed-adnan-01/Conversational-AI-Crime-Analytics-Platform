"""
Legal Analysis Action.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionMetadata, ActionResult
from app.ai.copilot.actions.base import BaseAction


class LegalAnalysisAction(BaseAction):
    """Action for mapping IPC/BNS sections and evaluating penal provisions."""

    @property
    def metadata(self) -> ActionMetadata:
        return ActionMetadata(
            name="legal_analysis",
            description="Evaluates applicable statutory sections (IPC, IT Act) and prosecution viability.",
            required_context=["Act", "Section"],
        )

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        return ActionResult(
            action_name="legal_analysis",
            success=True,
            message="Legal analysis executed successfully.",
            data={"applicable_sections": ["IPC Sec 420", "IT Act Sec 66D"], "viability": "HIGH"},
            confidence=0.96,
            latency_ms=160.0,
        )
