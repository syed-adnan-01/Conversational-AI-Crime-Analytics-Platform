"""
============================================================
Retrieval Benchmark Evaluator
============================================================

Module  : AI Evaluation Subsystem
Purpose : Benchmark runner evaluating retrieval precision, recall, and latency metrics.
"""

from typing import Any
from pydantic import BaseModel, ConfigDict
from app.ai.evaluation.metrics import RetrievalMetrics


class BenchmarkResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_queries: int
    mean_precision_at_k: float
    mean_recall_at_k: float
    mrr: float
    average_latency_ms: float


class RetrievalBenchmark:
    """
    Evaluator executing test benchmarks against evaluation datasets.
    """

    @classmethod
    def evaluate(cls, query_eval_cases: list[dict[str, Any]]) -> BenchmarkResult:
        precisions: list[float] = []
        recalls: list[float] = []
        rrs: list[float] = []
        latencies: list[float] = []

        for item in query_eval_cases:
            retrieved = item.get("retrieved_ids", [])
            relevant = set(item.get("relevant_ids", []))
            k = item.get("k", 5)
            lat = item.get("latency_ms", 0.0)

            precisions.append(RetrievalMetrics.precision_at_k(retrieved, relevant, k))
            recalls.append(RetrievalMetrics.recall_at_k(retrieved, relevant, k))
            rrs.append(RetrievalMetrics.mean_reciprocal_rank(retrieved, relevant))
            latencies.append(lat)

        n = len(query_eval_cases) or 1
        return BenchmarkResult(
            total_queries=len(query_eval_cases),
            mean_precision_at_k=round(sum(precisions) / n, 4),
            mean_recall_at_k=round(sum(recalls) / n, 4),
            mrr=round(sum(rrs) / n, 4),
            average_latency_ms=round(sum(latencies) / n, 2),
        )
