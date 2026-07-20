from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.common.enums import Gender, IdentificationType
from app.schemas.case import PaginationMeta


class WitnessSortField(str, Enum):
    """Sort fields for witness query options."""
    NAME = "name"
    AGE = "age"
    STATEMENT_DATE = "statement_date"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class WitnessCreate(BaseModel):
    """Schema for registering a new witness."""
    name: str = Field(..., min_length=2, max_length=150)
    gender: Gender
    age: Optional[int] = Field(None, ge=0, le=150)
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    nationality: Optional[str] = "Indian"
    occupation: Optional[str] = None
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None
    statement: Optional[str] = None
    statement_date: Optional[datetime] = None
    is_hostile: bool = False


class WitnessUpdate(BaseModel):
    """Schema for updating an existing witness."""
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    gender: Optional[Gender] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    nationality: Optional[str] = None
    occupation: Optional[str] = None
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None
    statement: Optional[str] = None
    statement_date: Optional[datetime] = None
    is_hostile: Optional[bool] = None


class WitnessResponse(BaseModel):
    """Response schema for witness details."""
    model_config = ConfigDict(from_attributes=True)

    witness_id: str
    case_master_id: str
    name: str
    gender: Gender
    age: Optional[int] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    nationality: Optional[str] = None
    occupation: Optional[str] = None
    id_type: Optional[IdentificationType] = None
    id_number: Optional[str] = None
    statement: Optional[str] = None
    statement_date: Optional[datetime] = None
    is_hostile: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WitnessSummary(BaseModel):
    """Summary schema for witness list views."""
    model_config = ConfigDict(from_attributes=True)

    witness_id: str
    case_master_id: str
    name: str
    gender: Gender
    mobile_no: Optional[str] = None
    is_hostile: bool
    statement_date: Optional[datetime] = None


class WitnessListResponse(BaseModel):
    """Paginated list response for witnesses."""
    items: List[WitnessSummary]
    pagination: PaginationMeta
