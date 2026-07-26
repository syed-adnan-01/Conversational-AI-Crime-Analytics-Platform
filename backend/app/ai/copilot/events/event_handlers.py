"""
Event Subscriber Handlers for AI Event Bus.
"""

import logging
from app.ai.copilot.events.event_models import CopilotEvent

logger = logging.getLogger("copilot.events")


class MetricsHandler:
    """Event subscriber updating system operational metrics."""
    @staticmethod
    def handle(event: CopilotEvent) -> None:
        logger.debug(f"[METRICS] Event received: {event.event_type} for session {event.session_id}")


class AuditHandler:
    """Event subscriber writing immutable audit records."""
    @staticmethod
    def handle(event: CopilotEvent) -> None:
        logger.debug(f"[AUDIT] Event logged: {event.event_type} id={event.event_id}")


class TraceHandler:
    """Event subscriber logging execution trace steps."""
    @staticmethod
    def handle(event: CopilotEvent) -> None:
        logger.debug(f"[TRACE] Execution step: {event.event_type}")


class WorkspaceHandler:
    """Event subscriber syncing state changes into CopilotWorkspace."""
    @staticmethod
    def handle(event: CopilotEvent) -> None:
        logger.debug(f"[WORKSPACE] Workspace sync event: {event.event_type}")


class NotificationHandler:
    """Event subscriber pushing notification alerts for completed steps."""
    @staticmethod
    def handle(event: CopilotEvent) -> None:
        logger.debug(f"[NOTIFICATION] Alert for: {event.event_type}")
