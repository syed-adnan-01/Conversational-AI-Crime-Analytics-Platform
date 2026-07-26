from .compliance_reports import ComplianceReports
from .governance_engine import GovernanceEngine
class GovernanceService:
    def __init__(self, engine=None, reports=None): self.engine = engine or GovernanceEngine(); self.reports = reports or ComplianceReports()
    def evaluate(self, request): return self.engine.evaluate(request)
    def policies(self): return self.engine.registry.all()
    def add_policy(self, policy): self.engine.registry.register(policy)
    def report(self): return self.reports.build(self.engine.history)
    def health(self): return {'status': 'healthy', 'policy_count': len(self.policies())}
