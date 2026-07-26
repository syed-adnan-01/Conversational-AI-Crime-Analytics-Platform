class Blackboard:
    """Coordinator-owned shared context; agents use it only through ExecutionContext."""
    def __init__(self): self._values = {}
    def write(self, key, value): self._values[key] = value
    def read(self, key, default=None): return self._values.get(key, default)
    def snapshot(self): return dict(self._values)
