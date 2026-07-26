class SecurityTracer:
    def __init__(self): self.events = []
    def record(self, event, **details): self.events.append({'event': event, **details})
