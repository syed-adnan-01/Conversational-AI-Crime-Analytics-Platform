from typing import Optional, Dict, Any

from app.repository.mock_users import MOCK_USERS
from app.auth.jwt_handler import JWTHandler
from app.models.user import User

class AuthService:
    """Service handling business logic for authentication."""

    @staticmethod
    def login(employee_id: str, password: str, department: str) -> Optional[Dict[str, Any]]:
        """
        Verify credentials and generate a JWT if valid.
        Currently uses MOCK_USERS.
        """
        # Find the user in the mock database
        user_data = next(
            (u for u in MOCK_USERS if u["employee_id"] == employee_id), 
            None
        )

        if not user_data:
            return None

        # Verify password and department
        # Note: In a real app, passwords should be verified using a hasher like bcrypt
        if user_data["password"] != password or user_data["department"] != department:
            return None

        # Create the user model instance
        user = User(**user_data)

        # Generate the JWT token
        token_data = {"sub": user.employee_id, "role": user.role.value}
        access_token = JWTHandler.create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "user": user
        }