class DecisionAudit:
    def __init__(self): self.entries = []
    def record(self, decision_id, action, **details): self.entries.append({'decision_id': decision_id, 'action': action, **details})
