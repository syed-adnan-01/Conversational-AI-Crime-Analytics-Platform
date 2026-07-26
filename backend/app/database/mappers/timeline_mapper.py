"""
Mapper between TimelineEvent domain model and CaseTimelineORM.
"""

from datetime import datetime
from typing import Dict, Any
from app.models.timeline import TimelineEvent, TimelineEventType
from app.database.orm.timeline import CaseTimelineORM

_TIMELINE_CACHE: Dict[str, Dict[str, Any]] = {}


class TimelineMapper:
    @classmethod
    def cache_domain(cls, domain: TimelineEvent):
        if not domain:
            return
        data = {
            "title": domain.title,
            "event_type": domain.event_type,
        }
        if domain.event_id:
            _TIMELINE_CACHE[domain.event_id] = data

    @classmethod
    def to_domain(cls, orm: CaseTimelineORM) -> TimelineEvent:
        cached = _TIMELINE_CACHE.get(orm.timeline_id) or {}

        event_type = cached.get("event_type")
        if not event_type:
            event_type = TimelineEventType.CASE_CREATED
            try:
                event_type = TimelineEventType(orm.event_name)
            except ValueError:
                pass

        title = cached.get("title") or orm.event_name
        now = datetime.now()

        return TimelineEvent(
            event_id=orm.timeline_id,
            case_master_id=orm.case_master_id,
            event_type=event_type,
            title=title,
            description=orm.description or "",
            event_time=orm.event_timestamp or now,
            created_by=orm.actor_id,
            created_at=now,
        )

    @classmethod
    def to_orm(cls, domain: TimelineEvent) -> CaseTimelineORM:
        cls.cache_domain(domain)
        return CaseTimelineORM(
            timeline_id=domain.event_id or "",
            case_master_id=domain.case_master_id,
            event_name=domain.event_type.value if hasattr(domain.event_type, "value") else str(domain.event_type),
            event_timestamp=domain.event_time,
            description=domain.description,
            actor_id=domain.created_by,
        )
