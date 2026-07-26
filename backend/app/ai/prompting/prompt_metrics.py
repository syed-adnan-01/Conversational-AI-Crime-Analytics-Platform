"""
Prompt Engine operational metrics tracker.
"""

from typing import Dict


class PromptMetrics:
    """Tracks Prompt Engine execution statistics and operational performance."""

    _cache_hits: int = 0
    _cache_misses: int = 0
    _total_prompts_built: int = 0
    _total_tokens_estimated: int = 0
    _validation_errors: int = 0
    _templates_used: Dict[str, int] = {}

    @classmethod
    def record_cache_hit(cls) -> None:
        cls._cache_hits += 1

    @classmethod
    def record_cache_miss(cls) -> None:
        cls._cache_misses += 1

    @classmethod
    def record_build(cls, template_name: str, token_count: int) -> None:
        cls._total_prompts_built += 1
        cls._total_tokens_estimated += token_count
        cls._templates_used[template_name] = cls._templates_used.get(template_name, 0) + 1

    @classmethod
    def record_validation_error(cls) -> None:
        cls._validation_errors += 1

    @classmethod
    def get_summary(cls) -> Dict[str, float | int | dict]:
        """Returns a snapshot of current engine metrics."""
        total_cache_reqs = cls._cache_hits + cls._cache_misses
        hit_rate = round(cls._cache_hits / total_cache_reqs * 100, 2) if total_cache_reqs > 0 else 0.0
        return {
            "total_prompts_built": cls._total_prompts_built,
            "total_tokens_estimated": cls._total_tokens_estimated,
            "cache_hits": cls._cache_hits,
            "cache_misses": cls._cache_misses,
            "cache_hit_rate_pct": hit_rate,
            "validation_errors": cls._validation_errors,
            "templates_used_count": dict(cls._templates_used),
        }

    @classmethod
    def reset(cls) -> None:
        cls._cache_hits = 0
        cls._cache_misses = 0
        cls._total_prompts_built = 0
        cls._total_tokens_estimated = 0
        cls._validation_errors = 0
        cls._templates_used.clear()
