from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class TimelineAgent(SpecialistAgent):
    def __init__(self, investigation_service=None, bus=None):
        def run(request, context):
            if investigation_service:
                from app.ai.investigation.intelligence.investigation_models import InvestigationRequest
                value = investigation_service.timeline(InvestigationRequest(case_id=request.case_id, query=request.query)); return {'timeline_verification': value.model_dump() if hasattr(value, 'model_dump') else value}
            return {'timeline_verification': [], 'gap_analysis': [], 'contradictions': [], 'sequence_validation': []}
        super().__init__('timeline-agent', AgentCapability.TIMELINE, run, bus)
