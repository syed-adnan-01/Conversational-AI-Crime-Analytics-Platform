from pydantic import BaseModel


class LoginRequest(BaseModel):
    employee_id: str
    password: str
    department: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: str
    employee_id: str
    name: str
    email: str
    department: str
    role: str