from app.ai.base.agent_models import AgentMetrics
class AgentMetricsStore:
    def __init__(self): self.metrics = AgentMetrics()
    def record(self, results):
        self.metrics.executions += len(results); self.metrics.successes += sum(result.error is None for result in results); self.metrics.failures += sum(result.error is not None for result in results); self.metrics.total_duration_ms += sum(result.duration_ms for result in results)
    def snapshot(self): return self.metrics
