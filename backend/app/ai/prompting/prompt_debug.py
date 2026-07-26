"""
Prompt Debug Instrumentation and Build Execution Trace models.
"""

from datetime import datetime, timezone
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PromptTraceStep(BaseModel):
    """Step record within a prompt build trace execution."""
    model_config = ConfigDict(from_attributes=True)

    step_name: str
    description: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Optional[dict[str, Any]] = None


class PromptTrace(BaseModel):
    """Execution build trace recording lifecycle execution flow."""
    model_config = ConfigDict(from_attributes=True)

    trace_id: str
    steps: List[PromptTraceStep] = Field(default_factory=list)

    def add_step(self, step_name: str, description: str, details: Optional[dict[str, Any]] = None) -> None:
        self.steps.append(
            PromptTraceStep(step_name=step_name, description=description, details=details)
        )


class PromptDebug(BaseModel):
    """Debug instrumentation information for troubleshooting generated prompts."""
    model_config = ConfigDict(from_attributes=True)

    template_name: str
    template_version: str
    sections_used: List[str]
    token_count_breakdown: dict[str, int]
    context_hash: Optional[str] = None
    retrieval_id: Optional[str] = None
    placeholders_resolved: List[str]
    optimization_reduction_chars: int = 0
    build_time_ms: float = 0.0
