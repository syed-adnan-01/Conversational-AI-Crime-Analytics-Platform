"""
Search Case Tool Executor.
"""

from app.ai.llm.tools.tool_models import ToolCall, ToolResult


class SearchCaseExecutor:
    """Executes search_case tool invocations against database or search indices."""

    @staticmethod
    def execute(tool_call: ToolCall) -> ToolResult:
        query = tool_call.arguments.get("query", "")
        limit = tool_call.arguments.get("limit", 5)

        # Mock result execution
        mock_output = [
            {"case_id": "CM-881", "fir_number": "FIR-2026-001", "summary": f"Case matching query: {query}"}
        ][:limit]

        return ToolResult(
            call_id=tool_call.call_id,
            tool_name="search_case",
            success=True,
            output=mock_output,
        )
