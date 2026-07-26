from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"message-{uuid4().hex}"); topic: str; sender: str; payload: dict[str, Any] = Field(default_factory=dict); timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
