"""
Server-Sent Events (SSE) Streaming Response Formatter.
"""

from typing import AsyncGenerator
import json


class StreamingResponseFormatter:
    """Formats async token chunks into SSE compliant payload lines."""

    @staticmethod
    async def format_sse_stream(
        stream_gen: AsyncGenerator[str, None]
    ) -> AsyncGenerator[str, None]:
        """Wraps string chunks in 'data: {...}\n\n' SSE format."""
        async for chunk in stream_gen:
            payload = json.dumps({"delta": chunk, "type": "content"})
            yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"
