from typing import List, Optional
from .notification_models import NotificationCreate, NotificationResponse, NotificationCountResponse, NotificationHealthResponse
from .notification_store import NotificationStore, NotificationEntity, notification_store
from .notification_mapper import NotificationMapper

class NotificationService:
    def __init__(self, store: NotificationStore = notification_store):
        self.store = store

    def create_notification(self, data: NotificationCreate) -> NotificationResponse:
        entity = NotificationEntity(
            title=data.title,
            message=data.message,
            category=data.category.value,
            priority=data.priority.value,
            source=data.source
        )
        self.store.add(entity)
        return NotificationMapper.to_response(entity)
        
    def get_notifications(self, unread_only: bool = False) -> List[NotificationResponse]:
        entities = self.store.get_all(unread_only=unread_only)
        return [NotificationMapper.to_response(e) for e in entities]
        
    def mark_read(self, notification_id: str) -> bool:
        return self.store.mark_read(notification_id)
        
    def mark_all_read(self) -> int:
        return self.store.mark_all_read()
        
    def delete_notification(self, notification_id: str) -> bool:
        return self.store.delete(notification_id)
        
    def get_count(self) -> NotificationCountResponse:
        total, unread = self.store.count()
        return NotificationCountResponse(total=total, unread=unread)
        
    def get_health(self) -> NotificationHealthResponse:
        total, _ = self.store.count()
        return NotificationHealthResponse(
            status="healthy",
            storage_status="in_memory",
            total_notifications=total
        )
