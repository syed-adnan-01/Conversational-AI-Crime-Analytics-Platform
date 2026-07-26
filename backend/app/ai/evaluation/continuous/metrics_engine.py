from .models import EvaluationMetrics
class MetricsEngine:
    def __init__(self): self.metrics = EvaluationMetrics()
    def record(self, latency_ms, cache_hit=False, failed=False): self.metrics.evaluations += 1; self.metrics.successful += int(not failed); self.metrics.failures += int(failed); self.metrics.cache_hits += int(cache_hit); self.metrics.total_latency_ms += latency_ms
    def snapshot(self): return self.metrics
