from .decision_engine import DecisionEngine
from .explainability_engine import ExplainabilityEngine
class DecisionService:
    def __init__(self, engine=None, explainability=None): self.engine = engine or DecisionEngine(); self.explainability = explainability or ExplainabilityEngine()
    def analyze(self, request): return self.engine.analyze(request)
    def recommendations(self, request): return self.analyze(request).recommendations
    def hypotheses(self, request): return self.analyze(request).hypotheses
    def confidence(self, request): return self.analyze(request).confidence
    def explanation(self, request, recommendation_id):
        recommendation = next((item for item in self.analyze(request).recommendations if item.recommendation_id == recommendation_id), None)
        return self.explainability.explain(recommendation) if recommendation else None
    def audit(self): return self.engine.audit.entries
    def metrics(self): return self.engine.metrics.metrics
    def health(self): return {'status': 'healthy', 'cache': self.engine.cache.statistics(), 'traces': len(self.engine.tracer.traces)}
