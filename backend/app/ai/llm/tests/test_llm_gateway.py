"""
Comprehensive Unit and Integration Tests for Phase 3.5 Enterprise LLM Gateway & AI Orchestrator.
"""

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.ai.llm.capabilities import ProviderCapabilities
from app.ai.llm.config import llm_config
from app.ai.llm.exceptions import ProviderNotFoundException, ResponseValidationException
from app.ai.llm.llm_cache import LLMCache
from app.ai.llm.llm_cost import LLMCostCalculator
from app.ai.llm.llm_gateway import LLMGateway
from app.ai.llm.llm_metrics import LLMMetrics
from app.ai.llm.llm_models import LLMRequest, LLMResponse
from app.ai.llm.llm_registry import ProviderRegistry
from app.ai.llm.llm_service import LLMService
from app.ai.llm.providers.catalyst_quickml_provider import CatalystQuickMLProvider
from app.ai.llm.providers.gemini_provider import GeminiProvider
from app.ai.llm.providers.mock_provider import MockLLMProvider
from app.ai.llm.response_parser import StructuredResponseParser
from app.ai.llm.retry import RetryEngine
from app.ai.llm.safety import SafetyValidator
from app.ai.llm.conversation import ConversationManager
from app.ai.llm.tools.registry import ToolRegistry
from app.ai.llm.tools.tool_models import ToolCall
from app.ai.orchestrator.ai_orchestrator import AIOrchestrator
from app.ai.orchestrator.workflow import OrchestrationRequest
from app.auth.dependencies import get_current_user
from app.models.user import User


# Setup authenticated test client
@pytest.fixture
def client():
    def mock_get_current_user():
        return User(
            user_id="USR-TEST-001",
            employee_id="EMP-100",
            name="Test Investigator",
            email="investigator@crimesphere.gov.in",
            role="investigator",
            department="Crime Branch",
            full_name="Test Investigator",
        )

    app.dependency_overrides[get_current_user] = mock_get_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_provider_registry():
    """Verify ProviderRegistry registration and default retrieval."""
    providers = ProviderRegistry.list_providers()
    assert "quickml" in providers
    assert "gemini" in providers
    assert "mock" in providers

    quickml_p = ProviderRegistry.get("quickml")
    assert quickml_p.provider_name == "quickml"
    assert quickml_p.capabilities.structured_output is True

    gemini_p = ProviderRegistry.get("gemini")
    assert gemini_p.provider_name == "gemini"

    mock_p = ProviderRegistry.get("mock")
    assert mock_p.provider_name == "mock"


def test_quickml_provider_generation():
    """Verify CatalystQuickMLProvider generation."""
    provider = CatalystQuickMLProvider()
    req = LLMRequest(prompt="Summarize financial fraud case", provider="quickml")
    resp = provider.generate(req)

    assert resp.provider == "quickml"
    assert resp.content != ""
    assert resp.token_usage.total_tokens > 0
    assert resp.cost >= 0.0


def test_gemini_provider_generation():
    """Verify GeminiProvider generation and capabilities."""
    provider = GeminiProvider()
    req = LLMRequest(prompt="Analyze CCTV video evidence", provider="gemini")
    resp = provider.generate(req)

    assert resp.provider == "gemini"
    assert provider.capabilities.multimodal is True
    assert provider.capabilities.tool_calling is True


def test_mock_provider_generation():
    """Verify MockLLMProvider generation with structured schema parsing."""
    provider = MockLLMProvider()
    req = LLMRequest(
        prompt="Get case summary",
        provider="mock",
        response_schema="CaseSummaryOutput",
    )
    resp = provider.generate(req)
    assert resp.provider == "mock"

    parsed = StructuredResponseParser.parse_and_validate(resp.content, "CaseSummaryOutput")
    assert parsed is not None
    assert parsed["fir_number"] == "FIR-2026-001"


def test_llm_cost_calculator():
    """Verify cost calculation across different providers."""
    cost_quickml = LLMCostCalculator.calculate_cost("quickml", 1000, 1000)
    assert cost_quickml == 0.0003

    cost_gemini = LLMCostCalculator.calculate_cost("gemini-2.5-pro", 1000, 1000)
    assert cost_gemini == 0.00625

    cost_mock = LLMCostCalculator.calculate_cost("mock", 1000, 1000)
    assert cost_mock == 0.0


def test_structured_response_parser_validation():
    """Verify structured response parsing and error handling."""
    valid_json = '```json\n{\n  "fir_number": "FIR-123",\n  "crime_type": "Theft",\n  "summary": "Sample summary text",\n  "key_facts": ["Fact 1"],\n  "victim_count": 1,\n  "accused_count": 1,\n  "status": "REGISTERED"\n}\n```'
    parsed = StructuredResponseParser.parse_and_validate(valid_json, "CaseSummaryOutput")
    assert parsed is not None
    assert parsed["fir_number"] == "FIR-123"

    invalid_json = '{"invalid": "data"}'
    with pytest.raises(ResponseValidationException):
        StructuredResponseParser.parse_and_validate(invalid_json, "CaseSummaryOutput")


def test_safety_validator():
    """Verify SafetyValidator disclaimers and empty content detection."""
    is_safe, violations = SafetyValidator.validate_safety("")
    assert is_safe is False
    assert "content is empty" in violations[0]

    is_safe, violations = SafetyValidator.validate_safety("As a large language model, I cannot browsing")
    assert is_safe is False

    is_safe, violations = SafetyValidator.validate_safety("Clean legal reasoning statement.")
    assert is_safe is True


def test_llm_cache():
    """Verify LLMCache storing and retrieving cached responses."""
    LLMCache.clear()
    req = LLMRequest(prompt="Deterministic cached query", provider="mock")

    cached_1 = LLMCache.get(req)
    assert cached_1 is None

    resp = LLMService.generate(req)
    assert resp.cached is False

    cached_2 = LLMCache.get(req)
    assert cached_2 is not None
    assert cached_2.cached is True


def test_retry_engine():
    """Verify RetryEngine retries on temporary failures."""
    calls = 0

    def flaky_func():
        nonlocal calls
        calls += 1
        if calls < 2:
            raise Exception("Temporary Network Failure")
        return "Success"

    res = RetryEngine.execute_with_retry(flaky_func, max_retries=2, base_delay=0.01)
    assert res == "Success"
    assert calls == 2


def test_tool_registry_and_execution():
    """Verify ToolRegistry definition listings and execution dispatch."""
    defs = ToolRegistry.list_definitions()
    names = [d.name for d in defs]
    assert "search_case" in names
    assert "get_timeline" in names

    call = ToolCall(call_id="CALL-1", tool_name="search_case", arguments={"query": "fraud"})
    res = ToolRegistry.execute_tool(call)
    assert res.success is True
    assert res.output[0]["case_id"] == "CM-881"


def test_conversation_manager():
    """Verify ConversationManager history tracking."""
    ConversationManager.clear()
    cid = "CONV-SESSION-100"
    ConversationManager.append_turn(cid, "user", "What is the FIR status?")
    ConversationManager.append_turn(cid, "assistant", "The FIR is registered.")

    history = ConversationManager.get_history(cid)
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"


def test_llm_api_endpoints(client: TestClient):
    """Verify FastAPI routes for LLM Gateway."""
    # 1. POST /ai/llm/generate
    resp = client.post(
        "/ai/llm/generate",
        json={"prompt": "Summarize case", "provider": "mock", "response_schema": "CaseSummaryOutput"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["provider"] == "mock"
    assert body["parsed_output"]["fir_number"] == "FIR-2026-001"

    # 2. GET /ai/llm/providers
    resp_p = client.get("/ai/llm/providers")
    assert resp_p.status_code == 200
    assert "quickml" in resp_p.json()

    # 3. GET /ai/llm/capabilities
    resp_cap = client.get("/ai/llm/capabilities?provider=quickml")
    assert resp_cap.status_code == 200
    cap_data = resp_cap.json()
    assert cap_data["provider"] == "quickml"
    assert cap_data["capabilities"]["structured_output"] is True

    # 4. GET /ai/llm/health
    resp_h = client.get("/ai/llm/health")
    assert resp_h.status_code == 200
    assert resp_h.json()["status"] == "HEALTHY"

    # 5. GET /ai/llm/metrics
    resp_m = client.get("/ai/llm/metrics")
    assert resp_m.status_code == 200
    assert resp_m.json()["total_requests"] >= 1

    # 6. DELETE /ai/llm/cache
    resp_c = client.delete("/ai/llm/cache")
    assert resp_c.status_code == 200
    assert "cleared successfully" in resp_c.json()["message"]
