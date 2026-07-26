class EvaluationRegistry:
    def __init__(self): self._evaluators = {}
    def register(self, module, evaluator): self._evaluators[module] = evaluator
    def get(self, module): return self._evaluators.get(module)
    def modules(self): return sorted(self._evaluators)
