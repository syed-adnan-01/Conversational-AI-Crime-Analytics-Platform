from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from app.ai.entities.entity_models import EntityRecord
from app.ai.relationships.relationship_models import Relationship


class ConfidenceLevel(str, Enum): LOW = "low"; MEDIUM = "medium"; HIGH = "high"

class GraphNode(EntityRecord):
    color: str | None = None
    group: str | None = None

class GraphEdge(Relationship):
    id: str | None = None

class GraphStatistics(BaseModel):
    node_count: int = 0; edge_count: int = 0; entity_counts: dict[str, int] = Field(default_factory=dict)
    relationship_counts: dict[str, int] = Field(default_factory=dict); built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RelationshipGraph(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    statistics: GraphStatistics = Field(default_factory=GraphStatistics)

class GraphSearchRequest(BaseModel):
    start_entity_id: str; max_depth: int = Field(default=2, ge=0, le=10); relationship_types: list[str] = Field(default_factory=list)

class GraphSearchResponse(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list); edges: list[GraphEdge] = Field(default_factory=list)
    depth: int = 0; query_latency_ms: float = 0

class ShortestPath(BaseModel):
    node_ids: list[str] = Field(default_factory=list); edges: list[GraphEdge] = Field(default_factory=list); found: bool = False

class Neighborhood(GraphSearchResponse): pass

class Community(BaseModel):
    id: str; node_ids: list[str]; reason: str; confidence: float

class LinkPrediction(BaseModel):
    source_id: str; target_id: str; relationship_type: str; confidence: float
    supporting_evidence: list[str] = Field(default_factory=list); reasoning: str

class ResolutionResult(BaseModel):
    resolution_score: float; merged_entity: EntityRecord | None = None; duplicate_entity_ids: list[str] = Field(default_factory=list); reasoning: list[str] = Field(default_factory=list)

class GraphMetrics(BaseModel):
    node_count: int = 0; edge_count: int = 0; resolution_accuracy: float = 0; query_latency_ms: float = 0
    cache_hit_rate: float = 0; graph_build_time_ms: float = 0

class GraphTrace(BaseModel):
    operation: str; started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)); duration_ms: float = 0; details: dict[str, Any] = Field(default_factory=dict)
