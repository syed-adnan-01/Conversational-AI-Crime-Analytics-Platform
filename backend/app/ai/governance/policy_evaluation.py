from .models import ComplianceResult
class PolicyEvaluator:
    def evaluate(self, request, policies):
        decisions = []; approval = False
        for policy in policies:
            if not policy.enabled: continue
            if policy.allowed_roles and request.role not in policy.allowed_roles: decisions.append(f'{policy.name}: role is not allowed')
            if policy.classifications and request.classification not in policy.classifications: decisions.append(f'{policy.name}: data classification is not allowed')
            if any(term.casefold() in request.prompt.casefold() for term in policy.blocked_terms): decisions.append(f'{policy.name}: prompt contains blocked term')
            approval = approval or policy.require_approval
        return ComplianceResult(compliant=not decisions, decisions=decisions, approval_required=approval)
