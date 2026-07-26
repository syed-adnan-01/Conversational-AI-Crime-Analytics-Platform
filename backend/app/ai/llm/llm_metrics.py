"""
LLM Gateway Operational Metrics Tracker.
"""

from typing import Dict, Any


class LLMMetrics:
    """Tracks latency, token usage, cost, and provider execution statistics."""

    _total_requests: int = 0
    _total_prompt_tokens: int = 0
    _total_completion_tokens: int = 0
    _total_cost_usd: float = 0.0
    _cache_hits: int = 0
    _cache_misses: int = 0
    _provider_counts: Dict[str, int] = {}
    _errors_count: int = 0

    @classmethod
    def record_request(
        cls, provider: str, prompt_tokens: int, completion_tokens: int, cost: float, cached: bool = False
    ) -> None:
        cls._total_requests += 1
        cls._total_prompt_tokens += prompt_tokens
        cls._total_completion_tokens += completion_tokens
        cls._total_cost_usd += cost
        cls._provider_counts[provider] = cls._provider_counts.get(provider, 0) + 1
        if cached:
            cls._cache_hits += 1
        else:
            cls._cache_misses += 1

    @classmethod
    def record_error(cls) -> None:
        cls._errors_count += 1

    @classmethod
    def get_summary(cls) -> Dict[str, Any]:
        """Returns a snapshot of Gateway operational metrics."""
        total_reqs = max(1, cls._total_requests)
        return {
            "total_requests": cls._total_requests,
            "total_prompt_tokens": cls._total_prompt_tokens,
            "total_completion_tokens": cls._total_completion_tokens,
            "total_tokens": cls._total_prompt_tokens + cls._total_completion_tokens,
            "total_cost_usd": round(cls._total_cost_usd, 6),
            "cache_hits": cls._cache_hits,
            "cache_misses": cls._cache_misses,
            "cache_hit_rate_pct": round(cls._cache_hits / max(1, cls._cache_hits + cls._cache_misses) * 100, 2),
            "error_count": cls._errors_count,
            "provider_breakdown": dict(cls._provider_counts),
        }

    @classmethod
    def reset(cls) -> None:
        cls._total_requests = 0
        cls._total_prompt_tokens = 0
        cls._total_completion_tokens = 0
        cls._total_cost_usd = 0.0
        cls._cache_hits = 0
        cls._cache_misses = 0
        cls._errors_count = 0
        cls._provider_counts.clear()
