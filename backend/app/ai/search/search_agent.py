from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class SearchAgent(SpecialistAgent):
    def __init__(self, search_service=None, bus=None):
        def run(request, context):
            value = search_service(request.case_id, request.query) if search_service else []
            return {'relevant_documents': value, 'similar_cases': [], 'historical_matches': []}
        super().__init__('search-agent', AgentCapability.SEARCH, run, bus)
