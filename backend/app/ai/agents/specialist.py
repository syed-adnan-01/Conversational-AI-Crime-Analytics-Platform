from app.ai.base.agent import BaseAgent

class SpecialistAgent(BaseAgent):
    """Adapter around an injected legacy service callable. No specialist knows another agent."""
    def __init__(self, agent_id, capability, runner=None, bus=None): super().__init__(agent_id, capability, bus); self.runner = runner
    def _execute(self, task, context):
        if self.runner: return self.runner(task.request, context)
        return {"case_id": task.request.case_id, "query": task.request.query, "status": "No provider configured; no unsupported inference was generated."}
