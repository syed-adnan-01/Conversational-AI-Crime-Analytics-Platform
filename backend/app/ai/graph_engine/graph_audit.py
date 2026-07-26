class GraphAudit:
    def __init__(self): self.events: list[dict] = []
    def record(self, operation: str, **details): self.events.append({"operation": operation, **details})
