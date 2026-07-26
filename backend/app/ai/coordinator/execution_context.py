from dataclasses import dataclass
from app.ai.memory.blackboard import Blackboard
from app.ai.communication.message_bus import MessageBus
@dataclass
class ExecutionContext:
    blackboard: Blackboard
    bus: MessageBus
    cancelled: bool = False
    def cancel(self): self.cancelled = True
