"""
Get Timeline Tool Executor.
"""

from app.ai.llm.tools.tool_models import ToolCall, ToolResult


class GetTimelineExecutor:
    """Executes get_timeline tool calls."""

    @staticmethod
    def execute(tool_call: ToolCall) -> ToolResult:
        case_id = tool_call.arguments.get("case_id", "UNKNOWN")

        mock_events = [
            {"event_id": "EVT-01", "timestamp": "2026-07-20 10:00:00", "description": f"Incident reported for {case_id}"},
            {"event_id": "EVT-02", "timestamp": "2026-07-20 14:30:00", "description": "Evidence collected at scene"},
        ]

        return ToolResult(
            call_id=tool_call.call_id,
            tool_name="get_timeline",
            success=True,
            output=mock_events,
        )
