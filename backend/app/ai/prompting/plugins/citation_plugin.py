"""
Citation Plugin for formatting document evidence citations into prompt variables.
"""

from app.ai.prompting.plugins.base import PromptPlugin
from app.ai.prompting.prompt_models import PromptRequest
from app.ai.prompting.prompt_variables import PromptVariables


class CitationPlugin(PromptPlugin):
    name: str = "citation_plugin"

    def before_render(self, request: PromptRequest, variables: PromptVariables) -> None:
        """Injects explicit citation instructions if retrieval context has chunks."""
        if request.retrieval_context and request.retrieval_context.chunks:
            chunk_citations = [
                f"[{c.metadata.get('chunk_id', idx)}] {c.metadata.get('source_type', 'DOC')} (Case: {c.metadata.get('case_id', 'N/A')})"
                for idx, c in enumerate(request.retrieval_context.chunks, 1)
            ]
            variables.citations = "### EVIDENCE SOURCE CITATIONS\n" + "\n".join(chunk_citations)
