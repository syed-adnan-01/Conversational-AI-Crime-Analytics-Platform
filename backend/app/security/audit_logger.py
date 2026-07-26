from hashlib import sha256
from .models import AuditEntry
class ImmutableAuditLogger:
    """Append-only hash-chained audit entries. A durable store may be injected later."""
    def __init__(self): self.entries = []
    def record(self, **kwargs):
        previous = self.entries[-1].entry_hash if self.entries else ''
        entry = AuditEntry(previous_hash=previous, **kwargs); payload = entry.model_dump(mode='json'); payload['entry_hash'] = ''; entry.entry_hash = sha256((previous + repr(sorted(payload.items()))).encode()).hexdigest(); self.entries.append(entry); return entry
