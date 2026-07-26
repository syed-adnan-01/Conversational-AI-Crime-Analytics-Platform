"""
High-Level LLM Service Facade.
"""

from typing import AsyncGenerator, Dict, Any, List

from app.ai.llm.llm_cache import LLMCache
from app.ai.llm.llm_gateway import LLMGateway
from app.ai.llm.llm_metrics import LLMMetrics
from app.ai.llm.llm_models import LLMRequest, LLMResponse
from app.ai.llm.llm_registry import ProviderRegistry
from app.ai.llm.streaming import StreamingResponseFormatter
from app.ai.prompting.prompt_models import PromptResponse


class LLMService:
    """Service wrapper for LLM Gateway operations."""

    @classmethod
    def generate(cls, request: LLMRequest) -> LLMResponse:
        """Executes LLM request."""
        return LLMGateway.generate(request)

    @classmethod
    def generate_from_prompt_response(
        cls, prompt_response: PromptResponse, provider: str | None = None
    ) -> LLMResponse:
        """Convenience method accepting a Phase 3.4 PromptResponse object directly."""
        request = LLMRequest(
            prompt_response=prompt_response,
            prompt=prompt_response.assembled_prompt,
            provider=provider,
            response_schema=prompt_response.output_schema,
        )
        return LLMGateway.generate(request)

    @classmethod
    async def generate_stream_sse(
        cls, request: LLMRequest
    ) -> AsyncGenerator[str, None]:
        """Returns SSE formatted stream."""
        raw_stream = LLMGateway.generate_stream(request)
        async for sse_chunk in StreamingResponseFormatter.format_sse_stream(raw_stream):
            yield sse_chunk

    @classmethod
    def get_providers(cls) -> List[str]:
        return ProviderRegistry.list_providers()

    @classmethod
    def get_capabilities(cls, provider_name: str | None = None) -> Dict[str, Any]:
        return LLMGateway.get_capabilities(provider_name)

    @classmethod
    def get_metrics(cls) -> Dict[str, Any]:
        return LLMMetrics.get_summary()

    @classmethod
    def clear_cache(cls) -> None:
        LLMCache.clear()
