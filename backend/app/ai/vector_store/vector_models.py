"""
============================================================
Vector Store Domain Models
============================================================

Module  : AI Vector Store Layer
Purpose : Defines SearchMode Enum, SearchFilter, VectorSearchRequest,
          and VectorSearchResult models.
"""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.ai.chunking.chunk_models import ChunkType


class SearchMode(str, Enum):
    """Supported search algorithms."""
    VECTOR = "VECTOR"
    KEYWORD = "KEYWORD"
    HYBRID = "HYBRID"


class SearchFilter(BaseModel):
    """
    Search filter criteria for metadata-based vector scoping.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    case_id: Optional[str] = None
    chunk_types: Optional[list[ChunkType]] = None
    metadata_filters: dict[str, Any] = Field(default_factory=dict)


class VectorSearchRequest(BaseModel):
    """
    API payload model for semantic vector search requests.
    Supports plain text string queries or pre-computed embedding vectors.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    query: Optional[str] = None
    query_vector: Optional[list[float]] = None
    search_mode: SearchMode = SearchMode.VECTOR
    filter: SearchFilter = Field(default_factory=SearchFilter)
    top_k: int = 5


class VectorSearchResult(BaseModel):
    """
    SearchResult item returned from semantic vector queries.
    """
    model_config = ConfigDict(from_attributes=True, extra="allow")

    chunk_id: str
    case_id: str
    score: float
    content: str
    chunk_type: str
    parent_entity_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
