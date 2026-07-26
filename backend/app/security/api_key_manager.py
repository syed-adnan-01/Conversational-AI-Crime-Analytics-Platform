from hashlib import sha256
import secrets
class APIKeyManager:
    def __init__(self): self._keys = {}
    def create(self, owner, scopes=()):
        raw = secrets.token_urlsafe(24); self._keys[sha256(raw.encode()).hexdigest()] = {'owner': owner, 'scopes': list(scopes), 'active': True}; return raw
    def validate(self, key, scope=None):
        record = self._keys.get(sha256(key.encode()).hexdigest()); return bool(record and record['active'] and (scope is None or scope in record['scopes']))
