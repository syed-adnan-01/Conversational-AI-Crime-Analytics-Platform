"""
Response Factory — constructs CopilotResponse from raw LLM output and plan metadata.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from app.ai.copilot.copilot_models import (
    AgentState,
    CopilotResponse,
    ExecutionPlan,
)


class ResponseFactory:
    """Assembles a strongly-typed CopilotResponse from LLM provider output."""

    @staticmethod
    def build(
        *,
        session_id: str,
        case_id: str,
        answer: str,
        plan: Optional[ExecutionPlan] = None,
        reasoning_trace: Optional[list] = None,
        provider_used: Optional[str] = None,
        confidence: float = 0.0,
        latency_ms: Optional[int] = None,
        citations: Optional[list[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CopilotResponse:
        response_metadata = metadata.copy() if metadata else {}
        if citations is not None:
            response_metadata.setdefault("citations", citations)
        return CopilotResponse(
            session_id=session_id,
            case_id=case_id,
            answer=answer,
            plan=plan,
            reasoning_trace=reasoning_trace or [],
            agent_state=AgentState.COMPLETE,
            confidence=confidence,
            provider_used=provider_used,
            latency_ms=latency_ms,
            citations=citations or [],
            metadata=response_metadata,
        )

    @staticmethod
    def build_error(
        *,
        session_id: str,
        case_id: str,
        error_message: str,
        plan: Optional[ExecutionPlan] = None,
    ) -> CopilotResponse:
        return CopilotResponse(
            session_id=session_id,
            case_id=case_id,
            answer=f"I encountered an error: {error_message}",
            plan=plan,
            agent_state=AgentState.FAILED,
            confidence=0.0,
            citations=[],
        )
