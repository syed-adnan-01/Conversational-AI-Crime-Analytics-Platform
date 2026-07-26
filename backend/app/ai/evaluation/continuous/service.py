import json
from time import perf_counter
from .audit import EvaluationAudit
from .benchmark_runner import BenchmarkRunner
from .cache import EvaluationCache
from .citation_validator import CitationValidator
from .datasets import DatasetRegistry
from .hallucination_detector import HallucinationDetector
from .metrics_engine import MetricsEngine
from .models import EvaluationResponse
from .quality_scorers import QualityScorers
from .reporting import ReportGenerator
from .tracing import EvaluationTracer
class EvaluationService:
    """Evaluates supplied public-module outputs only; it never invokes repositories or AI modules."""
    def __init__(self, scorers=None, detector=None, citations=None, cache=None, metrics=None, audit=None, tracer=None, datasets=None, reports=None):
        self.scorers = scorers or QualityScorers(); self.detector = detector or HallucinationDetector(); self.citations = citations or CitationValidator(); self.cache = cache or EvaluationCache(); self.metrics = metrics or MetricsEngine(); self.audit = audit or EvaluationAudit(); self.tracer = tracer or EvaluationTracer(); self.datasets = datasets or DatasetRegistry(); self.reports = reports or ReportGenerator(); self.history = []
    def evaluate(self, request):
        cache_payload = request.model_dump(mode='json')
        cache_payload.pop('request_id', None)
        key = json.dumps(cache_payload, sort_keys=True); cached = self.cache.get(key)
        if cached: self.metrics.record(0, cache_hit=True); return cached
        started = perf_counter()
        try:
            issues = self.detector.detect(request.output, request.expected) + self.citations.validate(request.output, request.expected)
            result = EvaluationResponse(module=request.module, scores=self.scorers.score(request), issues=issues, feedback=request.feedback)
            self.cache.put(key, result); self.history.append(result); self.audit.record('evaluated', evaluation_id=result.evaluation_id, module=request.module); self.tracer.record('evaluated', evaluation_id=result.evaluation_id); self.metrics.record((perf_counter()-started)*1000); return result
        except Exception:
            self.metrics.record((perf_counter()-started)*1000, failed=True); raise
    def benchmark(self, suite): return BenchmarkRunner(self).run(suite)
    def report(self): return self.reports.summary(self.history)
    def leaderboard(self): return sorted(({ 'module': item.module, 'score': item.scores.overall } for item in self.history), key=lambda item: item['score'], reverse=True)
    def health(self): return {'status': 'healthy', 'cache': self.cache.stats(), 'feedback_count': sum(item.feedback is not None for item in self.history)}
