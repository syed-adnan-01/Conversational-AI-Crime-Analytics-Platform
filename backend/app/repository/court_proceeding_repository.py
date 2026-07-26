"""
SQLAlchemy PostgreSQL implementation of CourtProceedingRepository.
"""

from typing import Optional
from uuid import uuid4
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.court_proceeding import CourtProceeding
from app.database.session import SessionLocal
from app.database.orm.court_proceeding import CourtProceedingORM
from app.database.mappers.court_proceeding_mapper import CourtProceedingMapper
from app.common.queries.court_proceeding_query import CourtProceedingQueryOptions


from app.database.db_list import DBList


class CourtProceedingRepository:
    _proceedings = DBList(CourtProceedingORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("CourtProceedingRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_proceeding(cls, proceeding: CourtProceeding) -> CourtProceeding:
        db = SessionLocal()
        try:
            if not proceeding.proceeding_id:
                proceeding = proceeding.model_copy(update={"proceeding_id": f"CP-{uuid4().hex[:12].upper()}"})
            orm_obj = CourtProceedingMapper.to_orm(proceeding)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = CourtProceedingMapper.to_domain(orm_obj)
            app_logger.info("Court proceeding stored in DB | ID=%s", res.proceeding_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create court proceeding: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_proceeding_by_id(cls, proceeding_id: str) -> Optional[CourtProceeding]:
        db = SessionLocal()
        try:
            orm_obj = db.get(CourtProceedingORM, proceeding_id)
            if not orm_obj:
                return None
            return CourtProceedingMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_proceedings_by_case_id(cls, case_master_id: str) -> list[CourtProceeding]:
        db = SessionLocal()
        try:
            stmt = select(CourtProceedingORM).where(CourtProceedingORM.case_master_id == case_master_id)
            orm_list = db.scalars(stmt).all()
            return [CourtProceedingMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_proceeding(cls, proceeding: CourtProceeding) -> Optional[CourtProceeding]:
        db = SessionLocal()
        try:
            if not proceeding.proceeding_id:
                return None
            orm_obj = db.get(CourtProceedingORM, proceeding.proceeding_id)
            if not orm_obj:
                return None
            new_orm = CourtProceedingMapper.to_orm(proceeding)
            orm_obj.stage = new_orm.stage
            orm_obj.summary = new_orm.summary
            orm_obj.judge_name = new_orm.judge_name
            db.commit()
            db.refresh(orm_obj)
            return CourtProceedingMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update court proceeding: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_proceeding(cls, proceeding_id: str) -> bool:
        db = SessionLocal()
        try:
            orm_obj = db.get(CourtProceedingORM, proceeding_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete court proceeding: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_proceedings(
        cls, options: CourtProceedingQueryOptions
    ) -> tuple[list[CourtProceeding], int]:
        db = SessionLocal()
        try:
            stmt = select(CourtProceedingORM)
            if options.case_master_id:
                stmt = stmt.where(CourtProceedingORM.case_master_id == options.case_master_id)

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [CourtProceedingMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
