"""
AI Event Bus for publishing and handling asynchronous/decoupled events.
"""

from typing import Callable, Dict, List
from app.ai.copilot.events.event_handlers import (
    AuditHandler,
    MetricsHandler,
    NotificationHandler,
    TraceHandler,
    WorkspaceHandler,
)
from app.ai.copilot.events.event_models import CopilotEvent, EventType

EventHandler = Callable[[CopilotEvent], None]


class CopilotEventBus:
    """Decoupled Pub/Sub Event Bus for Copilot lifecycle execution events."""

    _subscribers: Dict[EventType, List[EventHandler]] = {}
    _initialized: bool = False

    @classmethod
    def _setup_default_subscribers(cls) -> None:
        if not cls._initialized:
            cls.subscribe_all(MetricsHandler.handle)
            cls.subscribe_all(AuditHandler.handle)
            cls.subscribe_all(TraceHandler.handle)
            cls.subscribe(EventType.WORKSPACE_UPDATED, WorkspaceHandler.handle)
            cls.subscribe(EventType.ACTION_EXECUTED, NotificationHandler.handle)
            cls._initialized = True

    @classmethod
    def subscribe(cls, event_type: EventType, handler: EventHandler) -> None:
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)

    @classmethod
    def subscribe_all(cls, handler: EventHandler) -> None:
        for et in EventType:
            cls.subscribe(et, handler)

    @classmethod
    def publish(cls, event: CopilotEvent) -> None:
        cls._setup_default_subscribers()
        handlers = cls._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                pass

    @classmethod
    def clear(cls) -> None:
        cls._subscribers.clear()
        cls._initialized = False
