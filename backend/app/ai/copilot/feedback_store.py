"""
Feedback Store for conversation quality tracking.
"""

import threading
from typing import Dict, List

from app.ai.copilot.copilot_models import CopilotFeedback


class FeedbackStore:
    """Thread-safe in-memory feedback store keyed by session_id."""

    def __init__(self) -> None:
        self._store: Dict[str, List[CopilotFeedback]] = {}
        self._lock = threading.Lock()

    def record(self, feedback: CopilotFeedback) -> CopilotFeedback:
        with self._lock:
            self._store.setdefault(feedback.session_id, []).append(feedback)
        return feedback

    def get_by_session(self, session_id: str) -> List[CopilotFeedback]:
        return list(self._store.get(session_id, []))

    def get_all(self) -> List[CopilotFeedback]:
        all_fb: List[CopilotFeedback] = []
        for items in self._store.values():
            all_fb.extend(items)
        return all_fb

    def count(self) -> int:
        return sum(len(v) for v in self._store.values())
