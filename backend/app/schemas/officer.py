from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.officer import OfficerRole, OfficerRank
from app.schemas.case import PaginationMeta


class OfficerSortField(str, Enum):
    """Sort fields for officer assignments."""
    ASSIGNED_DATE = "assigned_date"
    ROLE = "role"
    CREATED_AT = "created_at"


class OfficerMasterCreate(BaseModel):
    """Schema for registering an officer in Officer Master."""
    badge_number: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    rank: OfficerRank
    department: str = Field(..., min_length=2, max_length=100)
    police_station_id: Optional[int] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True


class OfficerMasterResponse(BaseModel):
    """Response schema for Officer Master profile."""
    model_config = ConfigDict(from_attributes=True)

    officer_id: str
    badge_number: str
    name: str
    rank: OfficerRank
    department: str
    police_station_id: Optional[int] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OfficerAssignmentCreate(BaseModel):
    """Schema for assigning an officer to a case."""
    officer_id: str
    role: OfficerRole
    assigned_date: datetime
    relieved_date: Optional[datetime] = None
    is_active: bool = True
    remarks: Optional[str] = None


class OfficerAssignmentUpdate(BaseModel):
    """Schema for updating an officer assignment."""
    role: Optional[OfficerRole] = None
    assigned_date: Optional[datetime] = None
    relieved_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    remarks: Optional[str] = None


class OfficerAssignmentResponse(BaseModel):
    """Response schema for an officer assignment."""
    model_config = ConfigDict(from_attributes=True)

    assignment_id: str
    case_master_id: str
    officer_id: str
    officer_name: Optional[str] = None
    badge_number: Optional[str] = None
    rank: Optional[OfficerRank] = None
    role: OfficerRole
    assigned_date: datetime
    relieved_date: Optional[datetime] = None
    is_active: bool
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OfficerAssignmentListResponse(BaseModel):
    """Paginated list response for officer assignments."""
    items: List[OfficerAssignmentResponse]
    pagination: PaginationMeta
