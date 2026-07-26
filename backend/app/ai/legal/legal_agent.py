from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class LegalAgent(SpecialistAgent):
    def __init__(self, investigation_service=None, bus=None):
        def run(request, context):
            if investigation_service:
                from app.ai.investigation.intelligence.investigation_models import InvestigationRequest
                value = investigation_service.legal(InvestigationRequest(case_id=request.case_id, query=request.query)); return {'legal_analysis': value.model_dump() if hasattr(value, 'model_dump') else value}
            return {'applicable_acts': [], 'sections': [], 'legal_risks': [], 'missing_documents': []}
        super().__init__('legal-agent', AgentCapability.LEGAL, run, bus)
