from fastapi import APIRouter

from app.api.routes.home import router as home_router
from app.api.routes.health import router as health_router
from app.api.routes.config import router as config_router

api_router = APIRouter()

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