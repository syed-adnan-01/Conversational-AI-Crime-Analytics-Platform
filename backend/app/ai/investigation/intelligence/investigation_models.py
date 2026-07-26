"""Pydantic models for the AI Investigation Intelligence layer."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ConfidenceLevel(str, Enum):
    """Confidence buckets used across the investigation layer."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class InvestigationRequest(BaseModel):
    """Input payload for investigation analysis endpoints."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: Optional[str] = None
    query: Optional[str] = None
    top_k: int = 5
    include_graph: bool = True
    include_llm_reasoning: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class SimilarityResult(BaseModel):
    """Similarity result between the target case/query and a candidate case."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: str
    case_no: Optional[str] = None
    similarity_score: float = 0.0
    shared_evidence: list[str] = Field(default_factory=list)
    shared_accused: list[str] = Field(default_factory=list)
    shared_sections: list[str] = Field(default_factory=list)
    shared_mo: list[str] = Field(default_factory=list)
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    reason: str = ""
    confidence: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW


class EvidenceInsight(BaseModel):
    """Per-evidence analysis result."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    evidence_id: str
    title: str
    confidence: float = 0.0
    strength: float = 0.0
    importance: float = 0.0
    chain_of_custody_score: float = 0.0
    duplicate_detection: bool = False
    missing_evidence: list[str] = Field(default_factory=list)
    weak_evidence: list[str] = Field(default_factory=list)
    conflicting_evidence: list[str] = Field(default_factory=list)
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    supporting_facts: list[str] = Field(default_factory=list)


class TimelineInsight(BaseModel):
    """Chronological analysis result for a case timeline."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    missing_events: list[str] = Field(default_factory=list)
    large_gaps: list[str] = Field(default_factory=list)
    impossible_sequences: list[str] = Field(default_factory=list)
    time_conflicts: list[str] = Field(default_factory=list)
    chronological_inconsistencies: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    supporting_facts: list[str] = Field(default_factory=list)


class Contradiction(BaseModel):
    """Contradiction between statements, evidence, timeline, or notes."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    contradiction_id: str
    source_entities: list[str] = Field(default_factory=list)
    description: str
    confidence: float = 0.0
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    supporting_facts: list[str] = Field(default_factory=list)
    severity: str = "MEDIUM"


class CompletenessReport(BaseModel):
    """Investigation completeness assessment."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    overall_score: float = 0.0
    evidence: float = 0.0
    witnesses: float = 0.0
    timeline: float = 0.0
    arrests: float = 0.0
    forensics: float = 0.0
    chargesheet: float = 0.0
    legal_review: float = 0.0
    documents: float = 0.0
    missing_components: list[str] = Field(default_factory=list)


class LegalInsight(BaseModel):
    """Legal analysis output."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    relevant_acts: list[str] = Field(default_factory=list)
    relevant_sections: list[str] = Field(default_factory=list)
    precedents_placeholder: list[str] = Field(default_factory=list)
    legal_risks: list[str] = Field(default_factory=list)
    missing_legal_documentation: list[str] = Field(default_factory=list)
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    supporting_facts: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW


class Recommendation(BaseModel):
    """Prioritized investigation recommendation."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    recommendation_id: str
    priority: int
    confidence: float = 0.0
    reason: str
    affected_entities: list[str] = Field(default_factory=list)
    required_evidence: list[str] = Field(default_factory=list)
    supporting_citations: list[str] = Field(default_factory=list)
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    supporting_facts: list[str] = Field(default_factory=list)


class RelationshipNode(BaseModel):
    """Graph node representing a case entity."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    node_id: str
    node_type: str
    label: str
    case_id: Optional[str] = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class RelationshipEdge(BaseModel):
    """Graph edge linking two investigation entities."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    edge_id: str
    source_id: str
    target_id: str
    relation: str
    confidence: float = 0.0
    citations: list[str] = Field(default_factory=list)
    attributes: dict[str, Any] = Field(default_factory=dict)


class RelationshipGraph(BaseModel):
    """Investigation relationship graph."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: str
    nodes: list[RelationshipNode] = Field(default_factory=list)
    edges: list[RelationshipEdge] = Field(default_factory=list)
    summary: str = ""
    confidence: float = 0.0


class ReasoningTraceStep(BaseModel):
    """One step in the reasoning trace."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    step: str
    detail: str
    references: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReasoningTrace(BaseModel):
    """Explainable AI trace for an investigation run."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    trace_id: str
    case_id: Optional[str] = None
    summary: str = ""
    steps: list[ReasoningTraceStep] = Field(default_factory=list)
    confidence: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW
    evidence_references: list[str] = Field(default_factory=list)
    timeline_references: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InvestigationMetrics(BaseModel):
    """Operational metrics for the investigation layer."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    retrieval_confidence: float = 0.0
    evidence_confidence: float = 0.0
    recommendation_confidence: float = 0.0
    overall_confidence: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW
    retrieval_time_ms: float = 0.0
    analysis_time_ms: float = 0.0
    graph_time_ms: float = 0.0
    total_time_ms: float = 0.0
    cache_hit: bool = False
    audits_recorded: int = 0


class InvestigationResponse(BaseModel):
    """Aggregate response for the full investigation analysis."""

    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: Optional[str] = None
    query: Optional[str] = None
    similar_cases: list[SimilarityResult] = Field(default_factory=list)
    evidence_insights: list[EvidenceInsight] = Field(default_factory=list)
    timeline_insight: TimelineInsight = Field(default_factory=TimelineInsight)
    contradictions: list[Contradiction] = Field(default_factory=list)
    completeness: CompletenessReport = Field(default_factory=CompletenessReport)
    legal_insight: LegalInsight = Field(default_factory=LegalInsight)
    recommendations: list[Recommendation] = Field(default_factory=list)
    graph: Optional[RelationshipGraph] = None
    reasoning_trace: Optional[ReasoningTrace] = None
    metrics: InvestigationMetrics = Field(default_factory=InvestigationMetrics)
    confidence: float = 0.0
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
