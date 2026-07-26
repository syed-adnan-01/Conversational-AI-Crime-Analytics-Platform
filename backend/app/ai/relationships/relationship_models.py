from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class RelationshipType(str, Enum):
    INVOLVED_IN = "INVOLVED_IN"; OWNS = "OWNS"; USES = "USES"; MENTIONS = "MENTIONS"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"; LOCATED_AT = "LOCATED_AT"; WORKED_ON = "WORKED_ON"
    TESTIFIED_IN = "TESTIFIED_IN"; SUBMITTED = "SUBMITTED"; REFERENCES = "REFERENCES"
    SIMILAR_TO = "SIMILAR_TO"; RELATED_CASE = "RELATED_CASE"


class Relationship(BaseModel):
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    confidence: float = Field(ge=0, le=1)
    source: str
    reason: str
    source_records: list[str] = Field(default_factory=list)
    supporting_entities: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
