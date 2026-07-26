"""
Copilot Metrics — lightweight counters and histograms for observability.
"""

import threading
from collections import defaultdict
from typing import Dict


class CopilotMetrics:
    """Thread-safe in-memory metrics collector."""

    _lock = threading.Lock()
    _counters: Dict[str, int] = defaultdict(int)
    _latency_sums: Dict[str, float] = defaultdict(float)
    _latency_counts: Dict[str, int] = defaultdict(int)

    @classmethod
    def increment(cls, key: str, amount: int = 1) -> None:
        with cls._lock:
            cls._counters[key] += amount

    @classmethod
    def record_latency(cls, operation: str, latency_ms: float) -> None:
        with cls._lock:
            cls._latency_sums[operation] += latency_ms
            cls._latency_counts[operation] += 1

    @classmethod
    def get_counter(cls, key: str) -> int:
        return cls._counters.get(key, 0)

    @classmethod
    def get_avg_latency(cls, operation: str) -> float:
        count = cls._latency_counts.get(operation, 0)
        if count == 0:
            return 0.0
        return cls._latency_sums[operation] / count

    @classmethod
    def snapshot(cls) -> dict:
        with cls._lock:
            return {
                "counters": dict(cls._counters),
                "avg_latencies_ms": {
                    op: (cls._latency_sums[op] / cls._latency_counts[op])
                    for op in cls._latency_counts
                },
            }

    @classmethod
    def reset(cls) -> None:
        with cls._lock:
            cls._counters.clear()
            cls._latency_sums.clear()
            cls._latency_counts.clear()
