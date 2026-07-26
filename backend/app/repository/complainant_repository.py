"""
SQLAlchemy PostgreSQL implementation of ComplainantRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import complainant_logger
from app.models.complainant import Complainant
from app.database.session import SessionLocal
from app.database.orm.complainant import ComplainantDetailsORM
from app.database.mappers.complainant_mapper import ComplainantMapper
from app.common.queries.complainant_query import ComplainantQueryOptions


from app.database.db_list import DBList


class ComplainantRepository:
    _complainants = DBList(ComplainantDetailsORM)
    @classmethod
    def initialize(cls) -> None:
        complainant_logger.info("ComplainantRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_complainant(cls, complainant: Complainant) -> Complainant:
        db = SessionLocal()
        try:
            orm_obj = ComplainantMapper.to_orm(complainant)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            ComplainantMapper.cache_domain(complainant, db_id=orm_obj.complainantid)
            res = ComplainantMapper.to_domain(orm_obj)
            complainant_logger.info("Complainant stored in DB | ID=%s", res.complainant_id)
            return res
        except Exception as e:
            db.rollback()
            complainant_logger.error("Failed to create complainant: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_complainant_by_id(cls, complainant_id: str) -> Optional[Complainant]:
        db = SessionLocal()
        try:
            parsed_id = ComplainantMapper._parse_id(complainant_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(ComplainantDetailsORM, parsed_id)
            if not orm_obj:
                return None
            return ComplainantMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_complainants_by_case_id(cls, case_master_id: str) -> list[Complainant]:
        db = SessionLocal()
        try:
            parsed_case_id = ComplainantMapper._parse_case_id(case_master_id)
            stmt = select(ComplainantDetailsORM).where(ComplainantDetailsORM.casemasterid == parsed_case_id)
            orm_list = db.scalars(stmt).all()
            return [ComplainantMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_complainant(cls, complainant: Complainant) -> Optional[Complainant]:
        db = SessionLocal()
        try:
            parsed_id = ComplainantMapper._parse_id(complainant.complainant_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(ComplainantDetailsORM, parsed_id)
            if not orm_obj:
                return None
            new_orm = ComplainantMapper.to_orm(complainant)
            orm_obj.complainantname = new_orm.complainantname
            orm_obj.ageyear = new_orm.ageyear
            orm_obj.genderid = new_orm.genderid
            db.commit()
            db.refresh(orm_obj)
            ComplainantMapper.cache_domain(complainant, db_id=orm_obj.complainantid)
            return ComplainantMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            complainant_logger.error("Failed to update complainant: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_complainant(cls, complainant_id: str) -> bool:
        db = SessionLocal()
        try:
            parsed_id = ComplainantMapper._parse_id(complainant_id)
            if parsed_id is None:
                return False
            orm_obj = db.get(ComplainantDetailsORM, parsed_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            complainant_logger.error("Failed to delete complainant: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_complainants(
        cls, options: ComplainantQueryOptions
    ) -> tuple[list[Complainant], int]:
        db = SessionLocal()
        try:
            stmt = select(ComplainantDetailsORM)
            if options.case_master_id:
                parsed_case_id = ComplainantMapper._parse_case_id(options.case_master_id)
                stmt = stmt.where(ComplainantDetailsORM.casemasterid == parsed_case_id)
            if options.name:
                stmt = stmt.where(ComplainantDetailsORM.complainantname.ilike(f"%{options.name}%"))

            if hasattr(options, "sort_by") and options.sort_by:
                sort_col = ComplainantDetailsORM.complainantname
                if str(options.sort_by).lower().endswith("name"):
                    sort_col = ComplainantDetailsORM.complainantname
                elif str(options.sort_by).lower().endswith("age"):
                    sort_col = ComplainantDetailsORM.ageyear

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
            return [ComplainantMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
