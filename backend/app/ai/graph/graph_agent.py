from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class KnowledgeGraphAgent(SpecialistAgent):
    def __init__(self, graph_service=None, bus=None):
        def run(request, context):
            graph = graph_service.build(request.case_id) if graph_service else None
            data = graph.model_dump() if hasattr(graph, 'model_dump') else graph
            return {'graph': data, 'hidden_relationships': [], 'criminal_networks': [], 'shared_entities': []}
        super().__init__('graph-agent', AgentCapability.GRAPH, run, bus)
