from app.ai.agents.specialist import SpecialistAgent
from app.ai.base.agent_models import AgentCapability
class PredictionAgent(SpecialistAgent):
    def __init__(self, prediction_service=None, bus=None):
        def run(request, context):
            value = prediction_service(request.case_id, request.query) if prediction_service else {}
            return {'predictions': value, 'risk_score': None, 'conviction_probability': None, 'delay_prediction': None, 'offender_prediction': None}
        super().__init__('prediction-agent', AgentCapability.PREDICTION, run, bus)
