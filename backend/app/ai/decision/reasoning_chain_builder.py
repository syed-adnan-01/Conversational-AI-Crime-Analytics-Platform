from .decision_models import ReasoningStep
class ReasoningChainBuilder:
    def build(self, provenance, confidence): return [ReasoningStep(statement='Decision is derived only from supplied AI-module outputs.', evidence_ids=[item.source_id for item in provenance], module='decision', confidence=confidence.overall_confidence)]
