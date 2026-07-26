class EvaluationAudit:
    def __init__(self): self.entries = []
    def record(self, action, **details): self.entries.append({'action': action, **details})
