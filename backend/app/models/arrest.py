from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ArrestStatus(str, Enum):
    """Workflow statuses for arrests."""
    ARRESTED = "ARRESTED"
    RELEASED_ON_BAIL = "RELEASED_ON_BAIL"
    REMANDED = "REMANDED"
    ABSCONDING = "ABSCONDING"
    DETAINED = "DETAINED"


class Arrest(BaseModel):
    """
    Domain entity representing an Arrest of an Accused in a Case.
    """

    model_config = ConfigDict(from_attributes=True)

    arrest_id: Optional[str] = None
    case_master_id: str
    accused_id: str
    arrest_date: datetime
    arrest_time: Optional[str] = None
    arrest_location: str
    grounds_for_arrest: str
    arresting_officer: str
    arrest_memo: Optional[str] = None
    status: ArrestStatus = ArrestStatus.ARRESTED
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
