from app.ai.decision.decision_models import DecisionRequest
from app.ai.decision.decision_service import DecisionService

def request(): return DecisionRequest(case_id='C1', source_outputs={'retrieval': {'confidence': .8, 'retrieved_chunk_references': ['chunk-1']}, 'evidence': {'confidence': .7, 'missing_evidence': ['CCTV footage'], 'evidence_references': ['EV-1']}, 'legal': {'confidence': .6}, 'agents': {'evidence-agent': {}, 'legal-agent': {}}})
def test_decision_has_explainable_recommendation_and_provenance():
    response = DecisionService().analyze(request())
    assert response.recommendations[0].reasoning_chain and response.recommendations[0].supporting_evidence
    assert response.confidence.overall_confidence > 0 and response.provenance[0].source_id == 'chunk-1'
def test_hypotheses_and_cache():
    service = DecisionService(); first = service.analyze(request()); second = service.analyze(request())
    assert len(first.hypotheses) == 2 and first.decision_id == second.decision_id and service.metrics().cache_hits == 1
