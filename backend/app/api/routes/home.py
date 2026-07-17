from fastapi import APIRouter

from app.core.logging import app_logger

router = APIRouter()


@router.get("/")
def home():
    app_logger.info("Home endpoint accessed")
    return {
        "message": "Welcome to CrimeSphere AI Backend"
    }