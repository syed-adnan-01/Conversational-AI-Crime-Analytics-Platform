"""
Before Request Middleware for parameter enrichment and validation.
"""

import uuid
from app.ai.llm.config import llm_config
from app.ai.llm.llm_models import LLMRequest


class BeforeRequestMiddleware:
    """Processes LLMRequest prior to execution."""

    @classmethod
    def process(cls, request: LLMRequest) -> LLMRequest:
        """Injects request_id, defaults, and normalizes request parameters."""
        if not request.request_id:
            request.request_id = f"REQ-{uuid.uuid4().hex[:8]}"

        if not request.provider:
            request.provider = llm_config.ACTIVE_PROVIDER

        if not request.model:
            request.model = llm_config.DEFAULT_MODEL

        return request
