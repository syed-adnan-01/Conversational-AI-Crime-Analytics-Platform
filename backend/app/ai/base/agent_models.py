from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

class TaskStatus(str, Enum): PENDING="pending"; RUNNING="running"; COMPLETED="completed"; FAILED="failed"; CANCELLED="cancelled"
class AgentCapability(str, Enum): EVIDENCE="evidence"; TIMELINE="timeline"; LEGAL="legal"; SEARCH="search"; GRAPH="graph"; PREDICTION="prediction"; REPORTING="reporting"; ANALYTICS="analytics"
class AgentRequest(BaseModel):
    case_id: str; query: str | None = None; capabilities: list[AgentCapability] = Field(default_factory=list); context: dict[str, Any] = Field(default_factory=dict); request_id: str = Field(default_factory=lambda: f"agent-request-{uuid4().hex}")
class AgentResponse(BaseModel):
    agent_id: str; task_id: str; status: TaskStatus = TaskStatus.COMPLETED; result: dict[str, Any] = Field(default_factory=dict); summary: str = ""; citations: list[str] = Field(default_factory=list); error: str | None = None; duration_ms: float = 0
class AgentTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task-{uuid4().hex}"); agent_id: str; capability: AgentCapability; request: AgentRequest; depends_on: list[str] = Field(default_factory=list); timeout_seconds: float = 30; retries: int = 0; status: TaskStatus = TaskStatus.PENDING
class ExecutionStep(BaseModel): task: AgentTask; order: int; parallel_group: int = 0; condition: str | None = None
class ExecutionPlan(BaseModel): plan_id: str = Field(default_factory=lambda: f"plan-{uuid4().hex}"); request_id: str; steps: list[ExecutionStep] = Field(default_factory=list); rationale: str = ""
class AgentMetrics(BaseModel): executions: int = 0; successes: int = 0; failures: int = 0; total_duration_ms: float = 0
class AgentTrace(BaseModel): agent_id: str; event: str; timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)); details: dict[str, Any] = Field(default_factory=dict)
class AgentHealth(BaseModel): agent_id: str; healthy: bool; details: dict[str, Any] = Field(default_factory=dict)
