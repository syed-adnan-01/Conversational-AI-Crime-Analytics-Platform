"""
Tool Registry managing definitions and routing tool execution calls.
"""

from typing import Dict, List, Optional, Type
from app.ai.llm.tools.definitions import (
    GetEvidenceDefinition,
    GetTimelineDefinition,
    SearchCaseDefinition,
)
from app.ai.llm.tools.executors import GetTimelineExecutor, SearchCaseExecutor
from app.ai.llm.tools.tool_models import ToolCall, ToolDefinition, ToolResult


class ToolRegistry:
    """Registry maintaining declarative ToolDefinitions and dispatching ToolCalls to Executors."""

    _definitions: Dict[str, ToolDefinition] = {}

    @classmethod
    def _initialize(cls) -> None:
        if not cls._definitions:
            cls.register_definition(SearchCaseDefinition.get_definition())
            cls.register_definition(GetTimelineDefinition.get_definition())
            cls.register_definition(GetEvidenceDefinition.get_definition())

    @classmethod
    def register_definition(cls, definition: ToolDefinition) -> None:
        cls._definitions[definition.name] = definition

    @classmethod
    def list_definitions(cls) -> List[ToolDefinition]:
        cls._initialize()
        return list(cls._definitions.values())

    @classmethod
    def get_definition(cls, name: str) -> Optional[ToolDefinition]:
        cls._initialize()
        return cls._definitions.get(name)

    @classmethod
    def execute_tool(cls, tool_call: ToolCall) -> ToolResult:
        """Dispatches ToolCall to appropriate ToolExecutor."""
        cls._initialize()
        if tool_call.tool_name == "search_case":
            return SearchCaseExecutor.execute(tool_call)
        elif tool_call.tool_name == "get_timeline":
            return GetTimelineExecutor.execute(tool_call)

        return ToolResult(
            call_id=tool_call.call_id,
            tool_name=tool_call.tool_name,
            success=False,
            error=f"No registered executor for tool '{tool_call.tool_name}'",
        )
