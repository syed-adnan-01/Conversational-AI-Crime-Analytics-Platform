from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
def config():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }