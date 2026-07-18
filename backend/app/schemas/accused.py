"""
============================================================
Accused Pydantic Schemas
============================================================

Module  : Accused Management
Purpose : Request/Response structures and API contract.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import Gender, IdentificationType
from app.schemas.complainant import PaginationMeta


# ==============================================================
# BASE SCHEMA
# ==============================================================

class AccusedBase(BaseModel):
    """
    Shared fields between AccusedCreate, AccusedUpdate, and AccusedResponse.
    """

    gender: Optional[Gender] = Field(
        default=None,
        description="Gender of the accused.",
        examples=[Gender.MALE],
    )
    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=150,
        description="Age of the accused.",
        examples=[35],
    )
    address: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Address of the accused.",
        examples=["No 45, 2nd Main, Bengaluru"],
    )
    nationality: Optional[str] = Field(
        default="Indian",
        max_length=50,
        description="Nationality of the accused.",
        examples=["Indian"],
    )
    occupation: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Occupation of the accused.",
        examples=["Business Analyst"],
    )
    id_type: Optional[IdentificationType] = Field(
        default=None,
        description="Type of identification document.",
        examples=[IdentificationType.AADHAAR],
    )
    id_number: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Identification document number.",
        examples=["1234-5678-9012"],
    )


# ==============================================================
# 1. AccusedCreate — Registration Request
# ==============================================================

class AccusedCreate(AccusedBase):
    """
    Schema for registering a new accused.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the accused.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the accused.",
        examples=["9876543210"],
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the accused.",
        examples=["amit.kumar@example.com"],
    )


# ==============================================================
# 2. AccusedUpdate — Mutation Request
# ==============================================================

class AccusedUpdate(AccusedBase):
    """
    Schema for updating an existing accused.
    Every field is optional.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Full name of the accused.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the accused.",
        examples=["9876543210"],
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the accused.",
        examples=["amit.kumar@example.com"],
    )


# ==============================================================
# 3. AccusedResponse — Full Detail View
# ==============================================================

class AccusedResponse(AccusedBase):
    """
    Complete accused record returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    accused_id: str = Field(
        ...,
        description="Unique system-generated identifier for the accused.",
        examples=["AC-A1B2C3D4E5F6"],
    )
    case_master_id: str = Field(
        ...,
        description="ID of the case this accused is associated with.",
        examples=["CM-5065C147B4E7"],
    )
    name: str = Field(
        ...,
        description="Full name of the accused.",
        examples=["Amit Kumar"],
    )
    mobile_no: Optional[str] = Field(
        default=None,
        description="Mobile number of the accused.",
    )
    email: Optional[str] = Field(
        default=None,
        description="Email address of the accused.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the accused record was created.",
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the accused record was last updated.",
    )


# ==============================================================
# 4. AccusedSummary — Lightweight View
# ==============================================================

class AccusedSummary(BaseModel):
    """
    Lightweight summary of an accused, optimized for list views.
    """

    model_config = ConfigDict(from_attributes=True)

    accused_id: str
    case_master_id: str
    name: str
    gender: Optional[Gender] = None
    mobile_no: Optional[str] = None
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None


# ==============================================================
# 5. AccusedListResponse — Paginated List
# ==============================================================

class AccusedListResponse(BaseModel):
    """Wrapper encapsulating a page of accused summaries and metadata."""

    items: list[AccusedSummary] = Field(..., description="Page of accused records.")
    pagination: PaginationMeta = Field(..., description="Pagination state metadata.")


# ==============================================================
# 6. Sorting Enums
# ==============================================================

class AccusedSortField(str, Enum):
    """Allowed sort fields for Accused."""

    NAME = "name"
    AGE = "age"
    CREATED_DATE = "created_date"
    UPDATED_DATE = "updated_date"
