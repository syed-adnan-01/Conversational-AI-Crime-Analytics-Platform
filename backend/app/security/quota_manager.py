from collections import defaultdict
class QuotaManager:
    def __init__(self): self._limits = {}; self._usage = defaultdict(int)
    def set_limit(self, key, limit): self._limits[key] = limit
    def consume(self, key):
        if key in self._limits and self._usage[key] >= self._limits[key]: return False
        self._usage[key] += 1; return True
    def status(self, key): return {'used': self._usage[key], 'limit': self._limits.get(key)}
