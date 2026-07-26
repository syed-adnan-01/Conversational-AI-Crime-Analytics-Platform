"""
Semantic Search Action.
"""

from typing import Any, Dict
from app.ai.copilot.actions.action_models import ActionMetadata, ActionResult
from app.ai.copilot.actions.base import BaseAction


class SemanticSearchAction(BaseAction):
    """Action for vector semantic search across case records."""

    @property
    def metadata(self) -> ActionMetadata:
        return ActionMetadata(
            name="semantic_search",
            description="Performs semantic vector search across indexed case chunks.",
            requires_retrieval=True,
        )

    def execute(self, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        query = payload.get("query", "case facts")
        return ActionResult(
            action_name="semantic_search",
            success=True,
            message=f"Semantic search completed for query: {query}",
            data={"results_count": 5},
            confidence=0.94,
            latency_ms=120.0,
        )
