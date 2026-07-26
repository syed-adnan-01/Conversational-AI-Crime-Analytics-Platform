from .decision_models import DecisionMetrics
class MetricsTracker:
    def __init__(self): self.metrics = DecisionMetrics()
    def record(self, duration, cached=False, failed=False):
        self.metrics.analyses += 1; self.metrics.cache_hits += int(cached); self.metrics.failures += int(failed); self.metrics.last_duration_ms = duration
