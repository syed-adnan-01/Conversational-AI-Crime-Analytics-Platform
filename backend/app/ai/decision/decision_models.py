from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

class DecisionStatus(str, Enum): DRAFT='Draft'; PENDING_REVIEW='Pending Review'; APPROVED='Approved'; REJECTED='Rejected'; NEEDS_MORE_EVIDENCE='Needs More Evidence'
class EvidenceProvenance(BaseModel): source_type: str; source_id: str; description: str = ''; module: str = ''; confidence: float | None = None
class ConfidenceBreakdown(BaseModel): retrieval_confidence: float = 0; evidence_quality: float = 0; legal_confidence: float = 0; timeline_consistency: float = 0; graph_confidence: float = 0; prediction_reliability: float = 0; agent_agreement: float = 0; overall_confidence: float = 0; explanation: str = ''
class ReasoningStep(BaseModel): statement: str; evidence_ids: list[str] = Field(default_factory=list); module: str = ''; confidence: float = 0
class Recommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f'decision-rec-{uuid4().hex}'); title: str; priority: int = Field(ge=1, le=5); explanation: str; supporting_evidence: list[EvidenceProvenance] = Field(default_factory=list); conflicting_evidence: list[EvidenceProvenance] = Field(default_factory=list); retrieved_chunk_references: list[str] = Field(default_factory=list); confidence: ConfidenceBreakdown; recommended_next_step: str; legal_references: list[str] = Field(default_factory=list); originating_modules: list[str] = Field(default_factory=list); originating_agents: list[str] = Field(default_factory=list); reasoning_chain: list[ReasoningStep] = Field(default_factory=list); uncertainty_indicators: list[str] = Field(default_factory=list); status: DecisionStatus = DecisionStatus.DRAFT
class Hypothesis(BaseModel): description: str; supporting_evidence: list[EvidenceProvenance] = Field(default_factory=list); contradicting_evidence: list[EvidenceProvenance] = Field(default_factory=list); confidence: float = 0; reasoning_summary: str = ''
class DecisionRequest(BaseModel): case_id: str; query: str | None = None; source_outputs: dict[str, Any] = Field(default_factory=dict); status: DecisionStatus = DecisionStatus.DRAFT
class DecisionResponse(BaseModel): decision_id: str = Field(default_factory=lambda: f'decision-{uuid4().hex}'); case_id: str; recommendations: list[Recommendation] = Field(default_factory=list); hypotheses: list[Hypothesis] = Field(default_factory=list); confidence: ConfidenceBreakdown = Field(default_factory=ConfidenceBreakdown); provenance: list[EvidenceProvenance] = Field(default_factory=list); status: DecisionStatus = DecisionStatus.DRAFT; generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
class DecisionMetrics(BaseModel): analyses: int = 0; cache_hits: int = 0; failures: int = 0; last_duration_ms: float = 0
class DecisionTrace(BaseModel): decision_id: str; event: str; details: dict[str, Any] = Field(default_factory=dict); timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
