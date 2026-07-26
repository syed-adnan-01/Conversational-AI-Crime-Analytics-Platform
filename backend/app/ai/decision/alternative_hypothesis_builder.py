from .decision_models import Hypothesis
class AlternativeHypothesisBuilder:
    def build(self, provenance, confidence):
        return [Hypothesis(description='The available evidence supports the current investigative direction.', supporting_evidence=provenance, confidence=confidence.overall_confidence, reasoning_summary='This is a traceable summary, not a new factual assertion.'), Hypothesis(description='Additional corroboration may change the current investigative direction.', contradicting_evidence=[], confidence=1 - confidence.overall_confidence, reasoning_summary='Uncertainty remains where source modules report low confidence or no evidence.')]
