"""
Core Copilot domain models — shared across planner, engine, and service layers.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Agent State
# ---------------------------------------------------------------------------


class AgentState(str, Enum):
    IDLE = "IDLE"
    THINKING = "THINKING"
    RETRIEVING = "RETRIEVING"
    EXECUTING_ACTION = "EXECUTING_ACTION"
    GENERATING_PROMPT = "GENERATING_PROMPT"
    WAITING_FOR_LLM = "WAITING_FOR_LLM"
    BUILDING_RESPONSE = "BUILDING_RESPONSE"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# Execution Plan
# ---------------------------------------------------------------------------


class ExecutionStep(BaseModel):
    step_name: str
    action_type: str  # RETRIEVE | GENERATE | WORKFLOW | MEMORY | ACTION
    description: str
    completed: bool = False
    result: Optional[str] = None


class ExecutionPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"PLAN-{uuid.uuid4().hex[:8].upper()}")
    selected_strategy: str
    confidence: float = 0.0
    reason: str
    steps: List[ExecutionStep] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Reasoning Trace
# ---------------------------------------------------------------------------


class TraceStep(BaseModel):
    step: str
    detail: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ReasoningTrace(BaseModel):
    session_id: str
    turn_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    steps: List[TraceStep] = Field(default_factory=list)

    def add(self, step: str, detail: str = "") -> None:
        self.steps.append(TraceStep(step=step, detail=detail))

    def to_log(self) -> List[str]:
        return [f"[{s.timestamp.isoformat()}] {s.step}: {s.detail}" for s in self.steps]


# ---------------------------------------------------------------------------
# Conversation Message
# ---------------------------------------------------------------------------


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Conversation Turn (Copilot I/O)
# ---------------------------------------------------------------------------


class CopilotRequest(BaseModel):
    session_id: str
    case_id: str
    user_message: str
    persona: str = "investigator"
    stream: bool = False
    context: Dict[str, Any] = Field(default_factory=dict)


class CopilotResponse(BaseModel):
    session_id: str
    case_id: str
    answer: str
    plan: Optional[ExecutionPlan] = None
    reasoning_trace: Optional[List[str]] = None
    agent_state: AgentState = AgentState.COMPLETE
    confidence: float = 0.0
    provider_used: Optional[str] = None
    latency_ms: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Conversation Timeline Event
# ---------------------------------------------------------------------------


class TimelineEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    event_type: str
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Task Queue
# ---------------------------------------------------------------------------


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"


class CopilotTask(BaseModel):
    task_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    task_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------


class FeedbackRating(str, Enum):
    THUMBS_UP = "THUMBS_UP"
    THUMBS_DOWN = "THUMBS_DOWN"
    NEUTRAL = "NEUTRAL"


class CopilotFeedback(BaseModel):
    feedback_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    session_id: str
    turn_id: str
    rating: FeedbackRating
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Context Window
# ---------------------------------------------------------------------------


class ContextWindow(BaseModel):
    session_id: str
    messages: List[ConversationMessage] = Field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 32768

    def fits(self, tokens: int) -> bool:
        return (self.total_tokens + tokens) <= self.max_tokens
