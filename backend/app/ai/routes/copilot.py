"""
AI Copilot REST Router — Phase 3.6
Endpoints mounted at /ai/copilot
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.ai.copilot.copilot_models import CopilotRequest, CopilotResponse, FeedbackRating
from app.ai.copilot.copilot_service import CopilotService
from app.ai.copilot.exceptions import CopilotException, SessionNotFoundException

router = APIRouter()
_service = CopilotService()


# ---------------------------------------------------------------------------
# Request / Response Schemas
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    session_id: str
    case_id: str
    message: str
    persona: str = "investigator"
    stream: bool = False
    context: Dict[str, Any] = {}


class FeedbackRequest(BaseModel):
    session_id: str
    turn_id: str
    rating: FeedbackRating
    comment: Optional[str] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/chat", response_model=CopilotResponse, summary="Chat with the AI Copilot")
def chat(body: ChatRequest) -> CopilotResponse:
    """Process a conversational turn with the investigation AI copilot."""
    try:
        request = CopilotRequest(
            session_id=body.session_id,
            case_id=body.case_id,
            user_message=body.message,
            persona=body.persona,
            stream=body.stream,
            context=body.context,
        )
        return _service.chat(request)
    except CopilotException as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Copilot engine error: {exc}")


@router.get("/history/{session_id}", summary="Get conversation history for a session")
def get_history(
    session_id: str,
    limit: int = Query(default=20, ge=1, le=100),
) -> Dict[str, Any]:
    """Return recent conversation turns from session memory."""
    history = _service.get_history(session_id, limit=limit)
    return {"session_id": session_id, "count": len(history), "messages": history}


@router.get("/session/{session_id}", summary="Get copilot session details")
def get_session(session_id: str) -> Dict[str, Any]:
    data = _service.get_session(session_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return data


@router.delete("/session/{session_id}", summary="End a copilot session")
def end_session(session_id: str) -> Dict[str, Any]:
    return _service.end_session(session_id)


@router.post("/feedback", summary="Submit feedback for a copilot response")
def submit_feedback(body: FeedbackRequest) -> Dict[str, Any]:
    """Record investigator feedback on a copilot answer turn."""
    fb = _service.submit_feedback(
        session_id=body.session_id,
        turn_id=body.turn_id,
        rating=body.rating,
        comment=body.comment,
    )
    return {
        "feedback_id": fb.feedback_id,
        "session_id": fb.session_id,
        "rating": fb.rating,
        "recorded": True,
    }


@router.get("/search", summary="Semantic search across case documents")
def search(
    case_id: str = Query(..., description="Case ID to search within"),
    q: str = Query(..., description="Natural-language search query"),
) -> Dict[str, Any]:
    """Execute a single-turn semantic search without creating a session."""
    return _service.search(case_id=case_id, query=q)


@router.get("/health", summary="Copilot subsystem health check")
def health() -> Dict[str, Any]:
    """Return copilot engine health, registered skills, workflows, and metrics."""
    return _service.health()
