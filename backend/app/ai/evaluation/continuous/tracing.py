from datetime import datetime, timezone
class EvaluationTracer:
    def __init__(self): self.events = []
    def record(self, event, **details): self.events.append({'event': event, 'details': details, 'timestamp': datetime.now(timezone.utc).isoformat()})
