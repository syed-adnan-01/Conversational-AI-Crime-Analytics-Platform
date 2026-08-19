import os
import sys

# Ensure root backend directory is in sys.path when executed directly via python app/main.py
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

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

    try:
        initialize_application()
        app_logger.info("Application initialization completed.")
    except Exception as e:
        app_logger.warning("Application initialization warning: %s", e)

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
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https://.*\.catalystserverless\.(com|in)|https://.*\.zohocatalyst\.(com|in)|https://.*\.catalystappsail\.(com|in)|https://.*\.zohoslate\.(com|in)|https://.*\.zohosites\.(com|in)|https://.*\.zoho\.(com|in)|http://localhost:\d+|http://127\.0\.0\.1:\d+",
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
    return {
        "status": "ok",
        "app": "CrimeSphere AI",
        "listen_port_env": os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT"),
        "port_env": os.environ.get("PORT"),
    }


if __name__ == "__main__":
    import os
    import sys
    import uvicorn

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    port_str = os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT") or os.environ.get("PORT") or "9000"
    try:
        port = int(port_str)
    except ValueError:
        port = 9000

    app_logger.info(f"Binding AppSail Uvicorn server on 0.0.0.0:{port}...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)

