"""
Evidence Skill.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionResult
from app.ai.copilot.actions.action_registry import ActionRegistry
from app.ai.copilot.skills.base import BaseSkill


class EvidenceSkill(BaseSkill):
    """Skill for forensic and physical evidence evaluation."""

    @property
    def name(self) -> str:
        return "evidence_skill"

    @property
    def description(self) -> str:
        return "Evaluates recorded evidence items and cross-references statements."

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        res = ActionRegistry.execute("analyze_evidence", session_id, case_id, payload)
        return ActionResult(
            action_name="evidence_skill",
            success=res.success,
            message=f"Evidence skill executed: {res.message}",
            data=res.data,
            confidence=0.93,
        )
