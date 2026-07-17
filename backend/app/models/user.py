from pydantic import BaseModel, EmailStr, ConfigDict

from app.core.roles import UserRole


class User(BaseModel):
    """
    Represents an authenticated user within the CrimeSphere AI system.
    """

    model_config = ConfigDict(from_attributes=True)

    user_id: str
    employee_id: str
    name: str
    email: EmailStr
    department: str
    role: UserRole
    is_active: bool = True