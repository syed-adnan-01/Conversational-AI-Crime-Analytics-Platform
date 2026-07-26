"""
Abstract Base Tool Class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from app.ai.llm.tools.tool_models import ToolCall, ToolDefinition, ToolResult


class BaseTool(ABC):
    """Abstract interface combining tool definition schema and execution contract."""

    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """Returns declarative ToolDefinition schema."""
        pass

    @abstractmethod
    def execute(self, tool_call: ToolCall) -> ToolResult:
        """Executes tool logic and returns ToolResult."""
        pass
