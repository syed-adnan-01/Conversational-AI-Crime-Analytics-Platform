class GraphCache:
    def __init__(self): self._values = {}; self.hits = 0; self.misses = 0
    def get(self, key):
        if key in self._values: self.hits += 1; return self._values[key]
        self.misses += 1; return None
    def put(self, key, value): self._values[key] = value
    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
