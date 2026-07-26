class PolicyRegistry:
    def __init__(self): self._policies = {}
    def register(self, policy): self._policies[policy.policy_id] = policy
    def all(self): return list(self._policies.values())
