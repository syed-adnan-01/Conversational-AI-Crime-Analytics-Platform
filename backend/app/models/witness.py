from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

from app.common.enums import Gender, IdentificationType


class Witness(BaseModel):
    """
    Domain entity representing a Witness connected to a Case.
    """

    model_config = ConfigDict(from_attributes=True)

    witness_id: Optional[str] = None
    case_master_id: str
    name: str
    gender: Gender
    age: Optional[int] = None
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
