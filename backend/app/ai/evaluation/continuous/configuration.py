from pydantic import BaseModel
class EvaluationConfiguration(BaseModel): cache_enabled: bool = True; retain_feedback: bool = True
