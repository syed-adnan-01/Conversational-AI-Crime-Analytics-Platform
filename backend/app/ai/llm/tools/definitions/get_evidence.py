"""
Get Evidence Tool Definition.
"""

from app.ai.llm.tools.tool_models import ToolDefinition


class GetEvidenceDefinition:
    """Tool definition schema for fetching evidence records for a given case."""

    @staticmethod
    def get_definition() -> ToolDefinition:
        return ToolDefinition(
            name="get_evidence",
            description="Fetches recorded physical and digital evidence items for a case_id.",
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
