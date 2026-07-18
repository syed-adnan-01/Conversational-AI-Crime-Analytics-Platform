"""
============================================================
Complainant Pydantic Schemas
============================================================

Module  : Complainant Management
Purpose : Request/Response structures and API contract.
"""

from datetime import datetime
from enum import Enum
from math import ceil
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, EmailStr

from app.common.enums import Gender, SortOrder


# ==============================================================
# BASE SCHEMA
# ==============================================================

class ComplainantBase(BaseModel):
    """
    Shared fields between ComplainantCreate, ComplainantUpdate, and ComplainantResponse.
    """

    gender: Optional[Gender] = Field(
        default=None,
        description="Gender of the complainant.",
        examples=[Gender.MALE],
    )
    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150,
        description="Age of the complainant.",
        examples=[35],
    )
    address: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Address of the complainant.",
        examples=["No 45, 2nd Main, Bengaluru"],
    )
    nationality: Optional[str] = Field(
        default="Indian",
        max_length=50,
        description="Nationality of the complainant.",
        examples=["Indian"],
    )
    occupation: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Occupation of the complainant.",
        examples=["Business Analyst"],
    )
    relationship_type: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Relationship of the complainant to the case or victim.",
        examples=["Self", "Father", "Neighbor"],
    )
    relative_name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Name of the relative (e.g., father/husband).",
        examples=["Rajesh Kumar"],
    )


# ==============================================================
# 1. ComplainantCreate — Registration Request
# ==============================================================

class ComplainantCreate(ComplainantBase):
    """
    Schema for registering a new complainant.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the complainant.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the complainant.",
        examples=["9876543210"],
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the complainant.",
        examples=["amit.kumar@example.com"],
    )


# ==============================================================
# 2. ComplainantUpdate — Mutation Request
# ==============================================================

class ComplainantUpdate(ComplainantBase):
    """
    Schema for updating an existing complainant.
    Every field is optional.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Full name of the complainant.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the complainant.",
        examples=["9876543210"],
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the complainant.",
        examples=["amit.kumar@example.com"],
    )


# ==============================================================
# 3. ComplainantResponse — Full Detail View
# ==============================================================

class ComplainantResponse(ComplainantBase):
    """
    Complete complainant record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    complainant_id: str = Field(
        ...,
        description="Unique system-generated identifier for the complainant.",
        examples=["CP-A1B2C3D4E5F6"],
    )
    case_master_id: str = Field(
        ...,
        description="ID of the case this complainant is associated with.",
        examples=["CM-5065C147B4E7"],
    )
    name: str = Field(
        ...,
        description="Full name of the complainant.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the complainant.",
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the complainant.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the complainant record was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the complainant record was last updated.",
    )


# ==============================================================
# 4. ComplainantSummary — Lightweight View
# ==============================================================

class ComplainantSummary(BaseModel):
    """
    Lightweight summary of a complainant, optimized for list views.
    """

    model_config = ConfigDict(from_attributes=True)

    complainant_id: str
    case_master_id: str
    name: str
    gender: Optional[Gender] = None
    mobile_no: Optional[str] = None
    relationship_type: Optional[str] = None


# ==============================================================
# 5. ComplainantListResponse — Paginated List
# ==============================================================

class PaginationMeta(BaseModel):
    """Metadata describing the pagination state."""

    total: int = Field(..., description="Total number of matching records.")
    page: int = Field(..., description="Current page number (1-indexed).")
    page_size: int = Field(..., description="Number of records per page.")
    total_pages: int = Field(..., description="Total number of pages.")
    has_next: bool = Field(..., description="True if a subsequent page exists.")
    has_previous: bool = Field(..., description="True if a preceding page exists.")

    @classmethod
    def calculate(cls, total: int, page: int, page_size: int) -> "PaginationMeta":
        total_pages = ceil(total / page_size) if total > 0 else 1
        return cls(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


class ComplainantListResponse(BaseModel):
    """Wrapper encapsulating a page of complainant summaries and metadata."""

    items: list[ComplainantSummary] = Field(..., description="Page of complainant records.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")


# ==============================================================
# 6. Sorting Enums
# ==============================================================

class ComplainantSortField(str, Enum):
    """Allowed sort fields for Complainants."""

    NAME = "name"
    AGE = "age"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"
