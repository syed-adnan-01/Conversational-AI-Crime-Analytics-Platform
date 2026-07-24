"""
============================================================
Session Context Extension Point
============================================================

Module  : AI Conversation Subsystem (Reserved)
Purpose : Extension point for tracking multi-turn conversational session context.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class SessionContext(BaseModel):
    """
    Reserved extension slot holding conversational context across interaction turns.
    """
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    active_case_id: Optional[str] = None
    active_accused_id: Optional[str] = None
    previous_query: Optional[str] = None
    previous_retrieval_id: Optional[str] = None
