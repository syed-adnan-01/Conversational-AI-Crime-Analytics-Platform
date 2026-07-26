"""
Three-Tier Memory Manager orchestrating ShortTermMemory, WorkingMemory, and LongTermMemory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

from app.ai.copilot.memory.long_term import LongTermMemory
from app.ai.copilot.memory.memory_models import MemoryImportance
from app.ai.copilot.memory.short_term import ShortTermMemory
from app.ai.copilot.memory.working_memory import WorkingMemory

if TYPE_CHECKING:
    from app.ai.copilot.copilot_models import ConversationMessage


class SessionMemoryStore:
    """Combines short-term, working, and long-term memory for a session."""

    def __init__(self, case_id: str = ""):
        self.short_term = ShortTermMemory()
        self.working = WorkingMemory(case_id=case_id)
        self.long_term = LongTermMemory()


class MemoryManager:
    """Central Memory Manager storing memory stores per session."""

    _stores: Dict[str, SessionMemoryStore] = {}

    @classmethod
    def get_or_create_store(cls, session_id: str, case_id: str = "") -> SessionMemoryStore:
        if session_id not in cls._stores:
            cls._stores[session_id] = SessionMemoryStore(case_id=case_id)
        return cls._stores[session_id]

    @classmethod
    def record_turn(cls, session_id: str, role: str, content: str) -> None:
        store = cls.get_or_create_store(session_id)
        store.short_term.add_turn(role, content)

    @classmethod
    def get_recent(cls, session_id: str, limit: int = 10) -> List["ConversationMessage"]:
        """Return recent turns from short-term memory as ConversationMessage objects."""
        from app.ai.copilot.copilot_models import ConversationMessage, MessageRole

        store = cls._stores.get(session_id)
        if not store:
            return []
        turns = store.short_term.get_recent_turns(limit)
        return [
            ConversationMessage(
                role=MessageRole(t.role) if t.role in ("user", "assistant", "system") else MessageRole.USER,
                content=t.content,
            )
            for t in turns
        ]

    @classmethod
    def record_important_fact(
        cls, session_id: str, fact: str, importance: MemoryImportance = MemoryImportance.HIGH
    ) -> None:
        store = cls.get_or_create_store(session_id)
        store.long_term.add_fact(fact, importance=importance)

    @classmethod
    def clear(cls) -> None:
        cls._stores.clear()
