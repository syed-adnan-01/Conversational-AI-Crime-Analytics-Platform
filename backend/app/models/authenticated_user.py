from pydantic import BaseModel

from app.core.roles import UserRole


class AuthenticatedUser(BaseModel):
    user_id: str
    employee_id: str
    name: str
    department: str
    role: UserRole