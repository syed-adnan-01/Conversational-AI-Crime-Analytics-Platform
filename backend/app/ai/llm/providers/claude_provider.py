"""
Anthropic Claude LLM Provider Implementation.
"""

import asyncio
import time
import uuid
from typing import AsyncGenerator, Dict, Any

from app.ai.llm.capabilities import ProviderCapabilities
from app.ai.llm.llm_cost import LLMCostCalculator
from app.ai.llm.llm_models import LLMRequest, LLMResponse, TokenUsage
from app.ai.llm.providers.base import BaseLLMProvider


class ClaudeProvider(BaseLLMProvider):
    """Anthropic Claude 3.5 Sonnet Provider."""

    @property
    def provider_name(self) -> str:
        return "claude"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            provider_name="claude",
            streaming=True,
            json_mode=True,
            tool_calling=True,
            image_input=True,
            multimodal=True,
            max_context_window=200000,
            structured_output=True,
        )

    def count_tokens(self, text: str) -> int:
        return max(1, len(text.strip()) // 4) if text else 0

    def health_check(self) -> bool:
        return True

    def get_model_info(self) -> Dict[str, Any]:
        return {"provider": "claude", "model": "claude-3-5-sonnet", "capabilities": self.capabilities.model_dump()}

    def generate(self, request: LLMRequest) -> LLMResponse:
        start = time.time()
        user_p = request.prompt or (request.prompt_response.user_prompt if request.prompt_response else "")
        sys_p = request.system_prompt or (request.prompt_response.system_prompt if request.prompt_response else "")
        content = "Claude 3.5 Sonnet analysis: Documented investigative reasoning."
        latency = round((time.time() - start) * 1000, 2)
        p_tokens = self.count_tokens(f"{sys_p}\n{user_p}")
        c_tokens = self.count_tokens(content)

        return LLMResponse(
            response_id=f"RES-{uuid.uuid4().hex[:8]}",
            request_id=request.request_id or f"REQ-{uuid.uuid4().hex[:8]}",
            provider="claude",
            model="claude-3-5-sonnet",
            content=content,
            finish_reason="STOP",
            latency_ms=latency,
            token_usage=TokenUsage(prompt_tokens=p_tokens, completion_tokens=c_tokens, total_tokens=p_tokens + c_tokens),
            cost=LLMCostCalculator.calculate_cost("claude-3-5-sonnet", p_tokens, c_tokens),
            safety_passed=True,
        )

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        resp = self.generate(request)
        for chunk in resp.content.split(" "):
            yield chunk + " "
            await asyncio.sleep(0.02)
