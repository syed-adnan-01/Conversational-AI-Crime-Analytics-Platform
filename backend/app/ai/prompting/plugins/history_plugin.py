"""
History Plugin for formatting previous conversation turns into prompt variables.
"""

from app.ai.prompting.plugins.base import PromptPlugin
from app.ai.prompting.prompt_models import PromptRequest
from app.ai.prompting.prompt_variables import PromptVariables


class HistoryPlugin(PromptPlugin):
    name: str = "history_plugin"

    def before_render(self, request: PromptRequest, variables: PromptVariables) -> None:
        """Injects multi-turn conversation history into prompt variables if present."""
        if request.history:
            turns = [
                f"{turn.role.upper()}: {turn.content}"
                for turn in request.history
            ]
            variables.history = "### PREVIOUS CONVERSATION HISTORY\n" + "\n".join(turns)
