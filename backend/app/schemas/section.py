"""
============================================================
Section Pydantic Schemas
============================================================

Module  : Act & Section Management
Purpose : Request/Response structures and API contract for Sections.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.complainant import PaginationMeta


# ==============================================================
# BASE SCHEMA
# ==============================================================

class SectionBase(BaseModel):
    """
    Shared fields between SectionCreate, SectionUpdate, and SectionResponse.
    """

    description: Optional[str] = Field(
        default=None,
        max_length=1500,
        description="Detailed legal description or text of the section.",
        examples=["Punishment for committing murder."],
    )
    is_cognizable: bool = Field(
        default=True,
        description="Indicates if the offence is cognizable (police can arrest without warrant).",
        examples=[True],
    )
    is_bailable: bool = Field(
        default=True,
        description="Indicates if the offence is bailable.",
        examples=[False],
    )
    maximum_punishment: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Maximum legal punishment associated with this section.",
        examples=["Death or life imprisonment"],
    )


# ==============================================================
# 1. SectionCreate — Registration Request
# ==============================================================

class SectionCreate(SectionBase):
    """
    Schema for registering a new section under an Act.
    """

    section_number: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Section number (e.g. 103, 303, 35, 66D).",
        examples=["103"],
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=250,
        description="Legal title or short header of the section.",
        examples=["Punishment for Murder"],
    )


# ==============================================================
# 2. SectionUpdate — Mutation Request
# ==============================================================

class SectionUpdate(SectionBase):
    """
    Schema for updating an existing section.
    """

    section_number: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20,
        description="Section number (e.g. 103, 303, 35, 66D).",
        examples=["103"],
    )
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=250,
        description="Legal title or short header of the section.",
        examples=["Punishment for Murder"],
    )


# ==============================================================
# 3. SectionResponse — Full Detail View
# ==============================================================

class SectionResponse(SectionBase):
    """
    Complete Section record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    section_id: str = Field(
        ...,
        description="Unique system-generated identifier for the section.",
        examples=["SEC-BNS103"],
    )
    act_id: str = Field(
        ...,
        description="ID of the parent legislative Act.",
        examples=["ACT-BNS2023"],
    )
    section_number: str = Field(
        ...,
        description="Section number.",
    )
    title: str = Field(
        ...,
        description="Legal title of the section.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the section record was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the section record was last updated.",
    )


# ==============================================================
# 4. SectionSummary — Lightweight View
# ==============================================================

class SectionSummary(BaseModel):
    """
    Lightweight summary of a Section, optimized for list views.
    """

    model_config = ConfigDict(from_attributes=True)

    section_id: str
    act_id: str
    section_number: str
    title: str
    is_cognizable: bool
    is_bailable: bool
    maximum_punishment: Optional[str] = None


# ==============================================================
# 5. SectionListResponse — Paginated List
# ==============================================================

class SectionListResponse(BaseModel):
    """Wrapper encapsulating a page of Section summaries and metadata."""

    items: list[SectionSummary] = Field(..., description="Page of legal sections.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")


# ==============================================================
# 6. Sorting Enums
# ==============================================================

class SectionSortField(str, Enum):
    """Allowed sort fields for Sections."""

    SECTION_NUMBER = "section_number"
    TITLE = "title"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"
