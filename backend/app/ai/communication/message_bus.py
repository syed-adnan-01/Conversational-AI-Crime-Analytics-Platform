from collections import defaultdict
from .event_models import AgentMessage

class MessageBus:
    """In-process event bus; replaceable with an external broker without changing agents."""
    def __init__(self): self._subscribers = defaultdict(list); self.events = []
    def subscribe(self, topic, callback): self._subscribers[topic].append(callback)
    def publish(self, message: AgentMessage):
        self.events.append(message)
        for callback in self._subscribers[message.topic]: callback(message)
    def publish_response(self, response): self.publish(AgentMessage(topic="agent.response", sender=response.agent_id, payload=response.model_dump(mode="json")))
