"""
Enterprise LLM Gateway.
Main entry point for invoking LLM providers with cache, retries, validation, and metrics.
"""

from typing import AsyncGenerator, Dict, Any

from app.ai.llm.config import llm_config
from app.ai.llm.llm_cache import LLMCache
from app.ai.llm.llm_models import LLMRequest, LLMResponse
from app.ai.llm.llm_registry import ProviderRegistry
from app.ai.llm.llm_validator import LLMValidator
from app.ai.llm.middleware.after_response import AfterResponseMiddleware
from app.ai.llm.middleware.before_request import BeforeRequestMiddleware
from app.ai.llm.retry import RetryEngine


class LLMGateway:
    """Enterprise Gateway facade encapsulating provider routing and resiliency pipelines."""

    @classmethod
    def generate(cls, request: LLMRequest) -> LLMResponse:
        """Executes full request pipeline: Pre-Middleware -> Cache -> Retry Provider Call -> Validation -> Post-Middleware."""
        # 1. Before Request Middleware
        request = BeforeRequestMiddleware.process(request)

        # 2. Cache Lookup
        if llm_config.ENABLE_CACHE:
            cached_resp = LLMCache.get(request)
            if cached_resp:
                return cached_resp

        # 3. Provider Lookup & Execution via Retry Engine
        provider = ProviderRegistry.get(request.provider)

        def _execute():
            return provider.generate(request)

        raw_response: LLMResponse = RetryEngine.execute_with_retry(
            _execute, max_retries=llm_config.MAX_RETRIES
        )

        # 4. Response Validation (Safety + Schema Parsing)
        validated_response = LLMValidator.validate_response(
            raw_response, response_schema=request.response_schema
        )

        # 5. After Response Middleware
        final_response = AfterResponseMiddleware.process(request, validated_response)
        return final_response

    @classmethod
    async def generate_stream(cls, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Generates streaming text output chunks as AsyncGenerator."""
        request = BeforeRequestMiddleware.process(request)
        provider = ProviderRegistry.get(request.provider)

        async for chunk in provider.generate_stream(request):
            yield chunk

    @classmethod
    def get_capabilities(cls, provider_name: str | None = None) -> Dict[str, Any]:
        """Returns active provider capability matrix and model details."""
        provider = ProviderRegistry.get(provider_name)
        return {
            "provider": provider.provider_name,
            "capabilities": provider.capabilities.model_dump(),
            "model_info": provider.get_model_info(),
        }
