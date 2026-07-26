"""
Short-Term Memory Manager storing recent turns.
"""

from typing import List
from pydantic import BaseModel, Field
from app.ai.prompting.prompt_models import ConversationTurn


class ShortTermMemory(BaseModel):
    """Stores last N conversation turns."""

    turns: List[ConversationTurn] = Field(default_factory=list)
    max_turns: int = 15

    def add_turn(self, role: str, content: str) -> None:
        self.turns.append(ConversationTurn(role=role, content=content))
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns :]

    def get_recent_turns(self, limit: int = 10) -> List[ConversationTurn]:
        return self.turns[-limit:]
