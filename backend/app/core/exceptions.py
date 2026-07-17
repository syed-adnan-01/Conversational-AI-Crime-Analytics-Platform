from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import error_logger


class CrimeSphereException(Exception):
    """
    Base exception for application-specific errors.
    """

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def crimesphere_exception_handler(
    request: Request,
    exc: CrimeSphereException,
):
    request_id = getattr(request.state, "request_id", "N/A")

    error_logger.error(
        "RequestID=%s | Path=%s | Error=%s",
        request_id,
        request.url.path,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "request_id": request_id,
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    request_id = getattr(request.state, "request_id", "N/A")

    error_logger.exception(
        "RequestID=%s | Path=%s",
        request_id,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "request_id": request_id,
        },
    )