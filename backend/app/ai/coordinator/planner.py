from app.ai.base.agent_models import ExecutionPlan, ExecutionStep
from app.ai.base.capabilities import CAPABILITY_AGENT_IDS
class Planner:
    def plan(self, request, capabilities):
        available_agent_ids = set(capabilities)
        selected = request.capabilities or [capability for capability in CAPABILITY_AGENT_IDS if CAPABILITY_AGENT_IDS[capability] in available_agent_ids]
        tasks = []
        for order, capability in enumerate(selected):
            agent_id = CAPABILITY_AGENT_IDS[capability]
            if agent_id in available_agent_ids: tasks.append(ExecutionStep(task=__import__('app.ai.base.agent_models', fromlist=['AgentTask']).AgentTask(agent_id=agent_id, capability=capability, request=request), order=order, parallel_group=1))
        return ExecutionPlan(request_id=request.request_id, steps=tasks, rationale="Specialists were selected by requested capabilities and registry availability.")
