"""
============================================================
Case Section Pydantic Schemas
============================================================

Module  : Act & Section Management
Purpose : Request/Response structures and API contract for Case Section links.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.complainant import PaginationMeta


# ==============================================================
# 1. CaseSectionCreate — Linking Request
# ==============================================================

class CaseSectionCreate(BaseModel):
    """
    Schema for assigning a legal section to a case.
    """

    section_id: str = Field(
        ...,
        description="ID of the legal section to assign.",
        examples=["SEC-BNS103"],
    )
    remarks: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional remarks regarding this section assignment.",
        examples=["Primary section of offense (Murder)."],
    )


# ==============================================================
# 2. CaseSectionResponse — Association Details
# ==============================================================

class CaseSectionResponse(BaseModel):
    """
    Complete Case Section Association record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    association_id: str = Field(
        ...,
        description="Unique system-generated identifier for this link.",
        examples=["CSA-A1B2C3D4E5F6"],
    )
    case_master_id: str = Field(
        ...,
        description="ID of the associated case.",
        examples=["CM-5065C147B4E7"],
    )
    section_id: str = Field(
        ...,
        description="ID of the assigned legal section.",
        examples=["SEC-BNS103"],
    )
    remarks: Optional[str] = Field(
        default=None,
        description="Remarks on this section assignment.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the assignment was made.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the assignment was last updated.",
    )


# ==============================================================
# 3. CaseSectionSummary — Comprehensive Detailed Association Summary
# ==============================================================

class CaseSectionSummary(BaseModel):
    """
    Detailed summary of a case-section link including Act and Section details.
    """

    model_config = ConfigDict(from_attributes=True)

    association_id: str
    case_master_id: str
    section_id: str
    remarks: Optional[str] = None
    created_at: datetime

    # De-normalized properties to make API payload premium and clean
    section_number: str
    section_title: str
    act_short_name: str
    act_year: int
    is_cognizable: bool
    is_bailable: bool
    maximum_punishment: Optional[str] = None


# ==============================================================
# 4. CaseSectionListResponse — Paginated List
# ==============================================================

class CaseSectionListResponse(BaseModel):
    """Wrapper encapsulating a page of case section summaries and pagination metadata."""

    items: list[CaseSectionSummary] = Field(..., description="Page of case sections.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")
