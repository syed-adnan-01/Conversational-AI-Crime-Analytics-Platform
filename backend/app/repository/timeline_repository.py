"""
SQLAlchemy PostgreSQL implementation of TimelineRepository.
"""

from typing import Optional
from uuid import uuid4
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.timeline import TimelineEvent
from app.database.session import SessionLocal
from app.database.orm.timeline import CaseTimelineORM
from app.database.mappers.timeline_mapper import TimelineMapper
from app.common.queries.timeline_query import TimelineQueryOptions


from app.database.db_list import DBList


class TimelineRepository:
    _events = DBList(CaseTimelineORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("TimelineRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_event(cls, event: TimelineEvent) -> TimelineEvent:
        db = SessionLocal()
        try:
            if not event.event_id:
                event = event.model_copy(update={"event_id": f"TL-{uuid4().hex[:12].upper()}"})
            orm_obj = TimelineMapper.to_orm(event)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = TimelineMapper.to_domain(orm_obj)
            app_logger.info("Timeline event appended in DB | ID=%s", res.event_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to append timeline event: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_event_by_id(cls, event_id: str) -> Optional[TimelineEvent]:
        db = SessionLocal()
        try:
            orm_obj = db.get(CaseTimelineORM, event_id)
            if not orm_obj:
                return None
            return TimelineMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_case_timeline(cls, case_master_id: str) -> list[TimelineEvent]:
        db = SessionLocal()
        try:
            stmt = select(CaseTimelineORM).where(
                CaseTimelineORM.case_master_id == case_master_id
            ).order_by(CaseTimelineORM.event_timestamp.desc())
            orm_list = db.scalars(stmt).all()
            return [TimelineMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def query_timeline(
        cls, options: TimelineQueryOptions
    ) -> tuple[list[TimelineEvent], int]:
        db = SessionLocal()
        try:
            stmt = select(CaseTimelineORM)
            if options.case_master_id:
                stmt = stmt.where(CaseTimelineORM.case_master_id == options.case_master_id)

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [TimelineMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
