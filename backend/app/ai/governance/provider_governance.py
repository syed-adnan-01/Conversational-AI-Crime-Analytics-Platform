class ProviderGovernance:
    def validate(self, request, allowed_providers=()): return not allowed_providers or request.provider in allowed_providers
