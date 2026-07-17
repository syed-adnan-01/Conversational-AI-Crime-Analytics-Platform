from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings


class JWTHandler:
    """Utility class for creating and verifying JWT access tokens."""

    @staticmethod
    def create_access_token(data: dict[str, Any]) -> str:
        """
        Create a signed JWT access token.
        """
        payload = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload.update({"exp": expire})

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def verify_token(token: str) -> dict[str, Any]:
        """
        Verify a JWT and return its payload.
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload

        except JWTError:
            raise ValueError("Invalid or expired token")