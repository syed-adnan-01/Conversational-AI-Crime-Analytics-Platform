import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import api_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        request_id = getattr(request.state, "request_id", "N/A")

        client_ip = request.client.host if request.client else "Unknown"

        user_agent = request.headers.get("User-Agent", "Unknown")

        user = getattr(request.state, "user", "Anonymous")

        api_logger.info(
            "RequestID=%s | IP=%s | User=%s | Method=%s | Path=%s | "
            "Status=%s | Duration=%.2fms | UserAgent=%s",
            request_id,
            client_ip,
            user,
            request.method,
            request.url.path,
            response.status_code,
            duration,
            user_agent,
        )

        return response