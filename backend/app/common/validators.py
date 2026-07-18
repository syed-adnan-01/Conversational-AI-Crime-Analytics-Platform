import re
from typing import Optional
from app.core.exceptions import CrimeSphereException


class InvalidInputException(CrimeSphereException):
    """Raised when user input violates validation constraints."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=422,
        )


# Regex for Indian phone numbers (10 digits, optionally prefixed with +91)
# and general E.164 formats
PHONE_REGEX = re.compile(r"^(\+91[\-\s]?)?[6-9]\d{9}$|^\+?[1-9]\d{6,14}$")


# Simple robust email regex
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_phone(phone: Optional[str]) -> Optional[str]:
    """
    Validate phone number format.
    Raises InvalidInputException if the format is invalid.
    """
    if not phone:
        return None

    cleaned = phone.strip()
    if not PHONE_REGEX.match(cleaned):
        raise InvalidInputException(
            "Invalid mobile number format. Must be a valid 10-digit number optionally prefixed with +91."
        )

    return cleaned


def validate_email(email: Optional[str]) -> Optional[str]:
    """
    Validate email address format.
    Raises InvalidInputException if the format is invalid.
    """
    if not email:
        return None

    cleaned = email.strip().lower()
    if not EMAIL_REGEX.match(cleaned):
        raise InvalidInputException("Invalid email format.")

    return cleaned
