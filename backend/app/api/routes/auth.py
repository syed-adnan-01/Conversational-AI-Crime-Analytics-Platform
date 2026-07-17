from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.logging import auth_logger

router = APIRouter()


@router.get(
    "/me",
    summary="Current User",
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """
    return current_user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate User",
    description="Authenticate a user using Employee ID, Password, and Department.",
)
async def login(login_data: LoginRequest):
    """
    Authenticate user and return an access token.
    """

    result = AuthService.login(
        employee_id=login_data.employee_id,
        password=login_data.password,
        department=login_data.department,
    )

    if result is None:
        auth_logger.warning(
            "Failed login attempt for Employee ID: %s",
            login_data.employee_id,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid employee ID, password, or department.",
        )

    auth_logger.info(
        "User '%s' logged in successfully.",
        result["user"].employee_id,
    )

    return TokenResponse(
        access_token=result["access_token"]
    )