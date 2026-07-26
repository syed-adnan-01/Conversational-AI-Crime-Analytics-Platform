from .models import PolicyDecision
class PolicyEngine:
    def __init__(self, config): self.config = config
    def evaluate(self, request):
        terms = [term for term in self.config.blocked_terms if term.casefold() in request.text.casefold()]
        return PolicyDecision(allowed=not terms, reasons=[f'Blocked policy term: {term}' for term in terms])
