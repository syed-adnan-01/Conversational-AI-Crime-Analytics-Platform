"""
============================================================
Index Models
============================================================

Module  : AI Indexing Subsystem
Purpose : Defines IndexStatus Enum, IndexMetadata, and IndexListResponse models.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IndexStatus(str, Enum):
    """Lifecycle statuses of vector indexing for a case."""
    NOT_INDEXED = "NOT_INDEXED"
    INDEXING = "INDEXING"
    INDEXED = "INDEXED"
    OUTDATED = "OUTDATED"
    FAILED = "FAILED"


class IndexMetadata(BaseModel):
    """
    Metadata tracking the status, hash fingerprint, and provider metrics
    of a case vector index.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: str
    context_hash: str
    indexed_at: Optional[datetime] = None
    provider: str
    embedding_model: str
    vector_store: str
    embedding_version: str = "1.0.0"
    schema_version: str = "1.0.0"
    index_version: str = "1.0.0"
    chunk_count: int = 0
    indexing_duration_ms: float = 0.0
    status: IndexStatus = IndexStatus.NOT_INDEXED


class IndexListResponse(BaseModel):
    """
    Response model listing operational index metadata across all cases.
    """
    model_config = ConfigDict(from_attributes=True)

    total_cases_indexed: int
    total_vectors_stored: int
    items: list[IndexMetadata]
