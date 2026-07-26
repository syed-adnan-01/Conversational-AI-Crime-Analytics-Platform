"""
Data Models for Tool Calling Interfaces.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field


class ToolDefinition(BaseModel):
    """Declarative specification of a function/tool consumable by LLMs."""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Tool name, e.g. search_case")
    description: str = Field(..., description="Detailed capability description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="JSON Schema parameter specifications")


class ToolCall(BaseModel):
    """Model representing an LLM function call invocation."""
    model_config = ConfigDict(from_attributes=True)

    call_id: str
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """Model representing the execution result of a ToolCall."""
    model_config = ConfigDict(from_attributes=True)

    call_id: str
    tool_name: str
    success: bool = True
    output: Any = None
    error: Optional[str] = None
