"""
============================================================
Retrieval Memory Extension Point
============================================================

Module  : AI Conversation Subsystem (Reserved)
Purpose : Extension point for inheriting filters and candidate memories from prior turns.
"""

from typing import Optional
from app.ai.conversation.session_context import SessionContext
from app.ai.retrieval.retrieval_models import RetrievalFilter


class RetrievalMemory:
    """
    Reserved extension slot for contextual filter inheritance.
    """

    @classmethod
    def inherit_filters(
        cls, current_filter: RetrievalFilter, session: Optional[SessionContext]
    ) -> RetrievalFilter:
        if not session:
            return current_filter

        # Inherit active_case_id from session if missing in current_filter
        if not current_filter.case_id and session.active_case_id:
            current_filter.case_id = session.active_case_id

        return current_filter
