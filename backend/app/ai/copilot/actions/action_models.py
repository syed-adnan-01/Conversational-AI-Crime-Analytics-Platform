"""
Action Metadata and Uniform ActionResult Models.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ActionMetadata(BaseModel):
    """Metadata describing action capabilities and execution requirements."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    required_context: List[str] = Field(default_factory=list)
    estimated_latency_ms: float = 500.0
    requires_llm: bool = True
    requires_retrieval: bool = True
    requires_workspace: bool = False


class ActionResult(BaseModel):
    """Standardized result returned by every action and skill execution."""
    model_config = ConfigDict(from_attributes=True)

    action_name: str
    success: bool = True
    message: str = ""
    data: Optional[Dict[str, Any]] = None
    citations: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    latency_ms: float = 0.0
    error: Optional[str] = None
