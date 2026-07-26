"""
Copilot Session Models.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ConversationStatus(str, Enum):
    """Session operational status."""
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class ConversationMessage(BaseModel):
    """Message object inside a Copilot Session."""
    model_config = ConfigDict(from_attributes=True)

    message_id: str
    session_id: str
    role: str
    content: str
    message_type: str = "text"
    citations: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CopilotSession(BaseModel):
    """Copilot Session model."""
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    case_id: str
    user_id: str
    mode: str = "ASSISTANT"
    status: ConversationStatus = ConversationStatus.ACTIVE
    tags: List[str] = Field(default_factory=list)
    messages: List[ConversationMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
