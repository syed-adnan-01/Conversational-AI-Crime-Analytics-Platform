"""
Search Case Tool Definition.
"""

from app.ai.llm.tools.tool_models import ToolDefinition


class SearchCaseDefinition:
    """Tool definition schema for searching cases by keywords or query."""

    @staticmethod
    def get_definition() -> ToolDefinition:
        return ToolDefinition(
            name="search_case",
            description="Searches active FIR and crime cases matching specified keywords or query terms.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query terms e.g. cyber theft, robbery",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of matching cases to return",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        )
