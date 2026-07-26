"""
SQLAlchemy PostgreSQL implementation of ArrestRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.arrest import Arrest
from app.database.session import SessionLocal
from app.database.orm.arrest import ArrestSurrenderORM
from app.database.mappers.arrest_mapper import ArrestMapper
from app.common.queries.arrest_query import ArrestQueryOptions


from app.database.db_list import DBList


class ArrestRepository:
    _arrests = DBList(ArrestSurrenderORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("ArrestRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_arrest(cls, arrest: Arrest) -> Arrest:
        db = SessionLocal()
        try:
            orm_obj = ArrestMapper.to_orm(arrest)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            ArrestMapper.cache_domain(arrest, db_id=orm_obj.arrestsurrenderid)
            res = ArrestMapper.to_domain(orm_obj)
            app_logger.info("Arrest stored in DB | ID=%s", res.arrest_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create arrest: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_arrest_by_id(cls, arrest_id: str) -> Optional[Arrest]:
        db = SessionLocal()
        try:
            parsed_id = ArrestMapper._parse_id(arrest_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(ArrestSurrenderORM, parsed_id)
            if not orm_obj:
                return None
            return ArrestMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_arrests_by_case_id(cls, case_master_id: str) -> list[Arrest]:
        db = SessionLocal()
        try:
            parsed_case_id = ArrestMapper._parse_case_id(case_master_id)
            stmt = select(ArrestSurrenderORM).where(ArrestSurrenderORM.casemasterid == parsed_case_id)
            orm_list = db.scalars(stmt).all()
            return [ArrestMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def get_arrests_by_accused_id(cls, accused_id: str) -> list[Arrest]:
        db = SessionLocal()
        try:
            parsed_accused_id = ArrestMapper._parse_accused_id(accused_id)
            stmt = select(ArrestSurrenderORM).where(ArrestSurrenderORM.accusedmasterid == parsed_accused_id)
            orm_list = db.scalars(stmt).all()
            return [ArrestMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_arrest(cls, arrest: Arrest) -> Optional[Arrest]:
        db = SessionLocal()
        try:
            parsed_id = ArrestMapper._parse_id(arrest.arrest_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(ArrestSurrenderORM, parsed_id)
            if not orm_obj:
                return None
            new_orm = ArrestMapper.to_orm(arrest)
            orm_obj.arrestsurrenderdate = new_orm.arrestsurrenderdate
            db.commit()
            db.refresh(orm_obj)
            ArrestMapper.cache_domain(arrest, db_id=orm_obj.arrestsurrenderid)
            return ArrestMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update arrest: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_arrest(cls, arrest_id: str) -> bool:
        db = SessionLocal()
        try:
            parsed_id = ArrestMapper._parse_id(arrest_id)
            if parsed_id is None:
                return False
            orm_obj = db.get(ArrestSurrenderORM, parsed_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete arrest: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_arrests(
        cls, options: ArrestQueryOptions
    ) -> tuple[list[Arrest], int]:
        db = SessionLocal()
        try:
            stmt = select(ArrestSurrenderORM)
            if options.case_master_id:
                parsed_case_id = ArrestMapper._parse_case_id(options.case_master_id)
                stmt = stmt.where(ArrestSurrenderORM.casemasterid == parsed_case_id)
            if options.accused_id:
                parsed_accused_id = ArrestMapper._parse_accused_id(options.accused_id)
                stmt = stmt.where(ArrestSurrenderORM.accusedmasterid == parsed_accused_id)

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [ArrestMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
