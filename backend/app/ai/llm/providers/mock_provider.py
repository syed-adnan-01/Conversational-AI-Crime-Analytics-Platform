"""
Mock LLM Provider for offline testing and deterministic test suite execution.
"""

import asyncio
import time
import uuid
from typing import AsyncGenerator, Dict, Any

from app.ai.llm.capabilities import ProviderCapabilities
from app.ai.llm.llm_models import LLMRequest, LLMResponse, TokenUsage
from app.ai.llm.providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):
    """Deterministic Mock Provider returning JSON structured responses."""

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            provider_name="mock",
            streaming=True,
            json_mode=True,
            tool_calling=True,
            image_input=True,
            multimodal=True,
            max_context_window=32768,
            structured_output=True,
        )

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        return max(1, len(text.strip()) // 4)

    def health_check(self) -> bool:
        return True

    def get_model_info(self) -> Dict[str, Any]:
        return {"provider": "mock", "model": "mock-v1", "capabilities": self.capabilities.model_dump()}

    def generate(self, request: LLMRequest) -> LLMResponse:
        start = time.time()
        user_p = request.prompt or (request.prompt_response.user_prompt if request.prompt_response else "")
        schema = request.response_schema

        content = self._get_mock_content(query=user_p, schema=schema)
        latency = round((time.time() - start) * 1000, 2)
        p_tokens = self.count_tokens(user_p)
        c_tokens = self.count_tokens(content)

        return LLMResponse(
            response_id=f"RES-MOCK-{uuid.uuid4().hex[:8]}",
            request_id=request.request_id or f"REQ-MOCK-{uuid.uuid4().hex[:8]}",
            provider="mock",
            model="mock-v1",
            content=content,
            finish_reason="STOP",
            latency_ms=latency,
            token_usage=TokenUsage(prompt_tokens=p_tokens, completion_tokens=c_tokens, total_tokens=p_tokens + c_tokens),
            cost=0.0,
            safety_passed=True,
        )

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        resp = self.generate(request)
        words = resp.content.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.01)

    def _get_mock_content(self, query: str, schema: str | None) -> str:
        if schema == "CaseSummaryOutput":
            return (
                '{\n'
                '  "fir_number": "FIR-2026-001",\n'
                '  "crime_type": "Theft",\n'
                '  "summary": "Stolen smartphone from electronic shop.",\n'
                '  "key_facts": ["CCTV captured suspect"],\n'
                '  "victim_count": 1,\n'
                '  "accused_count": 1,\n'
                '  "status": "INVESTIGATING"\n'
                '}'
            )
        elif schema == "LegalOpinionOutput":
            return (
                '{\n'
                '  "applicable_acts": ["Indian Penal Code"],\n'
                '  "applicable_sections": ["IPC Sec 379"],\n'
                '  "legal_reasoning": "Theft of movable property.",\n'
                '  "evidentiary_requirements": ["CCTV Footage", "Owner Receipt"],\n'
                '  "prosecution_viability": "MEDIUM"\n'
                '}'
            )
        return "Mock LLM Response: Crime analysis completed successfully."
