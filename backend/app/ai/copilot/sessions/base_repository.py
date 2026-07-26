"""
Abstract Session Repository Interface (ISessionRepository).
Decouples session storage logic following Clean Architecture.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.ai.copilot.sessions.session_models import CopilotSession, ConversationMessage


class ISessionRepository(ABC):
    """Abstract interface for Copilot Session persistence."""

    @abstractmethod
    def create_session(self, session: CopilotSession) -> CopilotSession:
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[CopilotSession]:
        pass

    @abstractmethod
    def update_session(self, session: CopilotSession) -> CopilotSession:
        pass

    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        pass

    @abstractmethod
    def add_message(self, session_id: str, message: ConversationMessage) -> ConversationMessage:
        pass

    @abstractmethod
    def search_sessions(
        self,
        case_id: Optional[str] = None,
        tag: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[CopilotSession]:
        pass
