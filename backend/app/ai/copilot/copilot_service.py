"""
Copilot Service — application-layer facade consumed by the REST router.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.ai.copilot.copilot_engine import CopilotEngine
from app.ai.copilot.copilot_metrics import CopilotMetrics
from app.ai.copilot.copilot_models import (
    CopilotFeedback,
    CopilotRequest,
    CopilotResponse,
    FeedbackRating,
)
from app.ai.copilot.feedback_store import FeedbackStore
from app.ai.copilot.memory.memory_manager import MemoryManager
from app.ai.copilot.sessions.session_service import SessionService
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.workflow_registry import WorkflowRegistry

_engine = CopilotEngine()
_session_service = SessionService()
_feedback_store = FeedbackStore()


class CopilotService:
    """Application-layer service providing copilot chat, feedback, and introspection."""

    # ------------------------------------------------------------------
    # Core chat
    # ------------------------------------------------------------------

    def chat(self, request: CopilotRequest) -> CopilotResponse:
        """Process a conversational turn and return a structured response."""
        # Ensure session exists
        _session_service.get_or_create(request.session_id, request.case_id)
        return _engine.process(request)

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End and summarize a session."""
        session = _session_service.get(session_id)
        if not session:
            return {"status": "not_found", "session_id": session_id}
        _session_service.close(session_id)
        return {"status": "closed", "session_id": session_id}

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        session = _session_service.get(session_id)
        if not session:
            return None
        return session.model_dump()

    # ------------------------------------------------------------------
    # Conversation history
    # ------------------------------------------------------------------

    def get_history(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Return recent conversation turns from short-term memory."""
        messages = MemoryManager.get_recent(session_id, limit=limit)
        return [m.model_dump() for m in messages]

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------

    def submit_feedback(
        self,
        session_id: str,
        turn_id: str,
        rating: FeedbackRating,
        comment: Optional[str] = None,
    ) -> CopilotFeedback:
        feedback = CopilotFeedback(
            session_id=session_id,
            turn_id=turn_id,
            rating=rating,
            comment=comment,
        )
        return _feedback_store.record(feedback)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def health(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "skills": SkillRegistry.list_skills(),
            "workflows": WorkflowRegistry.list_workflows(),
            "metrics": CopilotMetrics.snapshot(),
        }

    def search(self, case_id: str, query: str, session_id: str = "search") -> Dict[str, Any]:
        """Execute a semantic search without a full conversational turn."""
        request = CopilotRequest(
            session_id=session_id,
            case_id=case_id,
            user_message=f"search {query}",
        )
        response = _engine.process(request)
        return {"query": query, "result": response.answer, "confidence": response.confidence}
