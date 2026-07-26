class ModelGovernance:
    def validate(self, request, allowed_models=()): return not allowed_models or request.model in allowed_models
