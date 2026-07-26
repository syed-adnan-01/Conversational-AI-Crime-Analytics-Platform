"""
SQLAlchemy PostgreSQL implementation of VictimRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.victim import Victim
from app.database.session import SessionLocal
from app.database.orm.victim import VictimORM
from app.database.mappers.victim_mapper import VictimMapper
from app.common.queries.victim_query import VictimQueryOptions


from app.database.db_list import DBList


class VictimRepository:
    _victims = DBList(VictimORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("VictimRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_victim(cls, victim: Victim) -> Victim:
        db = SessionLocal()
        try:
            orm_obj = VictimMapper.to_orm(victim)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            VictimMapper.cache_domain(victim, db_id=orm_obj.victimmasterid)
            res = VictimMapper.to_domain(orm_obj)
            app_logger.info("Victim stored in DB | ID=%s", res.victim_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create victim: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_victim_by_id(cls, victim_id: str) -> Optional[Victim]:
        db = SessionLocal()
        try:
            parsed_id = VictimMapper._parse_id(victim_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(VictimORM, parsed_id)
            if not orm_obj:
                return None
            return VictimMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_victims_by_case_id(cls, case_master_id: str) -> list[Victim]:
        db = SessionLocal()
        try:
            parsed_case_id = VictimMapper._parse_case_id(case_master_id)
            stmt = select(VictimORM).where(VictimORM.casemasterid == parsed_case_id)
            orm_list = db.scalars(stmt).all()
            return [VictimMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_victim(cls, victim: Victim) -> Optional[Victim]:
        db = SessionLocal()
        try:
            parsed_id = VictimMapper._parse_id(victim.victim_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(VictimORM, parsed_id)
            if not orm_obj:
                return None
            new_orm = VictimMapper.to_orm(victim)
            orm_obj.victimname = new_orm.victimname
            orm_obj.ageyear = new_orm.ageyear
            orm_obj.genderid = new_orm.genderid
            db.commit()
            db.refresh(orm_obj)
            VictimMapper.cache_domain(victim, db_id=orm_obj.victimmasterid)
            return VictimMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update victim: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_victim(cls, victim_id: str) -> bool:
        db = SessionLocal()
        try:
            parsed_id = VictimMapper._parse_id(victim_id)
            if parsed_id is None:
                return False
            orm_obj = db.get(VictimORM, parsed_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete victim: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_victims(
        cls, options: VictimQueryOptions
    ) -> tuple[list[Victim], int]:
        db = SessionLocal()
        try:
            stmt = select(VictimORM)
            if options.case_master_id:
                parsed_case_id = VictimMapper._parse_case_id(options.case_master_id)
                stmt = stmt.where(VictimORM.casemasterid == parsed_case_id)
            if options.name:
                stmt = stmt.where(VictimORM.victimname.ilike(f"%{options.name}%"))

            if hasattr(options, "sort_by") and options.sort_by:
                sort_col = VictimORM.victimname
                if str(options.sort_by).lower().endswith("name"):
                    sort_col = VictimORM.victimname
                elif str(options.sort_by).lower().endswith("age"):
                    sort_col = VictimORM.ageyear

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
            return [VictimMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
