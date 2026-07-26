"""
LLM Execution Tracing models.
"""

from datetime import datetime, timezone
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LLMTraceStep(BaseModel):
    """Step record within an LLM request execution trace."""
    model_config = ConfigDict(from_attributes=True)

    step_name: str
    description: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Optional[dict[str, Any]] = None


class LLMTrace(BaseModel):
    """Trace object capturing end-to-end LLM Gateway steps."""
    model_config = ConfigDict(from_attributes=True)

    trace_id: str
    steps: List[LLMTraceStep] = Field(default_factory=list)

    def add_step(self, step_name: str, description: str, details: Optional[dict[str, Any]] = None) -> None:
        self.steps.append(
            LLMTraceStep(step_name=step_name, description=description, details=details)
        )
