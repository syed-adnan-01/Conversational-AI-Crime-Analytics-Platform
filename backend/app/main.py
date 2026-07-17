from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import app_logger

from app.core.exceptions import (
    CrimeSphereException,
    crimesphere_exception_handler,
    global_exception_handler,
)

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware

from app.api.api import api_router


# --------------------------------------------------
# Create FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


# --------------------------------------------------
# Register Middlewares
# --------------------------------------------------

# FastAPI executes middleware in reverse order.
# RequestIDMiddleware must execute before RequestLoggingMiddleware,
# so RequestLoggingMiddleware is registered first.

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)


# --------------------------------------------------
# Register Exception Handlers
# --------------------------------------------------

app.add_exception_handler(
    CrimeSphereException,
    crimesphere_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# --------------------------------------------------
# Register API Routers
# --------------------------------------------------

app.include_router(api_router)


# --------------------------------------------------
# Startup Log
# --------------------------------------------------

app_logger.info("CrimeSphere AI Backend Started")