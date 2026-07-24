"""
============================================================
AI Investigation Context Domain Models
============================================================

Module  : AI Context Builder
Purpose : Defines the unified InvestigationContext aggregate model,
          metadata, summary, detail level enums, and extension slots.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.accused import Accused
from app.models.arrest import Arrest
from app.models.case_master import CaseMaster
from app.models.chargesheet import Chargesheet
from app.models.complainant import Complainant
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.officer import OfficerAssignment
from app.models.section import Section
from app.models.timeline import TimelineEvent
from app.models.victim import Victim
from app.models.witness import Witness


class DetailLevel(str, Enum):
    """Detail level granularity for context serialization."""
    SUMMARY = "summary"
    STANDARD = "standard"
    DETAILED = "detailed"


class ContextMetadata(BaseModel):
    """
    Metadata associated with a generated InvestigationContext.
    Tracks generation timestamp, execution duration, SHA-256 fingerprint,
    AI readiness state, and breakdown counts.
    """
    model_config = ConfigDict(from_attributes=True)

    generated_at: datetime
    case_id: str
    context_version: str = "1.0.0"
    build_duration_ms: float = 0.0
    context_hash: str
    is_ai_ready: bool = False
    ai_readiness_reasons: list[str] = Field(default_factory=list)
    total_entities: int = 0
    entity_counts: dict[str, int] = Field(default_factory=dict)


class ContextSummary(BaseModel):
    """
    Lightweight summary object designed for dashboard views,
    list views, and quick AI routing decisions.
    """
    model_config = ConfigDict(from_attributes=True)

    case_title: str
    status: str
    registered_date: Optional[datetime] = None
    lead_officer: Optional[str] = None
    total_accused: int = 0
    total_victims: int = 0
    total_evidence: int = 0
    total_sections: int = 0
    is_ai_ready: bool = False


class InvestigationContext(BaseModel):
    """
    Unified AI-ready context container aggregating all investigation
    domain entities into a single aggregate object.
    
    Serves as the single source of truth for downstream AI services:
    - RAG / Vector Search
    - LLM Prompt Context
    - AI Summarization
    - Knowledge Graphs
    - Crime Analytics & Predictions
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    # Core Case Aggregate & Sub-Entities
    case: CaseMaster
    complainant: Optional[Complainant] = None
    victims: list[Victim] = Field(default_factory=list)
    accused: list[Accused] = Field(default_factory=list)
    witnesses: list[Witness] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    arrests: list[Arrest] = Field(default_factory=list)
    chargesheets: list[Chargesheet] = Field(default_factory=list)
    court_proceedings: list[CourtProceeding] = Field(default_factory=list)
    officer_assignments: list[OfficerAssignment] = Field(default_factory=list)
    timeline_events: list[TimelineEvent] = Field(default_factory=list)

    # Headers & Summaries
    summary: ContextSummary
    metadata: ContextMetadata

    # Extensibility Slots for Future AI Layer Modules
    relationships: Optional[list[dict[str, Any]]] = None
    analytics: Optional[dict[str, Any]] = None
    predictions: Optional[dict[str, Any]] = None
    documents: Optional[list[dict[str, Any]]] = None
    embeddings: Optional[dict[str, Any]] = None
    knowledge: Optional[dict[str, Any]] = None
