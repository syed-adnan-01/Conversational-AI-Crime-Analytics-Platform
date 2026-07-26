"""
Copilot Trace — wraps ReasoningTrace with per-request trace collection.
"""

from __future__ import annotations

from typing import Dict, Optional

from app.ai.copilot.copilot_models import ReasoningTrace


class CopilotTrace:
    """In-process trace store mapping turn_id → ReasoningTrace."""

    _traces: Dict[str, ReasoningTrace] = {}

    @classmethod
    def start(cls, session_id: str, turn_id: str) -> ReasoningTrace:
        trace = ReasoningTrace(session_id=session_id, turn_id=turn_id)
        cls._traces[turn_id] = trace
        return trace

    @classmethod
    def get(cls, turn_id: str) -> Optional[ReasoningTrace]:
        return cls._traces.get(turn_id)

    @classmethod
    def finish(cls, turn_id: str) -> Optional[ReasoningTrace]:
        return cls._traces.pop(turn_id, None)

    @classmethod
    def clear(cls) -> None:
        cls._traces.clear()
