from app.repository.user_repository import UserRepository


def initialize_application() -> None:
    """
    Initialize all application resources.
    """

    UserRepository.initialize()

    print("✅ User repository initialized.")