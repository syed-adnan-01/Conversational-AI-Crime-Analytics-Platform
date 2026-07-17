from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import app_logger
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Register middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestLoggingMiddleware)


# Log startup
app_logger.info("CrimeSphere AI Backend Started")


@app.get("/")
def home():
    app_logger.info("Home endpoint accessed")
    return {
        "message": "Welcome to CrimeSphere AI Backend"
    }


@app.get("/config")
def config():
    app_logger.info("Config endpoint accessed")
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }