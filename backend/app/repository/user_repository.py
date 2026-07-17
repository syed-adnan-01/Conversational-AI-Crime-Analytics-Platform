from copy import deepcopy
from typing import Optional

from app.core.password import PasswordManager
from app.models.user import User
from app.repository.seed_users import SEED_USERS


class UserRepository:
    """
    Repository responsible for retrieving user data.

    During development, user data is loaded from SEED_USERS.
    Passwords are automatically hashed once during initialization
    so that authentication behaves like a production system.
    """

    # Internal in-memory user store
    _users = []

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the in-memory user store by hashing
        all seed passwords.
        """

        if cls._users:
            return

        for user in SEED_USERS:
            print("Before hashing:", repr(user["password"]))
            print("Length:", len(user["password"]))

            user_copy = deepcopy(user)

            user_copy["password"] = PasswordManager.hash_password(
                user["password"]
            )

            print("After hashing:", user_copy["password"])

            cls._users.append(user_copy)

    @classmethod
    def get_by_employee_id(cls, employee_id: str) -> Optional[dict]:
        """
        Retrieve a user by employee ID.
        """

        cls.initialize()

        return next(
            (
                user
                for user in cls._users
                if user["employee_id"] == employee_id
            ),
            None,
        )

    @classmethod
    def get_user(cls, employee_id: str) -> Optional[User]:
        """
        Retrieve a User model by employee ID.
        """

        user_data = cls.get_by_employee_id(employee_id)

        if user_data is None:
            return None

        return User(**user_data)