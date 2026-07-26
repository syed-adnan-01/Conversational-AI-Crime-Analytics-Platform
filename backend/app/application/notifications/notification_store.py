from typing import List, Optional
import uuid
from datetime import datetime, timezone
from threading import Lock

class NotificationEntity:
    def __init__(self, title: str, message: str, category: str, priority: str, source: str):
        self.notification_id = str(uuid.uuid4())
        self.title = title
        self.message = message
        self.category = category
        self.priority = priority
        self.source = source
        self.created_at = datetime.now(timezone.utc)
        self.read = False

class NotificationStore:
    def __init__(self):
        self._notifications: dict[str, NotificationEntity] = {}
        self._lock = Lock()
    
    def add(self, entity: NotificationEntity) -> NotificationEntity:
        with self._lock:
            self._notifications[entity.notification_id] = entity
        return entity
    
    def get_all(self, unread_only: bool = False) -> List[NotificationEntity]:
        with self._lock:
            if unread_only:
                return [n for n in self._notifications.values() if not n.read]
            return list(self._notifications.values())
            
    def get_by_id(self, notification_id: str) -> Optional[NotificationEntity]:
        with self._lock:
            return self._notifications.get(notification_id)
            
    def mark_read(self, notification_id: str) -> bool:
        with self._lock:
            if notification_id in self._notifications:
                self._notifications[notification_id].read = True
                return True
            return False
            
    def mark_all_read(self) -> int:
        count = 0
        with self._lock:
            for n in self._notifications.values():
                if not n.read:
                    n.read = True
                    count += 1
        return count
        
    def delete(self, notification_id: str) -> bool:
        with self._lock:
            if notification_id in self._notifications:
                del self._notifications[notification_id]
                return True
            return False
            
    def count(self) -> tuple[int, int]:
        with self._lock:
            total = len(self._notifications)
            unread = sum(1 for n in self._notifications.values() if not n.read)
            return total, unread

notification_store = NotificationStore()
