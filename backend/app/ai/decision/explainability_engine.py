class ExplainabilityEngine:
    def explain(self, recommendation):
        return {'recommendation_id': recommendation.recommendation_id, 'explanation': recommendation.explanation, 'reasoning_chain': recommendation.reasoning_chain, 'supporting_evidence': recommendation.supporting_evidence, 'conflicting_evidence': recommendation.conflicting_evidence, 'confidence': recommendation.confidence, 'uncertainty_indicators': recommendation.uncertainty_indicators}
