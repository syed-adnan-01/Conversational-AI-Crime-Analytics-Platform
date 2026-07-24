"""
============================================================
Chunk Models
============================================================

Module  : AI Chunking Engine
Purpose : Defines ChunkType Enum, typed ChunkMetadata, and ContextChunk model.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ChunkType(str, Enum):
    """Categorized domain entity chunk types."""
    CASE = "CASE"
    COMPLAINANT = "COMPLAINANT"
    VICTIM = "VICTIM"
    ACCUSED = "ACCUSED"
    WITNESS = "WITNESS"
    SECTION = "SECTION"
    EVIDENCE = "EVIDENCE"
    ARREST = "ARREST"
    CHARGESHEET = "CHARGESHEET"
    COURT = "COURT"
    OFFICER = "OFFICER"
    TIMELINE = "TIMELINE"


class ChunkMetadata(BaseModel):
    """
    Strongly-typed metadata container attached to each ContextChunk.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    entity_type: str
    entity_id: Optional[str] = None
    section_number: Optional[str] = None
    is_cognizable: Optional[bool] = None
    is_bailable: Optional[bool] = None
    custody_status: Optional[str] = None
    hearing_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    custom_attributes: dict[str, Any] = Field(default_factory=dict)


class ContextChunk(BaseModel):
    """
    A single granular text chunk extracted from an InvestigationContext,
    ready for embedding generation and vector search indexing.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    chunk_id: str
    case_id: str
    context_hash: str
    chunk_index: int
    chunk_type: ChunkType
    parent_entity_id: Optional[str] = None
    parent_chunk_id: Optional[str] = None
    content: str
    token_estimate: int
    metadata: ChunkMetadata
