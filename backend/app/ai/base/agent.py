from __future__ import annotations
from abc import ABC, abstractmethod
from time import perf_counter
from .agent_models import AgentHealth, AgentMetrics, AgentRequest, AgentResponse, AgentTask, TaskStatus

class BaseAgent(ABC):
    """Specialist contract. Agents never invoke other agents directly."""
    def __init__(self, agent_id: str, capability, bus=None): self.agent_id = agent_id; self.capability = capability; self.bus = bus; self.metrics = AgentMetrics()
    def initialize(self): return None
    @abstractmethod
    def _execute(self, task: AgentTask, context) -> dict: ...
    def execute(self, task: AgentTask, context) -> AgentResponse:
        started = perf_counter(); self.metrics.executions += 1
        try:
            if not self.validate(task): raise ValueError("Task capability is not supported by this agent")
            result = self._execute(task, context); response = AgentResponse(agent_id=self.agent_id, task_id=task.task_id, result=result, summary=self.summarize(result), duration_ms=(perf_counter()-started)*1000)
            self.metrics.successes += 1
        except Exception as exc:
            self.metrics.failures += 1; response = AgentResponse(agent_id=self.agent_id, task_id=task.task_id, status=TaskStatus.FAILED, error=str(exc), summary=f"{self.agent_id} failed", duration_ms=(perf_counter()-started)*1000)
        self.metrics.total_duration_ms += response.duration_ms
        if self.bus: self.bus.publish_response(response)
        return response
    def validate(self, task): return task.capability == self.capability
    def summarize(self, result): return f"{self.capability.value} analysis completed"
    def health(self): return AgentHealth(agent_id=self.agent_id, healthy=True, details=self.metrics.model_dump())
