from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability, AgentRequest, AgentTask
from app.ai.base.registry import AgentRegistry
from app.ai.communication.message_bus import MessageBus
from app.ai.coordinator.coordinator import AgentCoordinator
from app.ai.supervisor.supervisor_agent import SupervisorAgent
from app.ai.orchestration.workflow_engine import WorkflowEngine
from app.ai.orchestration.workflow_models import Workflow

class MockAgent(SpecialistAgent):
    def __init__(self, capability, bus=None): super().__init__(f'{capability.value}-agent', capability, lambda request, context: {'case_id': request.case_id}, bus)

def configured():
    bus = MessageBus(); registry = AgentRegistry()
    for capability in (AgentCapability.EVIDENCE, AgentCapability.TIMELINE): registry.register(MockAgent(capability, bus))
    return bus, registry, AgentCoordinator(registry, bus=bus)

def test_registry_and_message_bus():
    bus, registry, coordinator = configured(); seen = []; bus.subscribe('agent.response', seen.append)
    agent = registry.get('evidence-agent'); response = agent.execute(AgentTask(agent_id=agent.agent_id, capability=AgentCapability.EVIDENCE, request=AgentRequest(case_id='C1')), None)
    assert response.error is None and len(seen) == 1

def test_supervisor_parallel_execution_and_shared_blackboard():
    bus, registry, coordinator = configured()
    result = SupervisorAgent(coordinator).investigate(AgentRequest(case_id='C1', capabilities=[AgentCapability.EVIDENCE, AgentCapability.TIMELINE]))
    assert len(result['responses']) == 2
    assert 'response:evidence-agent' in result['blackboard']
    assert coordinator.metrics.snapshot().successes == 2

def test_workflow_execution():
    bus, registry, coordinator = configured(); engine = WorkflowEngine(coordinator)
    result = engine.execute(Workflow(name='review', request=AgentRequest(case_id='C1', capabilities=[AgentCapability.EVIDENCE])))
    assert len(result.responses) == 1 and engine.registry.all()
