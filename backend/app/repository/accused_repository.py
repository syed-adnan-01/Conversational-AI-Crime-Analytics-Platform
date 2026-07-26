"""
SQLAlchemy PostgreSQL implementation of AccusedRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.accused import Accused
from app.database.session import SessionLocal
from app.database.orm.accused import AccusedORM
from app.database.mappers.accused_mapper import AccusedMapper
from app.common.queries.accused_query import AccusedQueryOptions


from app.database.db_list import DBList


class AccusedRepository:
    _accused = DBList(AccusedORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("AccusedRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_accused(cls, accused: Accused) -> Accused:
        db = SessionLocal()
        try:
            orm_obj = AccusedMapper.to_orm(accused)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            AccusedMapper.cache_domain(accused, db_id=orm_obj.accusedmasterid)
            res = AccusedMapper.to_domain(orm_obj)
            app_logger.info("Accused stored in DB | ID=%s", res.accused_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create accused: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_accused_by_id(cls, accused_id: str) -> Optional[Accused]:
        db = SessionLocal()
        try:
            parsed_id = AccusedMapper._parse_id(accused_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(AccusedORM, parsed_id)
            if not orm_obj:
                return None
            return AccusedMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_accused_by_case_id(cls, case_master_id: str) -> list[Accused]:
        db = SessionLocal()
        try:
            parsed_case_id = AccusedMapper._parse_case_id(case_master_id)
            stmt = select(AccusedORM).where(AccusedORM.casemasterid == parsed_case_id)
            orm_list = db.scalars(stmt).all()
            return [AccusedMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_accused(cls, accused: Accused) -> Optional[Accused]:
        db = SessionLocal()
        try:
            parsed_id = AccusedMapper._parse_id(accused.accused_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(AccusedORM, parsed_id)
            if not orm_obj:
                return None
            new_orm = AccusedMapper.to_orm(accused)
            orm_obj.accusedname = new_orm.accusedname
            orm_obj.ageyear = new_orm.ageyear
            orm_obj.genderid = new_orm.genderid
            orm_obj.personid = new_orm.personid
            db.commit()
            db.refresh(orm_obj)
            return AccusedMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update accused: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_accused(cls, accused_id: str) -> bool:
        db = SessionLocal()
        try:
            parsed_id = AccusedMapper._parse_id(accused_id)
            if parsed_id is None:
                return False
            orm_obj = db.get(AccusedORM, parsed_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete accused: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_accused(
        cls, options: AccusedQueryOptions
    ) -> tuple[list[Accused], int]:
        db = SessionLocal()
        try:
            stmt = select(AccusedORM)
            if options.case_master_id:
                parsed_case_id = AccusedMapper._parse_case_id(options.case_master_id)
                stmt = stmt.where(AccusedORM.casemasterid == parsed_case_id)
            if options.name:
                stmt = stmt.where(AccusedORM.accusedname.ilike(f"%{options.name}%"))

            if hasattr(options, "sort_by") and options.sort_by:
                sort_col = AccusedORM.accusedname
                if str(options.sort_by).lower().endswith("name"):
                    sort_col = AccusedORM.accusedname
                elif str(options.sort_by).lower().endswith("age"):
                    sort_col = AccusedORM.ageyear

                if hasattr(options, "sort_order") and str(options.sort_order).lower().endswith("desc"):
                    stmt = stmt.order_by(sort_col.desc())
                else:
                    stmt = stmt.order_by(sort_col.asc())

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [AccusedMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
