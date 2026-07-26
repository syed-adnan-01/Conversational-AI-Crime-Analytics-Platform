"""
Suggest Next Steps Action.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionMetadata, ActionResult
from app.ai.copilot.actions.base import BaseAction


class SuggestNextStepsAction(BaseAction):
    """Action for generating recommended investigative steps."""

    @property
    def metadata(self) -> ActionMetadata:
        return ActionMetadata(
            name="suggest_next_steps",
            description="Generates prioritized next investigative actions for lead officers.",
        )

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        return ActionResult(
            action_name="suggest_next_steps",
            success=True,
            message="Next steps generated.",
            data={"next_steps": ["Issue notice under Sec 91 CrPC to bank", "Forensic extraction of seized phone"]},
            confidence=0.90,
            latency_ms=140.0,
        )
