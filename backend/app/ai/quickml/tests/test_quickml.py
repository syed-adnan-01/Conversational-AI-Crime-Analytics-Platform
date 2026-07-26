from __future__ import annotations

from fastapi.testclient import TestClient

from app.ai.quickml.knowledge_base_service import KnowledgeBaseService
from app.ai.quickml.quickml_cache import QuickMLCache
from app.ai.quickml.quickml_config import QuickMLConfig
from app.ai.quickml.quickml_models import QuickMLRetrievalResult
from app.main import app


class _StubClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def answer(self, query: str, documents: list[str]) -> QuickMLRetrievalResult:
        self.calls.append((query, documents))
        return QuickMLRetrievalResult(
            query=query,
            answer="Stub answer",
            citations=["DOC-1"],
            confidence=0.77,
            latency_ms=12,
            documents=documents,
        )


def test_knowledge_base_service_retrieve_and_cache() -> None:
    QuickMLCache.clear()
    config = QuickMLConfig.model_construct(
        CATALYST_PROJECT_ID="P1",
        CATALYST_ORG_ID="O1",
        ZOHO_ACCESS_TOKEN="T1",
        QUICKML_DOC_IDS=["DOC-1", "DOC-2"],
        QUICKML_TIMEOUT=1.0,
        QUICKML_MAX_RETRIES=1,
    )
    stub_client = _StubClient()
    service = KnowledgeBaseService(config=config, client=stub_client)

    first = service.retrieve("summarize the case")
    second = service.retrieve("summarize the case")

    assert first.answer == "Stub answer"
    assert first.citations == ["DOC-1"]
    assert second.cached is True
    assert len(stub_client.calls) == 1


def test_kb_health_route() -> None:
    with TestClient(app) as client:
        response = client.get("/ai/copilot/kb/health")

    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "project_id" in body
    assert "configured_documents" in body
    assert "cache_size" in body
    assert "last_query_time" in body