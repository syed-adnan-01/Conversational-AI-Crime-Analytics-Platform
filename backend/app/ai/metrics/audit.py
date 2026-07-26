class AgentAudit:
    def __init__(self): self.events = []
    def record(self, action, **payload): self.events.append({"action": action, **payload})
