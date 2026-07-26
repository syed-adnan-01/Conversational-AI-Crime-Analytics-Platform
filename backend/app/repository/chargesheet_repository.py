"""
SQLAlchemy PostgreSQL implementation of ChargesheetRepository.
"""

from typing import Optional, List
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.chargesheet import (
    Chargesheet, ChargesheetAccused, ChargesheetEvidence, ChargesheetSection
)
from app.database.session import SessionLocal
from app.database.orm.chargesheet import ChargesheetDetailsORM
from app.database.mappers.chargesheet_mapper import ChargesheetMapper
from app.common.queries.chargesheet_query import ChargesheetQueryOptions


from app.database.db_list import DBList


class ChargesheetRepository:
    _chargesheets = DBList(ChargesheetDetailsORM)
    _accused_links: list[ChargesheetAccused] = []
    _evidence_links: list[ChargesheetEvidence] = []
    _section_links: list[ChargesheetSection] = []

    @classmethod
    def initialize(cls) -> None:
        app_logger.info("ChargesheetRepository (SQLAlchemy) initialized.")

    @classmethod
    def create_chargesheet(
        cls,
        chargesheet: Chargesheet,
        accused_links: List[ChargesheetAccused] = None,
        evidence_links: List[ChargesheetEvidence] = None,
        section_links: List[ChargesheetSection] = None,
    ) -> Chargesheet:
        db = SessionLocal()
        try:
            orm_obj = ChargesheetMapper.to_orm(chargesheet)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = ChargesheetMapper.to_domain(orm_obj)
            ChargesheetMapper.cache_domain(res)
            if accused_links:
                for al in accused_links:
                    cls._accused_links.append(al.model_copy(update={"chargesheet_id": res.chargesheet_id}))
            if evidence_links:
                for el in evidence_links:
                    cls._evidence_links.append(el.model_copy(update={"chargesheet_id": res.chargesheet_id}))
            if section_links:
                for sl in section_links:
                    cls._section_links.append(sl.model_copy(update={"chargesheet_id": res.chargesheet_id}))
            app_logger.info("Chargesheet stored in DB | ID=%s", res.chargesheet_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create chargesheet: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_chargesheet_by_id(cls, chargesheet_id: str) -> Optional[Chargesheet]:
        db = SessionLocal()
        try:
            parsed_id = ChargesheetMapper._parse_id(chargesheet_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(ChargesheetDetailsORM, parsed_id)
            if not orm_obj:
                return None
            return ChargesheetMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_chargesheet_by_number(cls, chargesheet_number: str) -> Optional[Chargesheet]:
        db = SessionLocal()
        try:
            clean_id = chargesheet_number.replace("CS-NO-", "")
            if clean_id.isdigit():
                orm_obj = db.get(ChargesheetDetailsORM, int(clean_id))
                if orm_obj:
                    return ChargesheetMapper.to_domain(orm_obj)
            return None
        finally:
            db.close()

    @classmethod
    def get_chargesheets_by_case_id(cls, case_master_id: str) -> list[Chargesheet]:
        db = SessionLocal()
        try:
            parsed_case_id = ChargesheetMapper._parse_case_id(case_master_id)
            stmt = select(ChargesheetDetailsORM).where(ChargesheetDetailsORM.casemasterid == parsed_case_id)
            orm_list = db.scalars(stmt).all()
            return [ChargesheetMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def get_accused_links(cls, chargesheet_id: str) -> list[ChargesheetAccused]:
        target_pid = ChargesheetMapper._parse_id(chargesheet_id)
        return [
            ca for ca in cls._accused_links
            if ca.chargesheet_id == chargesheet_id or ChargesheetMapper._parse_id(ca.chargesheet_id) == target_pid
        ]

    @classmethod
    def get_evidence_links(cls, chargesheet_id: str) -> list[ChargesheetEvidence]:
        target_pid = ChargesheetMapper._parse_id(chargesheet_id)
        return [
            ce for ce in cls._evidence_links
            if ce.chargesheet_id == chargesheet_id or ChargesheetMapper._parse_id(ce.chargesheet_id) == target_pid
        ]

    @classmethod
    def get_section_links(cls, chargesheet_id: str) -> list[ChargesheetSection]:
        target_pid = ChargesheetMapper._parse_id(chargesheet_id)
        return [
            cs for cs in cls._section_links
            if cs.chargesheet_id == chargesheet_id or ChargesheetMapper._parse_id(cs.chargesheet_id) == target_pid
        ]

    @classmethod
    def update_chargesheet(
        cls,
        chargesheet: Chargesheet,
        accused_links: Optional[List[ChargesheetAccused]] = None,
        evidence_links: Optional[List[ChargesheetEvidence]] = None,
        section_links: Optional[List[ChargesheetSection]] = None,
    ) -> Optional[Chargesheet]:
        db = SessionLocal()
        try:
            parsed_id = ChargesheetMapper._parse_id(chargesheet.chargesheet_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(ChargesheetDetailsORM, parsed_id)
            if not orm_obj:
                return None
            new_orm = ChargesheetMapper.to_orm(chargesheet)
            orm_obj.csdate = new_orm.csdate
            db.commit()
            db.refresh(orm_obj)
            return ChargesheetMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update chargesheet: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_chargesheet(cls, chargesheet_id: str) -> bool:
        db = SessionLocal()
        try:
            parsed_id = ChargesheetMapper._parse_id(chargesheet_id)
            if parsed_id is None:
                return False
            orm_obj = db.get(ChargesheetDetailsORM, parsed_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete chargesheet: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_chargesheets(
        cls, options: ChargesheetQueryOptions
    ) -> tuple[list[Chargesheet], int]:
        db = SessionLocal()
        try:
            stmt = select(ChargesheetDetailsORM)
            if options.case_master_id:
                parsed_case_id = ChargesheetMapper._parse_case_id(options.case_master_id)
                stmt = stmt.where(ChargesheetDetailsORM.casemasterid == parsed_case_id)

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [ChargesheetMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
