"""
============================================================
Act Pydantic Schemas
============================================================

Module  : Act & Section Management
Purpose : Request/Response structures and API contract for Acts.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.complainant import PaginationMeta


# ==============================================================
# BASE SCHEMA
# ==============================================================

class ActBase(BaseModel):
    """
    Shared fields between ActCreate, ActUpdate, and ActResponse.
    """

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="A detailed description of the legislative act.",
        examples=["Primary criminal code of India replacing the IPC."],
    )


# ==============================================================
# 1. ActCreate — Registration Request
# ==============================================================

class ActCreate(ActBase):
    """
    Schema for creating a new legislative Act.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Official name of the legislative act.",
        examples=["Bharatiya Nyaya Sanhita"],
    )
    short_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Standard abbreviation or short name for the act.",
        examples=["BNS"],
    )
    year: int = Field(
        ...,
        ge=1800,
        le=2100,
        description="The year the act was enacted.",
        examples=[2023],
    )


# ==============================================================
# 2. ActUpdate — Mutation Request
# ==============================================================

class ActUpdate(ActBase):
    """
    Schema for updating an existing legislative Act.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Official name of the legislative act.",
        examples=["Bharatiya Nyaya Sanhita"],
    )
    short_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Standard abbreviation or short name for the act.",
        examples=["BNS"],
    )
    year: Optional[int] = Field(
        default=None,
        ge=1800,
        le=2100,
        description="The year the act was enacted.",
        examples=[2023],
    )


# ==============================================================
# 3. ActResponse — Full Detail View
# ==============================================================

class ActResponse(ActBase):
    """
    Complete Act record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    act_id: str = Field(
        ...,
        description="Unique system-generated identifier for the act.",
        examples=["ACT-BNS2023"],
    )
    name: str = Field(
        ...,
        description="Official name of the legislative act.",
    )
    short_name: str = Field(
        ...,
        description="Standard abbreviation or short name for the act.",
    )
    year: int = Field(
        ...,
        description="The year the act was enacted.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the act record was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the act record was last updated.",
    )


# ==============================================================
# 4. ActSummary — Lightweight View
# ==============================================================

class ActSummary(BaseModel):
    """
    Lightweight summary of an Act, optimized for list views.
    """

    model_config = ConfigDict(from_attributes=True)

    act_id: str
    name: str
    short_name: str
    year: int


# ==============================================================
# 5. ActListResponse — Paginated List
# ==============================================================

class ActListResponse(BaseModel):
    """Wrapper encapsulating a page of Act summaries and metadata."""

    items: list[ActSummary] = Field(..., description="Page of legislative acts.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")


# ==============================================================
# 6. Sorting Enums
# ==============================================================

class ActSortField(str, Enum):
    """Allowed sort fields for Acts."""

    NAME = "name"
    SHORT_NAME = "short_name"
    YEAR = "year"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"
