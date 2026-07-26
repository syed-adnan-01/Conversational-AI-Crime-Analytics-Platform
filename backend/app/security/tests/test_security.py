from app.security.configuration import SecurityConfiguration
from app.security.models import DataClassification, MaskingLevel, SecurityRequest
from app.security.rate_limiter import RateLimiter
from app.security.security_service import SecurityService
from app.ai.governance.governance_service import GovernanceService
from app.ai.governance.models import GovernancePolicy, GovernanceRequest
def test_pii_policy_permission_and_immutable_audit():
    service = SecurityService(config=SecurityConfiguration(masking_level=MaskingLevel.FULL, blocked_terms=['exfiltrate']))
    approved = service.inspect(SecurityRequest(user_id='u1', role='officer', endpoint='/ai', text='Contact a@b.com at 9876543210'))
    denied = service.inspect(SecurityRequest(user_id='u1', role='officer', endpoint='/ai', text='exfiltrate evidence', classification=DataClassification.RESTRICTED))
    assert approved.allowed and '[REDACTED]' in approved.masked_text and not denied.allowed
    assert service.audit.entries[1].previous_hash == service.audit.entries[0].entry_hash
def test_rate_limit_and_governance_policy():
    limiter = RateLimiter(limit=1); assert limiter.allow('user') and not limiter.allow('user')
    governance = GovernanceService(); governance.add_policy(GovernancePolicy(policy_id='victim', name='Victim privacy', blocked_terms=['victim address'], allowed_roles=['supervisor']))
    result = governance.evaluate(GovernanceRequest(user_id='u1', role='officer', prompt='show victim address'))
    assert not result.compliant and result.decisions
