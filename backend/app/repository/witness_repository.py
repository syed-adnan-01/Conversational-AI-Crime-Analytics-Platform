"""
SQLAlchemy PostgreSQL implementation of WitnessRepository.
"""

from typing import Optional
from uuid import uuid4
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.witness import Witness
from app.database.session import SessionLocal
from app.database.orm.witness import WitnessORM
from app.database.mappers.witness_mapper import WitnessMapper
from app.common.queries.witness_query import WitnessQueryOptions


from app.database.db_list import DBList


class WitnessRepository:
    _witnesses = DBList(WitnessORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("WitnessRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_witness(cls, witness: Witness) -> Witness:
        db = SessionLocal()
        try:
            if not witness.witness_id:
                witness = witness.model_copy(update={"witness_id": f"WIT-{uuid4().hex[:12].upper()}"})
            orm_obj = WitnessMapper.to_orm(witness)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = WitnessMapper.to_domain(orm_obj)
            app_logger.info("Witness stored in DB | ID=%s", res.witness_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create witness: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_witness_by_id(cls, witness_id: str) -> Optional[Witness]:
        db = SessionLocal()
        try:
            orm_obj = db.get(WitnessORM, witness_id)
            if not orm_obj:
                return None
            return WitnessMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_witnesses_by_case_id(cls, case_master_id: str) -> list[Witness]:
        db = SessionLocal()
        try:
            stmt = select(WitnessORM).where(WitnessORM.case_master_id == case_master_id)
            orm_list = db.scalars(stmt).all()
            return [WitnessMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_witness(cls, witness: Witness) -> Optional[Witness]:
        db = SessionLocal()
        try:
            if not witness.witness_id:
                return None
            orm_obj = db.get(WitnessORM, witness.witness_id)
            if not orm_obj:
                return None
            new_orm = WitnessMapper.to_orm(witness)
            orm_obj.witness_name = new_orm.witness_name
            orm_obj.statement_summary = new_orm.statement_summary
            orm_obj.contact_number = new_orm.contact_number
            orm_obj.witness_type = new_orm.witness_type
            db.commit()
            db.refresh(orm_obj)
            return WitnessMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update witness: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_witness(cls, witness_id: str) -> bool:
        db = SessionLocal()
        try:
            orm_obj = db.get(WitnessORM, witness_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete witness: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_witnesses(
        cls, options: WitnessQueryOptions
    ) -> tuple[list[Witness], int]:
        db = SessionLocal()
        try:
            stmt = select(WitnessORM)
            if options.case_master_id:
                stmt = stmt.where(WitnessORM.case_master_id == options.case_master_id)
            if options.name:
                stmt = stmt.where(WitnessORM.witness_name.ilike(f"%{options.name}%"))

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [WitnessMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
