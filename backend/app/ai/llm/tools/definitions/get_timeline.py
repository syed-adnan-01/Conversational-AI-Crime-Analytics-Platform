"""
Get Timeline Tool Definition.
"""

from app.ai.llm.tools.tool_models import ToolDefinition


class GetTimelineDefinition:
    """Tool definition schema for retrieving chronologically ordered case timeline events."""

    @staticmethod
    def get_definition() -> ToolDefinition:
        return ToolDefinition(
            name="get_timeline",
            description="Retrieves chronological timeline events for a given case_id.",
            parameters={
                "type": "object",
                "properties": {
                    "case_id": {
                        "type": "string",
                        "description": "Unique case ID e.g. CM-101",
                    }
                },
                "required": ["case_id"],
            },
        )
