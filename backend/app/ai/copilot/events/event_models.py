"""
Copilot Event Models.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    """Supported AI Copilot Event types."""
    PLANNER_STARTED = "PLANNER_STARTED"
    PLANNER_COMPLETED = "PLANNER_COMPLETED"
    RETRIEVAL_STARTED = "RETRIEVAL_STARTED"
    RETRIEVAL_COMPLETED = "RETRIEVAL_COMPLETED"
    PROMPT_GENERATED = "PROMPT_GENERATED"
    LLM_STARTED = "LLM_STARTED"
    LLM_COMPLETED = "LLM_COMPLETED"
    ACTION_EXECUTED = "ACTION_EXECUTED"
    SKILL_EXECUTED = "SKILL_EXECUTED"
    WORKFLOW_EXECUTED = "WORKFLOW_EXECUTED"
    CONVERSATION_UPDATED = "CONVERSATION_UPDATED"
    WORKSPACE_UPDATED = "WORKSPACE_UPDATED"


class CopilotEvent(BaseModel):
    """Pub/Sub event payload model."""
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    session_id: str
    event_type: EventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)
