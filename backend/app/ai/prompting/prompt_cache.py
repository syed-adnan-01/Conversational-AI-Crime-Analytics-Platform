"""
In-memory Prompt Cache for deduplicating identical prompt construction calls.
"""

import hashlib
from typing import Optional
from app.ai.prompting.prompt_metrics import PromptMetrics
from app.ai.prompting.prompt_models import PromptResponse, PromptRequest


class PromptCache:
    """Stores built PromptResponse objects keyed by composite input parameter hashes."""

    _cache: dict[str, PromptResponse] = {}

    @staticmethod
    def generate_cache_key(request: PromptRequest) -> str:
        """Computes composite cache key for a PromptRequest."""
        ctx_hash = request.retrieval_context.provenance.context_hash if request.retrieval_context and request.retrieval_context.provenance else "no_ctx"
        query_str = request.query or ""
        ver = request.version or "1.0.0"
        persona = request.persona.value
        profile = request.profile.value
        intent = request.intent.value
        lang = request.language

        raw = f"{ctx_hash}|{query_str}|{ver}|{persona}|{profile}|{intent}|{lang}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def get(cls, request: PromptRequest) -> Optional[PromptResponse]:
        """Retrieves cached response if present."""
        key = cls.generate_cache_key(request)
        if key in cls._cache:
            PromptMetrics.record_cache_hit()
            return cls._cache[key]
        PromptMetrics.record_cache_miss()
        return None

    @classmethod
    def put(cls, request: PromptRequest, response: PromptResponse) -> None:
        """Stores built response in cache."""
        key = cls.generate_cache_key(request)
        cls._cache[key] = response

    @classmethod
    def clear(cls) -> None:
        """Clears cache entries."""
        cls._cache.clear()
