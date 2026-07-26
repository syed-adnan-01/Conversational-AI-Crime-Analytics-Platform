from .notification_models import NotificationResponse
from .notification_store import NotificationEntity

class NotificationMapper:
    @staticmethod
    def to_response(entity: NotificationEntity) -> NotificationResponse:
        return NotificationResponse(
            notification_id=entity.notification_id,
            title=entity.title,
            message=entity.message,
            category=entity.category,
            priority=entity.priority,
            source=entity.source,
            created_at=entity.created_at,
            read=entity.read
        )
