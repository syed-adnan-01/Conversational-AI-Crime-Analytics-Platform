"""
After Response Middleware for metrics recording, auditing, and caching.
"""

from app.ai.llm.llm_audit import LLMAuditEntry, LLMAuditTrail
from app.ai.llm.llm_cache import LLMCache
from app.ai.llm.llm_metrics import LLMMetrics
from app.ai.llm.llm_models import LLMRequest, LLMResponse


class AfterResponseMiddleware:
    """Processes LLMResponse after generation."""

    @classmethod
    def process(cls, request: LLMRequest, response: LLMResponse) -> LLMResponse:
        """Records metrics, audit entry, and caches output."""
        # 1. Record Metrics
        if not response.cached:
            LLMMetrics.record_request(
                provider=response.provider,
                prompt_tokens=response.token_usage.prompt_tokens,
                completion_tokens=response.token_usage.completion_tokens,
                cost=response.cost,
                cached=False,
            )

        # 2. Record Audit Entry
        audit_entry = LLMAuditEntry(
            request_id=response.request_id,
            response_id=response.response_id,
            provider=response.provider,
            model=response.model,
            conversation_id=request.conversation_id,
            tokens_used=response.token_usage.total_tokens,
            cost_usd=response.cost,
            latency_ms=response.latency_ms,
            safety_passed=response.safety_passed,
        )
        LLMAuditTrail.record(audit_entry)

        # 3. Store in Cache if non-cached and cache enabled
        if not response.cached:
            LLMCache.put(request, response)

        return response
