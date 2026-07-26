from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class AnalyticsAgent(SpecialistAgent):
    def __init__(self, analytics_service=None, bus=None):
        def run(request, context):
            value = analytics_service(request.case_id) if analytics_service else {}
            return {'analytics': value, 'crime_statistics': {}, 'district_analytics': {}, 'officer_analytics': {}, 'resource_insights': []}
        super().__init__('analytics-agent', AgentCapability.ANALYTICS, run, bus)
