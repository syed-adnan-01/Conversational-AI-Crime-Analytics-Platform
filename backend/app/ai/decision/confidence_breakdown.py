from .decision_models import ConfidenceBreakdown
def overall(values: ConfidenceBreakdown) -> ConfidenceBreakdown:
    factors = [values.retrieval_confidence, values.evidence_quality, values.legal_confidence, values.timeline_consistency, values.graph_confidence, values.prediction_reliability, values.agent_agreement]
    values.overall_confidence = sum(factors) / len(factors)
    values.explanation = 'Overall confidence is the unweighted mean of seven transparent component scores.'
    return values
