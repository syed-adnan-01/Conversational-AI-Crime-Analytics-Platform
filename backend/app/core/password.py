from passlib.context import CryptContext

# Configure bcrypt hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class PasswordManager:
    """
    Utility class for password hashing and verification.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain text password against a hash.
        """
        return pwd_context.verify(
            plain_password,
            hashed_password,
        )