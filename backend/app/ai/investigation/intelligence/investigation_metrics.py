"""Investigation metrics collector."""

from __future__ import annotations

from app.ai.investigation.analysis.confidence import level_from_score
from app.ai.investigation.intelligence.investigation_models import InvestigationMetrics


class InvestigationMetricsCollector:
    """Tracks the latest investigation metrics snapshot."""

    def __init__(self) -> None:
        self._metrics = InvestigationMetrics()

    def update(
        self,
        *,
        retrieval_confidence: float | None = None,
        evidence_confidence: float | None = None,
        recommendation_confidence: float | None = None,
        overall_confidence: float | None = None,
        retrieval_time_ms: float | None = None,
        analysis_time_ms: float | None = None,
        graph_time_ms: float | None = None,
        total_time_ms: float | None = None,
        cache_hit: bool | None = None,
        audits_recorded: int | None = None,
    ) -> InvestigationMetrics:
        if retrieval_confidence is not None:
            self._metrics.retrieval_confidence = retrieval_confidence
        if evidence_confidence is not None:
            self._metrics.evidence_confidence = evidence_confidence
        if recommendation_confidence is not None:
            self._metrics.recommendation_confidence = recommendation_confidence
        if overall_confidence is not None:
            self._metrics.overall_confidence = overall_confidence
            self._metrics.confidence_level = level_from_score(overall_confidence)
        if retrieval_time_ms is not None:
            self._metrics.retrieval_time_ms = retrieval_time_ms
        if analysis_time_ms is not None:
            self._metrics.analysis_time_ms = analysis_time_ms
        if graph_time_ms is not None:
            self._metrics.graph_time_ms = graph_time_ms
        if total_time_ms is not None:
            self._metrics.total_time_ms = total_time_ms
        if cache_hit is not None:
            self._metrics.cache_hit = cache_hit
        if audits_recorded is not None:
            self._metrics.audits_recorded = audits_recorded
        return self._metrics

    def snapshot(self) -> InvestigationMetrics:
        return self._metrics.model_copy(deep=True)
