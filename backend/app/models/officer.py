from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class OfficerRole(str, Enum):
    """Roles assigned to officers in case investigations."""
    INVESTIGATING_OFFICER = "Investigating Officer"
    SUPERVISING_OFFICER = "Supervising Officer"
    SHO = "SHO"
    ACP = "ACP"
    DCP = "DCP"
    COMMISSIONER = "Commissioner"
    FORENSIC_OFFICER = "Forensic Officer"


class OfficerRank(str, Enum):
    """Ranks of police officers."""
    CONSTABLE = "Constable"
    HEAD_CONSTABLE = "Head Constable"
    SUB_INSPECTOR = "Sub-Inspector"
    INSPECTOR = "Inspector"
    DSP = "DSP"
    SP = "SP"
    DCP = "DCP"
    IGP = "IGP"
    COMMISSIONER = "Commissioner"


class OfficerMaster(BaseModel):
    """
    Master entity representing a Police Officer profile.
    """

    model_config = ConfigDict(from_attributes=True)

    officer_id: Optional[str] = None
    badge_number: str
    name: str
    rank: OfficerRank
    department: str
    police_station_id: Optional[int] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OfficerAssignment(BaseModel):
    """
    Transactional domain entity mapping an Officer to a Case.
    """

    model_config = ConfigDict(from_attributes=True)

    assignment_id: Optional[str] = None
    case_master_id: str
    officer_id: str
    role: OfficerRole
    assigned_date: datetime
    relieved_date: Optional[datetime] = None
    is_active: bool = True
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
