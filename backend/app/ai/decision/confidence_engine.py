from .confidence_breakdown import overall
from .decision_models import ConfidenceBreakdown
class ConfidenceEngine:
    def calculate(self, outputs):
        def score(*keys):
            for key in keys:
                value = outputs.get(key, {})
                if isinstance(value, dict):
                    for field in ('confidence', 'overall_confidence', 'reliability'):
                        if isinstance(value.get(field), (int, float)): return float(value[field])
            return 0.0
        agents = outputs.get('agents', {})
        agreement = 1.0 if isinstance(agents, dict) and len(agents) > 1 else 0.0
        return overall(ConfidenceBreakdown(retrieval_confidence=score('retrieval'), evidence_quality=score('investigation', 'evidence'), legal_confidence=score('legal'), timeline_consistency=score('timeline'), graph_confidence=score('graph'), prediction_reliability=score('prediction'), agent_agreement=agreement))
