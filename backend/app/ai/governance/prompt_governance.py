class PromptGovernance:
    def validate(self, request, policies, evaluator): return evaluator.evaluate(request, policies)
