class EvaluationCache:
    def __init__(self): self._items = {}; self.hits = 0; self.misses = 0
    def get(self, key):
        if key in self._items: self.hits += 1; return self._items[key]
        self.misses += 1; return None
    def put(self, key, value): self._items[key] = value
    def stats(self): return {'hits': self.hits, 'misses': self.misses, 'size': len(self._items)}
