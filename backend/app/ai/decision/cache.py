class DecisionCache:
    def __init__(self): self._items = {}; self.hits = 0; self.misses = 0
    def get(self, key):
        if key in self._items: self.hits += 1; return self._items[key]
        self.misses += 1; return None
    def put(self, key, value): self._items[key] = value
    def statistics(self): return {'items': len(self._items), 'hits': self.hits, 'misses': self.misses, 'hit_rate': self.hits / (self.hits + self.misses) if self.hits + self.misses else 0}
