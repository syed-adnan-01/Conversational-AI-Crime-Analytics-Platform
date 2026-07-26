from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.core.exceptions import (
    CrimeSphereException,
    crimesphere_exception_handler,
    global_exception_handler,
)
from app.core.logging import app_logger
from app.core.startup import initialize_application
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Initializing CrimeSphere AI...")

    initialize_application()

    app_logger.info("Application initialization completed.")

    yield

    app_logger.info("CrimeSphere AI shutting down...")


app = FastAPI(
    title="CrimeSphere AI",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Next.js frontend
        "http://localhost:5173",   # legacy Vite frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Middlewares
# ------------------------------

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


# ------------------------------
# Exception Handlers
# ------------------------------

app.add_exception_handler(
    CrimeSphereException,
    crimesphere_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# ------------------------------
# API Routers
# ------------------------------

app.include_router(api_router)


# Root health check — AppSail probes this immediately on startup
@app.get("/", include_in_schema=False)
async def root():
    return {"status": "ok", "app": "CrimeSphere AI"}
