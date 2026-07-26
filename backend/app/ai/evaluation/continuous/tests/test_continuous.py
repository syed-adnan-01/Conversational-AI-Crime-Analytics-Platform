from app.ai.evaluation.continuous.models import BenchmarkSuite, EvaluationRequest, Feedback
from app.ai.evaluation.continuous.service import EvaluationService
def sample(): return EvaluationRequest(module='decision', output={'retrieved_ids': ['a', 'b'], 'claims': ['supported', 'invented'], 'citations': ['a', 'bad'], 'entities': ['Suspect A', 'Ghost'], 'recommendations': [{'explanation': 'Need CCTV', 'supporting_evidence': ['a']}], 'confidence': .8}, expected={'relevant_ids': ['a'], 'k': 2, 'supported_claims': ['supported'], 'citations': ['a'], 'entities': ['Suspect A'], 'outcome': 1}, feedback=Feedback(thumbs_up=True, accepted_recommendation_ids=['r1']))
def test_metrics_and_hallucinations():
    result = EvaluationService().evaluate(sample())
    assert result.scores.retrieval['precision_at_k'] == .5
    assert {issue.category for issue in result.issues} >= {'unsupported_claim', 'fabricated_entity', 'evidence_mismatch'}
def test_benchmark_feedback_and_cache():
    service = EvaluationService(); first = service.evaluate(sample()); second = service.evaluate(sample()); report = service.benchmark(BenchmarkSuite(name='suite', cases=[sample()]))
    assert first.evaluation_id == second.evaluation_id and service.metrics.snapshot().cache_hits >= 1 and report.total == 1
