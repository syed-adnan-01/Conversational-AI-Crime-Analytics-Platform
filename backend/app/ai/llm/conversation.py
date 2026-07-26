"""
Conversation Manager for tracking multi-turn user/AI chat turns.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.ai.prompting.prompt_models import ConversationTurn


class ConversationSession(BaseModel):
    """Session object storing multi-turn history."""
    model_config = ConfigDict(from_attributes=True)

    conversation_id: str
    provider: str = "quickml"
    model: str = "quickml-rag-v1"
    turns: List[ConversationTurn] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_turn(self, role: str, content: str) -> None:
        self.turns.append(ConversationTurn(role=role, content=content))
        self.updated_at = datetime.now(timezone.utc)


class ConversationManager:
    """In-memory conversation store for AI Copilot continuity."""

    _sessions: Dict[str, ConversationSession] = {}

    @classmethod
    def get_or_create_session(
        cls, conversation_id: str, provider: str = "quickml", model: str = "default"
    ) -> ConversationSession:
        if conversation_id not in cls._sessions:
            cls._sessions[conversation_id] = ConversationSession(
                conversation_id=conversation_id,
                provider=provider,
                model=model,
            )
        return cls._sessions[conversation_id]

    @classmethod
    def append_turn(cls, conversation_id: str, role: str, content: str) -> None:
        session = cls.get_or_create_session(conversation_id)
        session.add_turn(role, content)

    @classmethod
    def get_history(cls, conversation_id: str) -> List[ConversationTurn]:
        if conversation_id in cls._sessions:
            return cls._sessions[conversation_id].turns
        return []

    @classmethod
    def clear(cls) -> None:
        cls._sessions.clear()
