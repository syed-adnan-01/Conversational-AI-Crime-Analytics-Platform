from __future__ import annotations
import json
from time import perf_counter
from .alternative_hypothesis_builder import AlternativeHypothesisBuilder
from .auditing import DecisionAudit
from .cache import DecisionCache
from .confidence_engine import ConfidenceEngine
from .decision_models import DecisionResponse
from .evidence_provenance import EvidenceProvenanceBuilder
from .hypothesis_engine import HypothesisEngine
from .metrics import MetricsTracker
from .reasoning_chain_builder import ReasoningChainBuilder
from .recommendation_engine import RecommendationEngine
from .tracing import DecisionTracer
from .validator import DecisionValidator

class DecisionEngine:
    """Transforms public AI service outputs into transparent decisions; never reads repositories."""
    def __init__(self, confidence=None, provenance=None, recommendations=None, hypotheses=None, reasoning=None, validator=None, cache=None, metrics=None, tracer=None, audit=None):
        self.confidence = confidence or ConfidenceEngine(); self.provenance = provenance or EvidenceProvenanceBuilder(); self.recommendations = recommendations or RecommendationEngine(); self.hypotheses = hypotheses or HypothesisEngine(); self.reasoning = reasoning or ReasoningChainBuilder(); self.validator = validator or DecisionValidator(); self.cache = cache or DecisionCache(); self.metrics = metrics or MetricsTracker(); self.tracer = tracer or DecisionTracer(); self.audit = audit or DecisionAudit()
    def analyze(self, request):
        key = json.dumps(request.model_dump(mode='json'), sort_keys=True)
        cached = self.cache.get(key)
        if cached: self.metrics.record(0, cached=True); return cached
        started = perf_counter()
        try:
            confidence = self.confidence.calculate(request.source_outputs); provenance = self.provenance.build(request.source_outputs); reasoning = self.reasoning.build(provenance, confidence)
            response = DecisionResponse(case_id=request.case_id, recommendations=self.recommendations.generate(request, provenance, confidence, reasoning), hypotheses=self.hypotheses.generate(provenance, confidence), confidence=confidence, provenance=provenance, status=request.status)
            self.validator.validate(response); self.cache.put(key, response); self.tracer.record(response.decision_id, 'analyzed', recommendation_count=len(response.recommendations)); self.audit.record(response.decision_id, 'created', case_id=request.case_id); self.metrics.record((perf_counter()-started)*1000); return response
        except Exception:
            self.metrics.record((perf_counter()-started)*1000, failed=True); raise
