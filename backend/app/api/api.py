from fastapi import APIRouter

from app.api.routes.home import router as home_router
from app.api.routes.health import router as health_router
from app.api.routes.config import router as config_router
from app.api.routes.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)

# Home Routes
api_router.include_router(
    home_router,
    tags=["Home"],
)

# Health Routes
api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

# Configuration Routes
api_router.include_router(
    config_router,
    prefix="/config",
    tags=["Configuration"],
)
# Authentication Routes
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)