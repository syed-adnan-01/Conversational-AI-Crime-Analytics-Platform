from pydantic import BaseModel
class DecisionConfiguration(BaseModel): cache_enabled: bool = True; minimum_confidence: float = 0.0
