from app.ai.communication.message_bus import MessageBus
from app.ai.memory.blackboard import Blackboard
from app.ai.metrics.metrics import AgentMetricsStore
from .execution_context import ExecutionContext
from .planner import Planner
from .scheduler import Scheduler

class AgentCoordinator:
    """Single collaboration boundary: plans, dispatches, and collects all agent work."""
    def __init__(self, registry, planner=None, scheduler=None, bus=None, metrics=None):
        self.registry = registry; self.planner = planner or Planner(); self.scheduler = scheduler or Scheduler(); self.bus = bus or MessageBus(); self.metrics = metrics or AgentMetricsStore()
    def execute(self, request):
        context = ExecutionContext(blackboard=Blackboard(), bus=self.bus); context.blackboard.write("request", request.model_dump())
        plan = self.planner.plan(request, self.registry.capabilities())
        self.bus.publish(__import__('app.ai.communication.event_models', fromlist=['AgentMessage']).AgentMessage(topic="plan.created", sender="coordinator", payload=plan.model_dump(mode="json")))
        results = self.scheduler.execute(plan, self.registry, context)
        for result in results: context.blackboard.write(f"response:{result.agent_id}", result.model_dump())
        self.metrics.record(results)
        return plan, results, context
