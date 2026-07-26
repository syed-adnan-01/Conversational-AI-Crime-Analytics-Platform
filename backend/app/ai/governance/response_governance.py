class ResponseGovernance:
    def validate(self, request, policies, evaluator): return evaluator.evaluate(request, policies)
