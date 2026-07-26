"""
SQLAlchemy PostgreSQL implementation of SectionRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.section import Section
from app.database.session import SessionLocal
from app.database.orm.section import SectionORM
from app.database.mappers.section_mapper import SectionMapper
from app.common.queries.section_query import SectionQueryOptions
from app.database.db_list import DBList


class SectionRepository:
    _sections = DBList(SectionORM)

    @classmethod
    def initialize(cls) -> None:
        db = SessionLocal()
        try:
            from app.repository.seed.legal_seed import SEED_SECTIONS
            default_sections = [
                ("SEC-303", "BNS", "303", "Theft", "Punishment for theft"),
                ("SEC-304", "BNS", "304", "Snatching", "Punishment for snatching"),
                ("SEC-310", "BNS", "310", "Dacoity", "Punishment for dacoity"),
            ]
            for sec_id, act_code, sec_no, title, desc in default_sections:
                stmt = select(SectionORM).where(SectionORM.sectioncode == sec_no)
                existing = db.scalar(stmt)
                if not existing:
                    domain_sec = Section(
                        section_id=sec_id,
                        act_id=act_code,
                        section_number=sec_no,
                        title=title,
                        description=desc,
                    )
                    orm_obj = SectionMapper.to_orm(domain_sec)
                    db.merge(orm_obj)

            for sec_data in SEED_SECTIONS:
                sec_id = sec_data["section_id"]
                sec_no = sec_data["section_number"]
                stmt = select(SectionORM).where(
                    (SectionORM.sectioncode == sec_id)
                    | (SectionORM.sectioncode == sec_no)
                )
                existing = db.scalar(stmt)
                if not existing:
                    domain_sec = Section(
                        section_id=sec_id,
                        act_id=sec_data["act_id"],
                        section_number=sec_no,
                        title=sec_data["title"],
                        description=sec_data.get("description"),
                    )
                    orm_obj = SectionMapper.to_orm(domain_sec)
                    db.merge(orm_obj)

            db.commit()
            app_logger.info("SectionRepository (SQLAlchemy) initialized.")
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to initialize sections: %s", e)
        finally:
            db.close()

    @classmethod
    def create_section(cls, section: Section) -> Section:
        db = SessionLocal()
        try:
            orm_obj = SectionMapper.to_orm(section)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = SectionMapper.to_domain(orm_obj)
            app_logger.info("Section created in DB | ID=%s", res.section_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create section: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_section_by_id(cls, section_id: str) -> Optional[Section]:
        db = SessionLocal()
        try:
            stmt = select(SectionORM).where(
                (SectionORM.sectioncode == section_id)
                | (SectionORM.sectioncode == section_id.replace("SEC-", ""))
            )
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            return SectionMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_section_by_number(cls, act_id: str, section_number: str) -> Optional[Section]:
        secs = cls.get_sections_by_act_id(act_id)
        for s in secs:
            if s.section_number.strip().lower() == section_number.strip().lower():
                return s
        return None

    @classmethod
    def get_sections_by_act_id(cls, act_id: str) -> list[Section]:
        db = SessionLocal()
        try:
            stmt = select(SectionORM).where(SectionORM.actcode.ilike(act_id))
            orm_list = db.scalars(stmt).all()
            return [SectionMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def get_sections_by_ids(cls, section_ids: list[str]) -> list[Section]:
        db = SessionLocal()
        try:
            parsed_ids = [s.replace("SEC-", "") for s in section_ids]
            stmt = select(SectionORM).where(
                (SectionORM.sectioncode.in_(section_ids))
                | (SectionORM.sectioncode.in_(parsed_ids))
            )
            orm_list = db.scalars(stmt).all()
            return [SectionMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_section(cls, section: Section) -> Optional[Section]:
        db = SessionLocal()
        try:
            stmt = select(SectionORM).where(
                (SectionORM.sectioncode == section.section_id)
                | (SectionORM.sectioncode == section.section_id.replace("SEC-", ""))
            )
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            new_orm = SectionMapper.to_orm(section)
            orm_obj.sectiondescription = new_orm.sectiondescription
            db.commit()
            db.refresh(orm_obj)
            return SectionMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update section: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_section(cls, section_id: str) -> bool:
        db = SessionLocal()
        try:
            stmt = select(SectionORM).where(
                (SectionORM.sectioncode == section_id)
                | (SectionORM.sectioncode == section_id.replace("SEC-", ""))
            )
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete section: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_sections(
        cls, options: SectionQueryOptions
    ) -> tuple[list[Section], int]:
        db = SessionLocal()
        try:
            stmt = select(SectionORM)
            if hasattr(options, "act_id") and options.act_id:
                stmt = stmt.where(SectionORM.actcode.ilike(options.act_id))
            if hasattr(options, "section_number") and options.section_number:
                stmt = stmt.where(SectionORM.sectioncode.ilike(f"%{options.section_number}%"))
            search_term = getattr(options, "search_term", None)
            if search_term:
                term = f"%{search_term}%"
                stmt = stmt.where(
                    (SectionORM.sectioncode.ilike(term))
                    | (SectionORM.sectiondescription.ilike(term))
                )

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            page = getattr(options, "page", 1) or 1
            size = getattr(options, "page_size", 10) or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [SectionMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
