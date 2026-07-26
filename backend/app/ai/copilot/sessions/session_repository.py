"""
Concrete Implementation of ISessionRepository.
"""

from typing import Dict, List, Optional
from app.ai.copilot.sessions.base_repository import ISessionRepository
from app.ai.copilot.sessions.session_models import CopilotSession, ConversationMessage


class SessionRepository(ISessionRepository):
    """In-memory session repository implementation."""

    _sessions: Dict[str, CopilotSession] = {}

    def create_session(self, session: CopilotSession) -> CopilotSession:
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[CopilotSession]:
        return self._sessions.get(session_id)

    def update_session(self, session: CopilotSession) -> CopilotSession:
        session.touch()
        self._sessions[session.session_id] = session
        return session

    def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def add_message(self, session_id: str, message: ConversationMessage) -> ConversationMessage:
        session = self.get_session(session_id)
        if session:
            session.messages.append(message)
            session.touch()
        return message

    def search_sessions(
        self,
        case_id: Optional[str] = None,
        tag: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[CopilotSession]:
        results: List[CopilotSession] = []
        for s in self._sessions.values():
            if case_id and s.case_id != case_id:
                continue
            if tag and tag.lower() not in [t.lower() for t in s.tags]:
                continue
            if user_id and s.user_id != user_id:
                continue
            results.append(s)
            if len(results) >= limit:
                break
        return results

    def clear(self) -> None:
        self._sessions.clear()
