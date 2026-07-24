"""
============================================================
Retrieval Domain Models
============================================================

Module  : AI Retrieval Engine
Purpose : Defines models for query execution, citation references,
          retrieved chunks, confidence scoring, provenance, statistics,
          and LLM-ready RetrievalContext objects.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.ai.chunking.chunk_models import ChunkType


class RetrievalMode(str, Enum):
    """Operational retrieval speed vs accuracy balance."""
    FAST = "FAST"
    BALANCED = "BALANCED"
    COMPREHENSIVE = "COMPREHENSIVE"


class QueryIntent(str, Enum):
    """Classified user query intent categories."""
    CASE_LOOKUP = "CASE_LOOKUP"
    EVIDENCE_SEARCH = "EVIDENCE_SEARCH"
    TIMELINE_QUERY = "TIMELINE_QUERY"
    OFFICER_QUERY = "OFFICER_QUERY"
    LEGAL_QUERY = "LEGAL_QUERY"
    GENERAL = "GENERAL"


class CitationReference(BaseModel):
    """
    Source citation reference enabling LLM output source-attribution.
    (e.g., "[Evidence #EVI-001] Digital Log")
    """
    model_config = ConfigDict(from_attributes=True)

    source_reference: str
    entity_name: str
    entity_id: str
    module: str


class RetrievalFilter(BaseModel):
    """
    Metadata filter criteria for scoped vector search.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: Optional[str] = None
    chunk_types: Optional[list[ChunkType]] = None
    entity_type: Optional[str] = None
    officer: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    custom_filters: dict[str, Any] = Field(default_factory=dict)


class SearchQuery(BaseModel):
    """
    Query parameter container for multi-stage retrieval execution.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    query: str
    query_embedding: Optional[list[float]] = None
    mode: RetrievalMode = RetrievalMode.BALANCED
    top_k: int = 10
    min_similarity: float = 0.0
    filters: RetrievalFilter = Field(default_factory=RetrievalFilter)


class RetrievedChunk(BaseModel):
    """
    Rich retrieved chunk with dual confidence scores, entity priorities,
    and source citation reference.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    chunk_id: str
    case_id: str
    chunk_type: str
    content: str
    token_estimate: int
    similarity_score: float = 0.0
    rerank_score: float = 0.0
    retrieval_confidence: float = 0.0
    source_reliability: float = 1.0
    overall_confidence: float = 0.0
    confidence_level: str = "HIGH"  # "HIGH" | "MEDIUM" | "LOW"
    priority: int = 50
    citation: CitationReference
    parent_entity_id: Optional[str] = None
    parent_chunk_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievalStatistics(BaseModel):
    """
    Metrics tracking retrieval durations, candidate counts, and token totals.
    """
    model_config = ConfigDict(from_attributes=True)

    retrieval_time_ms: float = 0.0
    rerank_time_ms: float = 0.0
    compression_time_ms: float = 0.0
    total_time_ms: float = 0.0
    chunks_examined: int = 0
    chunks_returned: int = 0
    average_similarity: float = 0.0
    token_count: int = 0


class PromptProvenance(BaseModel):
    """
    Audit provenance metadata for assembled prompt contexts.
    """
    model_config = ConfigDict(from_attributes=True)

    query_id: str
    retrieval_id: str
    chunk_ids: list[str]
    generated_at: datetime
    context_hash: str


class PromptSections(BaseModel):
    """
    Structured context sections ready for direct LLM system & user prompt construction.
    """
    model_config = ConfigDict(from_attributes=True)

    system_context: str = ""
    case_summary: str = ""
    victims: str = ""
    accused: str = ""
    evidence: str = ""
    timeline: str = ""
    legal: str = ""
    question: str = ""


class SearchResult(BaseModel):
    """
    API response model for raw retrieval queries.
    """
    model_config = ConfigDict(from_attributes=True)

    query: str
    intent: QueryIntent = QueryIntent.GENERAL
    chunks: list[RetrievedChunk]
    total_found: int
    statistics: RetrievalStatistics


class RetrievalContext(BaseModel):
    """
    Fully assembled, LLM-ready RetrievalContext.
    """
    model_config = ConfigDict(from_attributes=True)

    version: str = "1.0.0"
    query: str
    assembled_text: str
    sections: PromptSections
    chunks: list[RetrievedChunk]
    token_count: int
    max_token_budget: int
    provenance: PromptProvenance
    statistics: RetrievalStatistics
