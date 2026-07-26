class DatasetRegistry:
    def __init__(self): self._datasets = {}
    def add(self, name, cases): self._datasets[name] = cases
    def get(self, name): return self._datasets.get(name, [])
    def names(self): return sorted(self._datasets)
