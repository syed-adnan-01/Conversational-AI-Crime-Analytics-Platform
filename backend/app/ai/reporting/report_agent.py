from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class ReportAgent(SpecialistAgent):
    def __init__(self, report_service=None, bus=None):
        def run(request, context):
            value = report_service(request.case_id, request.query) if report_service else {}
            return {'report': value, 'case_summary': '', 'executive_summary': '', 'chargesheet_draft': '', 'investigation_report': ''}
        super().__init__('report-agent', AgentCapability.REPORTING, run, bus)
