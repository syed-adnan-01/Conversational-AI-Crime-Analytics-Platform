from app.ai.base.agent_models import AgentTrace
class AgentTracer:
    def __init__(self): self.events = []
    def record(self, agent_id, event, **details): self.events.append(AgentTrace(agent_id=agent_id, event=event, details=details))
