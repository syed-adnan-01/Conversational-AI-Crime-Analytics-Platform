"""
Comprehensive Unit & Integration Test Suite for the CrimeSphere AI Prompt Engine.
"""

from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient

from app.ai.prompting.exceptions import PromptValidationException, TemplateNotFoundException
from app.ai.prompting.guardrails import SafetyGuardrails
from app.ai.prompting.llm_profiles import GeminiProfile, QuickMLProfile, get_llm_profile
from app.ai.prompting.output_schema_registry import OutputSchemaRegistry
from app.ai.prompting.prompt_builder import PromptBuilder
from app.ai.prompting.prompt_cache import PromptCache
from app.ai.prompting.prompt_intents import PromptIntent
from app.ai.prompting.prompt_metadata import PromptMetadataFactory
from app.ai.prompting.prompt_metrics import PromptMetrics
from app.ai.prompting.prompt_models import (
    ConversationTurn,
    PromptPersona,
    PromptRequest,
    PromptResponse,
    PromptType,
)
from app.ai.prompting.prompt_optimizer import PromptOptimizer
from app.ai.prompting.prompt_profiles import PromptProfile
from app.ai.prompting.prompt_quality import PromptQualityEvaluator
from app.ai.prompting.prompt_registry import PromptRegistry
from app.ai.prompting.prompt_sections import PromptSection
from app.ai.prompting.prompt_service import PromptService
from app.ai.prompting.prompt_templates import TemplateEngine
from app.ai.prompting.prompt_validator import PromptValidator
from app.ai.prompting.prompt_variables import PromptVariables
from app.ai.prompting.token_budget_manager import TokenBudgetManager
from app.ai.retrieval.retrieval_models import (
    PromptProvenance,
    PromptSections,
    RetrievalContext,
    RetrievalStatistics,
)
from app.main import app


@pytest.fixture
def mock_retrieval_context():
    """Provides a sample RetrievalContext object."""
    sections = PromptSections(
        system_context="Case context system info",
        case_summary="FIR No. 102/2026 registered under IPC 302.",
        victims="Victim: John Doe, Age: 34.",
        accused="Accused: Jane Smith, Status: Arrested.",
        evidence="Seized Weapon: Knife (Ex. 1).",
        timeline="10:00 AM - Incident reported.",
        legal="IPC Section 302 - Murder.",
        question="What is the evidence against Jane Smith?",
    )
    provenance = PromptProvenance(
        query_id="Q-123",
        retrieval_id="RET-456",
        chunk_ids=["CHK-1", "CHK-2"],
        generated_at=datetime.now(timezone.utc),
        context_hash="a1b2c3d4e5f67890",
    )
    stats = RetrievalStatistics(
        total_chunks_searched=10,
        candidates_after_filtering=5,
        final_chunks_assembled=2,
        assembly_time_ms=12.5,
    )
    return RetrievalContext(
        version="1.0.0",
        query="What is the evidence against Jane Smith?",
        assembled_text="Full assembled text content",
        sections=sections,
        chunks=[],
        token_count=150,
        max_token_budget=4096,
        provenance=provenance,
        statistics=stats,
    )


def test_template_engine():
    """Tests placeholder substitution in TemplateEngine."""
    template = "System: {{system_instructions}}\nQuestion: {{question}}"
    vars = PromptVariables(system_instructions="You are an investigator.", question="Who is accused?")
    rendered = TemplateEngine.render(template, vars)
    assert "System: You are an investigator." in rendered
    assert "Question: Who is accused?" in rendered
    assert len(TemplateEngine.find_unresolved_placeholders(rendered)) == 0


def test_prompt_optimizer():
    """Tests text deduplication and whitespace optimization."""
    raw = "Line 1\nLine 1\n\n\n\nLine 2   with   extra   spaces"
    opt, orig_len, opt_len = PromptOptimizer.optimize(raw)
    assert "Line 1\n\nLine 2 with extra spaces" in opt
    assert opt_len < orig_len


def test_token_budget_manager():
    """Tests token estimation and text trimming."""
    text = "Word " * 100
    est = TokenBudgetManager.estimate_tokens(text)
    assert est > 0
    trimmed = TokenBudgetManager.trim_to_budget(text, max_tokens=10)
    assert "[Truncated due to token budget]" in trimmed


def test_prompt_registry():
    """Tests dynamic template and version manifest loading."""
    content, meta, stem = PromptRegistry.get_template(PromptType.SUMMARY, "1.0.0")
    assert "CASE CONTEXT DATA" in content or "summary" in content.lower()
    assert meta.version == "1.0.0"
    assert stem == "summary.md"


def test_prompt_validator():
    """Tests prompt validation checks."""
    assert PromptValidator.validate("System text", "User text", max_budget=4096) is True
    with pytest.raises(PromptValidationException):
        PromptValidator.validate("", "")

    with pytest.raises(PromptValidationException):
        PromptValidator.validate("Unresolved {{missing_key}}", "User query")


def test_llm_profiles():
    """Tests LLM capability profile retrieval and hints."""
    gemini = get_llm_profile("gemini")
    assert isinstance(gemini, GeminiProfile)
    assert gemini.maximum_context == 1048576

    quickml = get_llm_profile("quickml")
    assert isinstance(quickml, QuickMLProfile)
    assert quickml.supports_images is False


def test_output_schema_registry():
    """Tests output schema instructions generation."""
    instr = OutputSchemaRegistry.get_formatting_instructions(PromptType.SUMMARY)
    assert "CRITICAL OUTPUT FORMATTING INSTRUCTIONS" in instr
    assert "CaseSummaryOutput" in instr


def test_prompt_quality_evaluator():
    """Tests quality score calculation."""
    res = PromptQualityEvaluator.evaluate(
        system_prompt=SafetyGuardrails.get_guardrails_text(),
        user_prompt="Question: What happened?",
        max_budget=4096,
        estimated_tokens=200,
    )
    assert res["quality_score"] == 100.0
    assert res["passed_validation"] is True


def test_prompt_builder_full_flow(mock_retrieval_context):
    """Tests end-to-end prompt construction using PromptBuilder."""
    builder = PromptBuilder()
    req = PromptRequest(
        query="Explain evidence against Jane Smith",
        retrieval_context=mock_retrieval_context,
        prompt_type=PromptType.EVIDENCE_ANALYSIS,
        persona=PromptPersona.INVESTIGATOR,
        profile=PromptProfile.POLICE_INVESTIGATION,
        intent=PromptIntent.ANALYZE,
        conversation_id="CONV-789",
        history=[
            ConversationTurn(role="user", content="Initiate case review"),
            ConversationTurn(role="assistant", content="Case 102/2026 loaded."),
        ],
    )
    resp = builder.build(req, use_cache=False)
    assert isinstance(resp, PromptResponse)
    assert "Senior Criminal Investigator" in resp.system_prompt
    assert "Jane Smith" in resp.user_prompt
    assert resp.metadata.prompt_id.startswith("PRM-")
    assert resp.metadata.quality_score >= 70.0
    assert resp.debug is not None
    assert resp.trace is not None


def test_prompt_service(mock_retrieval_context):
    """Tests PromptService methods."""
    PromptCache.clear()
    PromptMetrics.reset()

    service = PromptService()
    req = PromptRequest(
        query="Draft summary",
        retrieval_context=mock_retrieval_context,
        prompt_type=PromptType.SUMMARY,
    )
    resp = service.build_prompt(req)
    assert resp.metadata.prompt_type == PromptType.SUMMARY

    preview = service.preview_prompt(req)
    assert "system_prompt" in preview
    assert "user_prompt" in preview

    templates = service.list_templates()
    assert len(templates) > 0

    personas = service.list_personas()
    assert "investigator" in personas

    metrics = service.get_metrics()
    assert metrics["total_prompts_built"] >= 1


def test_prompt_routes():
    """Integration test verifying REST API endpoints."""
    from app.auth.dependencies import get_current_user
    from app.models.user import User

    def override_get_current_user():
        return User(
            user_id="USR-999",
            employee_id="EMP001",
            name="Test Investigator",
            email="investigator@crimesphere.gov.in",
            role="investigator",
            department="Cyber Crime",
            full_name="Test Investigator",
        )

    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)

    # Test POST /ai/prompt
    payload = {
        "query": "Who is the accused?",
        "prompt_type": "summary",
        "persona": "investigator",
        "profile": "police_investigation",
        "intent": "question",
    }
    res = client.post("/ai/prompt", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "system_prompt" in data
    assert "user_prompt" in data
    assert data["metadata"]["prompt_id"].startswith("PRM-")

    # Test GET /ai/prompt/templates
    res_t = client.get("/ai/prompt/templates")
    assert res_t.status_code == 200
    assert isinstance(res_t.json(), list)

    # Test GET /ai/prompt/personas
    res_p = client.get("/ai/prompt/personas")
    assert res_p.status_code == 200
    assert "investigator" in res_p.json()

    # Test GET /ai/prompt/metrics
    res_m = client.get("/ai/prompt/metrics")
    assert res_m.status_code == 200
    assert "total_prompts_built" in res_m.json()

    app.dependency_overrides.clear()

