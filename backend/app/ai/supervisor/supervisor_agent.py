from .strategy import SynthesisStrategy
class SupervisorAgent:
    """Owns plan/result synthesis but delegates dispatch to AgentCoordinator."""
    def __init__(self, coordinator, strategy=None): self.coordinator = coordinator; self.strategy = strategy or SynthesisStrategy()
    def investigate(self, request):
        plan, results, context = self.coordinator.execute(request)
        return {"plan": plan, "responses": results, "result": self.strategy.synthesize(results), "blackboard": context.blackboard.snapshot()}
