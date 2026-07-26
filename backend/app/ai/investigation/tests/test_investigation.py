"""Tests for the AI Investigation Intelligence layer."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.ai.investigation.intelligence.investigation_models import InvestigationRequest
from app.ai.investigation.intelligence.investigation_service import InvestigationService
from app.ai.tests.test_context_builder import clear_all_repositories, setup_sample_case_data
from app.main import app


def _auth_headers(client: TestClient) -> dict[str, str]:
    login_res = client.post(
        "/auth/login",
        json={"employee_id": "EMP001", "password": "password123", "department": "Cyber Crime"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_similarity_engine():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    service = InvestigationService()

    result = service.similar(InvestigationRequest(case_id=case_id, query="fraud digital evidence", top_k=3))
    assert isinstance(result, list)
    assert result == [] or all(item.similarity_score >= 0 for item in result)


def test_evidence_analysis():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    service = InvestigationService()

    insights = service.evidence(InvestigationRequest(case_id=case_id))
    assert len(insights) == 1
    assert insights[0].confidence >= 0
    assert insights[0].strength >= 0


def test_timeline_analysis():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    service = InvestigationService()

    insight = service.timeline(InvestigationRequest(case_id=case_id))
    assert insight.confidence >= 0
    assert isinstance(insight.recommendations, list)


def test_contradictions_and_recommendations():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    service = InvestigationService()

    contradictions = service.contradictions(InvestigationRequest(case_id=case_id))
    recommendations = service.recommend(InvestigationRequest(case_id=case_id, query="fraud investigation"))
    assert isinstance(contradictions, list)
    assert isinstance(recommendations, list)
    assert all(item.priority >= 1 for item in recommendations)


def test_explainability_and_confidence_scoring():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    service = InvestigationService()

    analysis = service.analyze(InvestigationRequest(case_id=case_id, include_graph=True))
    assert analysis.reasoning_trace is not None
    assert analysis.metrics.overall_confidence >= 0
    assert analysis.confidence >= 0


def test_graph_builder_health_and_metrics():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    service = InvestigationService()

    graph = service.build_graph(case_id)
    metrics = service.metrics()
    health = service.health()
    assert graph.case_id == case_id
    assert isinstance(graph.nodes, list)
    assert isinstance(graph.edges, list)
    assert metrics.confidence_level in {"LOW", "MEDIUM", "HIGH"}
    assert health["status"] == "ok"


def test_rest_endpoints():
    clear_all_repositories()
    case_id = setup_sample_case_data()
    client = TestClient(app)

    headers = _auth_headers(client)

    analyze_res = client.post("/ai/investigation/analyze", json={"case_id": case_id, "query": "fraud"}, headers=headers)
    assert analyze_res.status_code == 200
    assert analyze_res.json()["case_id"] == case_id

    similar_res = client.post("/ai/investigation/similar", json={"case_id": case_id, "query": "fraud"}, headers=headers)
    assert similar_res.status_code == 200

    evidence_res = client.post("/ai/investigation/evidence", json={"case_id": case_id}, headers=headers)
    assert evidence_res.status_code == 200

    timeline_res = client.post("/ai/investigation/timeline", json={"case_id": case_id}, headers=headers)
    assert timeline_res.status_code == 200

    contradiction_res = client.post("/ai/investigation/contradictions", json={"case_id": case_id}, headers=headers)
    assert contradiction_res.status_code == 200

    recommend_res = client.post("/ai/investigation/recommend", json={"case_id": case_id}, headers=headers)
    assert recommend_res.status_code == 200

    completeness_res = client.post("/ai/investigation/completeness", json={"case_id": case_id}, headers=headers)
    assert completeness_res.status_code == 200

    legal_res = client.post("/ai/investigation/legal", json={"case_id": case_id}, headers=headers)
    assert legal_res.status_code == 200

    graph_res = client.get(f"/ai/investigation/graph/{case_id}", headers=headers)
    assert graph_res.status_code == 200
    assert graph_res.json()["case_id"] == case_id

    metrics_res = client.get("/ai/investigation/metrics")
    assert metrics_res.status_code == 200

    health_res = client.get("/ai/investigation/health")
    assert health_res.status_code == 200
    assert health_res.json()["status"] == "ok"
