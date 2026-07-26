from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

class Feedback(BaseModel): rating: int | None = Field(default=None, ge=1, le=5); thumbs_up: bool | None = None; comment: str | None = None; accepted_recommendation_ids: list[str] = Field(default_factory=list); rejected_recommendation_ids: list[str] = Field(default_factory=list)
class EvaluationRequest(BaseModel): module: str; output: dict[str, Any] = Field(default_factory=dict); expected: dict[str, Any] = Field(default_factory=dict); feedback: Feedback | None = None; request_id: str = Field(default_factory=lambda: f'eval-{uuid4().hex}')
class QualityIssue(BaseModel): category: str; description: str; reference: str | None = None; severity: str = 'medium'
class EvaluationScores(BaseModel): retrieval: dict[str, float] = Field(default_factory=dict); prompt: dict[str, float] = Field(default_factory=dict); llm: dict[str, float] = Field(default_factory=dict); decision: dict[str, float] = Field(default_factory=dict); overall: float = 0
class EvaluationResponse(BaseModel): evaluation_id: str = Field(default_factory=lambda: f'evaluation-{uuid4().hex}'); module: str; scores: EvaluationScores; issues: list[QualityIssue] = Field(default_factory=list); feedback: Feedback | None = None; created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
class BenchmarkSuite(BaseModel): name: str; cases: list[EvaluationRequest] = Field(default_factory=list)
class BenchmarkReport(BaseModel): suite: str; total: int; average_score: float; evaluations: list[EvaluationResponse] = Field(default_factory=list)
class EvaluationMetrics(BaseModel): evaluations: int = 0; successful: int = 0; failures: int = 0; cache_hits: int = 0; total_latency_ms: float = 0
