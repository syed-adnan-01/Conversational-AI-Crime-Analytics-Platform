from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class EvidenceAgent(SpecialistAgent):
    def __init__(self, investigation_service=None, retrieval_service=None, graph_service=None, bus=None):
        def run(request, context):
            if investigation_service:
                from app.ai.investigation.intelligence.investigation_models import InvestigationRequest
                value = investigation_service.evidence(InvestigationRequest(case_id=request.case_id, query=request.query))
                return {"evidence_assessment": value.model_dump() if hasattr(value, 'model_dump') else value}
            return {"evidence_assessment": [], "evidence_gaps": [], "weak_evidence": [], "strong_evidence": []}
        super().__init__('evidence-agent', AgentCapability.EVIDENCE, run, bus)
