"""
Copilot Events Package.
"""

from app.ai.copilot.events.event_bus import CopilotEventBus
from app.ai.copilot.events.event_handlers import (
    AuditHandler,
    MetricsHandler,
    NotificationHandler,
    TraceHandler,
    WorkspaceHandler,
)
from app.ai.copilot.events.event_models import CopilotEvent, EventType

__all__ = [
    "CopilotEventBus",
    "CopilotEvent",
    "EventType",
    "MetricsHandler",
    "AuditHandler",
    "TraceHandler",
    "WorkspaceHandler",
    "NotificationHandler",
]
