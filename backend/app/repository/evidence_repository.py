"""
SQLAlchemy PostgreSQL implementation of EvidenceRepository.
"""

from typing import Optional
from uuid import uuid4
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.evidence import Evidence
from app.database.session import SessionLocal
from app.database.orm.evidence import EvidenceORM
from app.database.mappers.evidence_mapper import EvidenceMapper
from app.common.queries.evidence_query import EvidenceQueryOptions


from app.database.db_list import DBList


class EvidenceRepository:
    _evidence_list = DBList(EvidenceORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("EvidenceRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_evidence(cls, evidence: Evidence) -> Evidence:
        db = SessionLocal()
        try:
            if not evidence.evidence_id:
                evidence = evidence.model_copy(update={"evidence_id": f"EV-{uuid4().hex[:12].upper()}"})
            orm_obj = EvidenceMapper.to_orm(evidence)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = EvidenceMapper.to_domain(orm_obj)
            app_logger.info("Evidence stored in DB | ID=%s", res.evidence_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create evidence: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_evidence_by_id(cls, evidence_id: str) -> Optional[Evidence]:
        db = SessionLocal()
        try:
            orm_obj = db.get(EvidenceORM, evidence_id)
            if not orm_obj:
                return None
            return EvidenceMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_case_evidence(cls, case_master_id: str) -> list[Evidence]:
        db = SessionLocal()
        try:
            stmt = select(EvidenceORM).where(EvidenceORM.case_master_id == case_master_id)
            orm_list = db.scalars(stmt).all()
            return [EvidenceMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_evidence(cls, evidence: Evidence) -> Optional[Evidence]:
        db = SessionLocal()
        try:
            if not evidence.evidence_id:
                return None
            orm_obj = db.get(EvidenceORM, evidence.evidence_id)
            if not orm_obj:
                return None
            new_orm = EvidenceMapper.to_orm(evidence)
            orm_obj.description = new_orm.description
            orm_obj.storage_location = new_orm.storage_location
            db.commit()
            db.refresh(orm_obj)
            return EvidenceMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update evidence: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_evidence(cls, evidence_id: str) -> bool:
        db = SessionLocal()
        try:
            orm_obj = db.get(EvidenceORM, evidence_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete evidence: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_evidence(
        cls, options: EvidenceQueryOptions
    ) -> tuple[list[Evidence], int]:
        db = SessionLocal()
        try:
            stmt = select(EvidenceORM)
            if options.case_master_id:
                stmt = stmt.where(EvidenceORM.case_master_id == options.case_master_id)
            if options.evidence_type:
                ev_type_val = options.evidence_type.value if hasattr(options.evidence_type, "value") else str(options.evidence_type)
                stmt = stmt.where(EvidenceORM.evidence_type == ev_type_val)
            if options.collected_by:
                stmt = stmt.where(EvidenceORM.collected_by.ilike(f"%{options.collected_by}%"))
            if options.evidence_number:
                stmt = stmt.where(EvidenceORM.evidence_number.ilike(f"%{options.evidence_number}%"))

            orm_list = db.scalars(stmt).all()
            domains = [EvidenceMapper.to_domain(o) for o in orm_list]

            # Filter non-ORM or cached domain properties
            filtered = []
            for item in domains:
                if options.title and options.title.lower() not in item.title.lower():
                    continue
                if options.status and item.status != options.status:
                    continue
                if options.victim_id and item.victim_id != options.victim_id:
                    continue
                if options.accused_id and item.accused_id != options.accused_id:
                    continue
                if options.section_id and item.section_id != options.section_id:
                    continue
                filtered.append(item)

            total = len(filtered)
            page = options.page or 1
            size = options.page_size or 10
            start = (page - 1) * size
            end = start + size
            return filtered[start:end], total
        finally:
            db.close()
