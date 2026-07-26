"""
Exponential Backoff Retry Engine for resilient LLM calls.
"""

import asyncio
import time
from typing import Callable, TypeVar

from app.ai.llm.exceptions import (
    LLMTimeoutException,
    ProviderExecutionException,
    RateLimitExceededException,
    ResponseValidationException,
)

T = TypeVar("T")


class RetryEngine:
    """Handles automatic retries with exponential backoff for transient provider errors."""

    @classmethod
    def execute_with_retry(
        cls,
        func: Callable[[], T],
        max_retries: int = 3,
        base_delay: float = 0.5,
    ) -> T:
        """Executes func synchronously with exponential backoff retries."""
        last_exception: Exception | None = None
        for attempt in range(max_retries + 1):
            try:
                return func()
            except ResponseValidationException:
                # Do NOT retry validation failures!
                raise
            except (RateLimitExceededException, LLMTimeoutException, ProviderExecutionException, Exception) as e:
                last_exception = e
                if attempt == max_retries:
                    break
                sleep_time = base_delay * (2**attempt)
                time.sleep(sleep_time)

        raise ProviderExecutionException(
            f"Failed after {max_retries} retries. Last error: {str(last_exception)}"
        ) from last_exception

    @classmethod
    async def execute_async_with_retry(
        cls,
        func: Callable[[], T],
        max_retries: int = 3,
        base_delay: float = 0.5,
    ) -> T:
        """Executes async func with exponential backoff retries."""
        last_exception: Exception | None = None
        for attempt in range(max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func()
                return func()
            except ResponseValidationException:
                raise
            except (RateLimitExceededException, LLMTimeoutException, ProviderExecutionException, Exception) as e:
                last_exception = e
                if attempt == max_retries:
                    break
                sleep_time = base_delay * (2**attempt)
                await asyncio.sleep(sleep_time)

        raise ProviderExecutionException(
            f"Async execution failed after {max_retries} retries. Last error: {str(last_exception)}"
        ) from last_exception
