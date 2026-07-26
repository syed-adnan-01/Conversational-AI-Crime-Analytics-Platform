from .compliance_validator import ComplianceValidator
from .policy_evaluation import PolicyEvaluator
from .policy_registry import PolicyRegistry
class GovernanceEngine:
    def __init__(self, registry=None, evaluator=None, validator=None): self.registry = registry or PolicyRegistry(); self.evaluator = evaluator or PolicyEvaluator(); self.validator = validator or ComplianceValidator(); self.history = []
    def evaluate(self, request):
        result = self.validator.validate(self.evaluator.evaluate(request, self.registry.all())); self.history.append(result); return result
