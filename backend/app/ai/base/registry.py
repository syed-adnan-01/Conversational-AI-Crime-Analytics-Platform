class AgentRegistry:
    def __init__(self): self._agents = {}
    def register(self, agent): self._agents[agent.agent_id] = agent
    def get(self, agent_id): return self._agents.get(agent_id)
    def all(self): return list(self._agents.values())
    def capabilities(self): return {agent.agent_id: agent.capability.value for agent in self.all()}
