from hashlib import sha256
from .audit_logger import ImmutableAuditLogger
from .configuration import SecurityConfiguration
from .models import PolicyDecision
from .permission_evaluator import PermissionEvaluator
from .pii_detector import PIIDetector
from .policy_engine import PolicyEngine
from .rate_limiter import RateLimiter
from .redaction_engine import RedactionEngine
from .security_metrics import SecurityMetricsTracker
from .security_tracing import SecurityTracer
class SecurityService:
    def __init__(self, config=None, policy=None, permissions=None, pii=None, redaction=None, rate_limiter=None, audit=None, metrics=None, tracer=None):
        self.config = config or SecurityConfiguration(); self.policy = policy or PolicyEngine(self.config); self.permissions = permissions or PermissionEvaluator(); self.pii = pii or PIIDetector(); self.redaction = redaction or RedactionEngine(); self.rate_limiter = rate_limiter or RateLimiter(self.config.user_limit); self.audit = audit or ImmutableAuditLogger(); self.metrics = metrics or SecurityMetricsTracker(); self.tracer = tracer or SecurityTracer()
    def inspect(self, request):
        self.metrics.value.requests += 1
        if not self.rate_limiter.allow(f'user:{request.user_id}'):
            self.metrics.value.rate_limited += 1; return PolicyDecision(allowed=False, reasons=['Rate limit exceeded'])
        decision = self.policy.evaluate(request)
        if not self.permissions.evaluate(request): decision.allowed = False; decision.reasons.append('Role is not permitted for this data classification')
        findings = self.pii.detect(request.text); self.metrics.value.pii_detections += len(findings); decision.masked_text = self.redaction.redact(request.text, findings, self.config.masking_level)
        if not decision.allowed: self.metrics.value.denied += 1
        self.audit.record(user_id=request.user_id, role=request.role, endpoint=request.endpoint, provider=request.provider, prompt_hash=sha256(request.text.encode()).hexdigest(), policy_decisions=decision.reasons); self.tracer.record('request_inspected', allowed=decision.allowed); return decision
    def health(self): return {'status': 'healthy', 'audit_entries': len(self.audit.entries)}
