from .decision_models import DecisionTrace
class DecisionTracer:
    def __init__(self): self.traces = []
    def record(self, decision_id, event, **details): self.traces.append(DecisionTrace(decision_id=decision_id, event=event, details=details))
