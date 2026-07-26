"""Operational metrics for QuickML retrieval."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock


class QuickMLMetrics:
    _lock = RLock()
    _requests: int = 0
    _successes: int = 0
    _failures: int = 0
    _cache_hits: int = 0
    _cache_misses: int = 0
    _total_latency_ms: float = 0.0
    _last_query_time: datetime | None = None
    _last_error: str | None = None

    @classmethod
    def record_success(cls, latency_ms: int, cached: bool = False) -> None:
        with cls._lock:
            cls._requests += 1
            cls._successes += 1
            cls._total_latency_ms += latency_ms
            cls._last_query_time = datetime.now(timezone.utc)
            if cached:
                cls._cache_hits += 1
            else:
                cls._cache_misses += 1

    @classmethod
    def record_failure(cls, error: str) -> None:
        with cls._lock:
            cls._requests += 1
            cls._failures += 1
            cls._last_error = error
            cls._last_query_time = datetime.now(timezone.utc)

    @classmethod
    def snapshot(cls) -> dict[str, object]:
        with cls._lock:
            avg_latency = cls._total_latency_ms / cls._successes if cls._successes else 0.0
            return {
                "requests": cls._requests,
                "successes": cls._successes,
                "failures": cls._failures,
                "cache_hits": cls._cache_hits,
                "cache_misses": cls._cache_misses,
                "average_latency_ms": round(avg_latency, 2),
                "last_query_time": cls._last_query_time.isoformat() if cls._last_query_time else None,
                "last_error": cls._last_error,
            }

    @classmethod
    def last_query_time(cls) -> datetime | None:
        with cls._lock:
            return cls._last_query_time

    @classmethod
    def reset(cls) -> None:
        with cls._lock:
            cls._requests = 0
            cls._successes = 0
            cls._failures = 0
            cls._cache_hits = 0
            cls._cache_misses = 0
            cls._total_latency_ms = 0.0
            cls._last_query_time = None
            cls._last_error = None