from typing import Optional

from app.auth.jwt_handler import JWTHandler
from app.core.password import PasswordManager
from app.models.user import User
from app.repository.user_repository import UserRepository


class AuthService:
    """Service responsible for authentication business logic."""

    @staticmethod
    def login(
        employee_id: str,
        password: str,
        department: str,
    ) -> Optional[dict]:
        """
        Authenticate a user and generate an access token.
        """

        # Retrieve user from repository
        user_data = UserRepository.get_by_employee_id(employee_id)

        if user_data is None:
            return None

        # Verify password using bcrypt
        if not PasswordManager.verify_password(
            password,
            user_data["password"],
        ):
            return None

        # Verify department
        if user_data["department"] != department:
            return None

        # Convert dictionary to User model
        user = User(**user_data)

        # JWT payload
        token_data = {
            "sub": user.employee_id,
            "uid": user.user_id,
            "name": user.name,
            "department": user.department,
            "role": user.role.value,
        }

        # Generate access token
        access_token = JWTHandler.create_access_token(token_data)

        return {
            "access_token": access_token,
            "user": user,
        }