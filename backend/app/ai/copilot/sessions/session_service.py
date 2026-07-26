"""
High-Level Session Service Facade.
"""

import uuid
from typing import List, Optional
from app.ai.copilot.exceptions import SessionNotFoundException
from app.ai.copilot.sessions.base_repository import ISessionRepository
from app.ai.copilot.sessions.session_models import CopilotSession, ConversationMessage
from app.ai.copilot.sessions.session_repository import SessionRepository


class SessionService:
    """Service handling session operations using ISessionRepository."""

    def __init__(self, repo: Optional[ISessionRepository] = None):
        self.repo = repo or SessionRepository()

    def create(self, case_id: str, user_id: str, mode: str = "ASSISTANT", tags: Optional[List[str]] = None) -> CopilotSession:
        sid = f"COPILOT-{uuid.uuid4().hex[:8]}"
        session = CopilotSession(
            session_id=sid,
            case_id=case_id,
            user_id=user_id,
            mode=mode,
            tags=tags or ["Investigation"],
        )
        return self.repo.create_session(session)

    def get(self, session_id: str) -> CopilotSession:
        session = self.repo.get_session(session_id)
        if not session:
            raise SessionNotFoundException(f"Copilot session '{session_id}' not found.")
        return session

    def delete(self, session_id: str) -> bool:
        return self.repo.delete_session(session_id)

    def search(
        self,
        case_id: Optional[str] = None,
        tag: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[CopilotSession]:
        return self.repo.search_sessions(case_id=case_id, tag=tag, user_id=user_id, limit=limit)

    def get_or_create(self, session_id: str, case_id: str = "") -> CopilotSession:
        """Return existing session or create a minimal one if not found."""
        session = self.repo.get_session(session_id)
        if session:
            return session
        session = CopilotSession(
            session_id=session_id,
            case_id=case_id,
            user_id="anonymous",
        )
        return self.repo.create_session(session)

    def close(self, session_id: str) -> bool:
        """Mark session as closed (delegates to delete for in-memory store)."""
        return self.repo.delete_session(session_id)

