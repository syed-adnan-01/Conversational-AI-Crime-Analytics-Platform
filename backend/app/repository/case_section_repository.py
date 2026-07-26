"""
SQLAlchemy PostgreSQL implementation of CaseSectionRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.case_section import CaseSectionAssociation
from app.database.session import SessionLocal
from app.database.orm.case_section import ActSectionAssociationORM
from app.database.mappers.case_section_mapper import CaseSectionMapper
from app.common.queries.case_section_query import CaseSectionQueryOptions


from app.database.db_list import DBList


class CaseSectionRepository:
    _associations = DBList(ActSectionAssociationORM)
    @classmethod
    def initialize(cls) -> None:
        app_logger.info("CaseSectionRepository (SQLAlchemy) initialized.")

    @classmethod
    def assign_section_to_case(
        cls, association: CaseSectionAssociation
    ) -> CaseSectionAssociation:
        db = SessionLocal()
        try:
            orm_obj = CaseSectionMapper.to_orm(association)
            db.add(orm_obj)
            db.commit()
            res = CaseSectionMapper.to_domain(orm_obj)
            app_logger.info("Case section assigned in DB | ID=%s", res.association_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to assign case section: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_association_by_id(
        cls, association_id: str
    ) -> Optional[CaseSectionAssociation]:
        db = SessionLocal()
        try:
            if association_id.startswith("CSA-"):
                rest = association_id[4:]
                parts = rest.split("-", 1)
                if len(parts) == 2:
                    case_id = CaseSectionMapper._parse_case_id(parts[0])
                    sec_id = parts[1]
                    stmt = select(ActSectionAssociationORM).where(
                        ActSectionAssociationORM.casemasterid == case_id,
                        ActSectionAssociationORM.sectionid == sec_id,
                    )
                    orm_obj = db.scalar(stmt)
                    if orm_obj:
                        return CaseSectionMapper.to_domain(orm_obj)
            return None
        finally:
            db.close()

    @classmethod
    def get_association_by_case_and_section(
        cls, case_master_id: str, section_id: str
    ) -> Optional[CaseSectionAssociation]:
        db = SessionLocal()
        try:
            parsed_case_id = CaseSectionMapper._parse_case_id(case_master_id)
            stmt = select(ActSectionAssociationORM).where(
                ActSectionAssociationORM.casemasterid == parsed_case_id,
                ActSectionAssociationORM.sectionid == section_id,
            )
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            return CaseSectionMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_case_sections(cls, case_master_id: str) -> list[CaseSectionAssociation]:
        db = SessionLocal()
        try:
            parsed_case_id = CaseSectionMapper._parse_case_id(case_master_id)
            stmt = select(ActSectionAssociationORM).where(
                ActSectionAssociationORM.casemasterid == parsed_case_id
            )
            orm_list = db.scalars(stmt).all()
            return [CaseSectionMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def remove_section(cls, association_id: str) -> bool:
        db = SessionLocal()
        try:
            if association_id.startswith("CSA-"):
                rest = association_id[4:]
                parts = rest.split("-", 1)
                if len(parts) == 2:
                    case_id = CaseSectionMapper._parse_case_id(parts[0])
                    sec_id = parts[1]
                    stmt = select(ActSectionAssociationORM).where(
                        ActSectionAssociationORM.casemasterid == case_id,
                        ActSectionAssociationORM.sectionid == sec_id,
                    )
                    orm_obj = db.scalar(stmt)
                    if orm_obj:
                        db.delete(orm_obj)
                        db.commit()
                        return True
            return False
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to remove case section: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_case_sections(
        cls, options: CaseSectionQueryOptions
    ) -> tuple[list[CaseSectionAssociation], int]:
        db = SessionLocal()
        try:
            stmt = select(ActSectionAssociationORM)
            if options.case_master_id:
                parsed_case_id = CaseSectionMapper._parse_case_id(options.case_master_id)
                stmt = stmt.where(ActSectionAssociationORM.casemasterid == parsed_case_id)
            if options.section_id:
                stmt = stmt.where(ActSectionAssociationORM.sectionid == options.section_id)

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [CaseSectionMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
