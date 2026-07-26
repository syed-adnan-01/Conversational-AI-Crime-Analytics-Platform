from datetime import datetime, timedelta, timezone
from .models import RetentionRecord
class RetentionManager:
    def __init__(self): self.records = []
    def retain(self, resource_id, days):
        record = RetentionRecord(resource_id=resource_id, retain_until=datetime.now(timezone.utc)+timedelta(days=days)); self.records.append(record); return record
