"""
Prompt Fingerprint Response Cache.
"""

import hashlib
from typing import Optional
from app.ai.llm.llm_metrics import LLMMetrics
from app.ai.llm.llm_models import LLMRequest, LLMResponse


class LLMCache:
    """In-memory cache for storing and deduplicating identical LLM gateway responses."""

    _cache: dict[str, LLMResponse] = {}

    @staticmethod
    def generate_key(request: LLMRequest) -> str:
        """Computes cache key based on prompt, provider, model, temperature, and top_p."""
        prompt_str = request.prompt or (request.prompt_response.user_prompt if request.prompt_response else "")
        sys_str = request.system_prompt or (request.prompt_response.system_prompt if request.prompt_response else "")
        provider = request.provider or "quickml"
        model = request.model or "default"
        temp = str(request.temperature)
        top_p = str(request.top_p)

        raw = f"{sys_str}|{prompt_str}|{provider}|{model}|{temp}|{top_p}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def get(cls, request: LLMRequest) -> Optional[LLMResponse]:
        """Returns cached response if present."""
        key = cls.generate_key(request)
        if key in cls._cache:
            resp = cls._cache[key]
            # Copy and mark cached = True
            cached_resp = resp.model_copy(update={"cached": True})
            LLMMetrics.record_request(
                provider=cached_resp.provider,
                prompt_tokens=cached_resp.token_usage.prompt_tokens,
                completion_tokens=cached_resp.token_usage.completion_tokens,
                cost=0.0,
                cached=True,
            )
            return cached_resp
        return None

    @classmethod
    def put(cls, request: LLMRequest, response: LLMResponse) -> None:
        """Stores built response in cache."""
        key = cls.generate_key(request)
        cls._cache[key] = response

    @classmethod
    def clear(cls) -> None:
        """Clears cache entries."""
        cls._cache.clear()
