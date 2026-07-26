"""
SQLAlchemy PostgreSQL implementation of ActRepository.
"""

from typing import Optional
from sqlalchemy import select, func, text
from app.core.logging import app_logger
from app.models.act import Act
from app.database.session import SessionLocal
from app.database.orm.act import ActORM
from app.database.mappers.act_mapper import ActMapper
from app.common.queries.act_query import ActQueryOptions
from app.database.db_list import DBList


class ActRepository:
    _acts = DBList(ActORM)

    @classmethod
    def initialize(cls) -> None:
        db = SessionLocal()
        try:
            from app.repository.seed.legal_seed import SEED_ACTS, SEED_SECTIONS
            default_acts = [
                ("BNS", "Bharatiya Nyaya Sanhita, 2023", "BNS", 2023),
                ("BNSS", "Bharatiya Nagarik Suraksha Sanhita, 2023", "BNSS", 2023),
                ("IT Act", "Information Technology Act, 2000", "IT Act", 2000),
                ("NDPS", "Narcotic Drugs and Psychotropic Substances Act, 1985", "NDPS", 1985),
                ("POCSO", "Protection of Children from Sexual Offences Act, 2012", "POCSO", 2012),
                ("CrPC", "Code of Criminal Procedure, 1973", "CrPC", 1973),
            ]
            default_codes = tuple({a[0] for a in default_acts} | {a["act_id"] for a in SEED_ACTS})
            default_sec_codes = tuple({"SEC-303", "SEC-304", "SEC-310", "303", "304", "310"} | {s["section_id"] for s in SEED_SECTIONS} | {s["section_number"] for s in SEED_SECTIONS})

            db.execute(text("DELETE FROM actsectionassociation WHERE sectionid NOT IN :secs OR actid NOT IN :acts"), {"secs": default_sec_codes, "acts": default_codes})
            db.execute(text("DELETE FROM section WHERE actcode NOT IN :acts OR sectioncode NOT IN :secs"), {"secs": default_sec_codes, "acts": default_codes})
            db.execute(text("DELETE FROM act WHERE actcode NOT IN :acts"), {"acts": default_codes})
            db.commit()

            for act_code, desc, short_name, year in default_acts:
                existing = db.get(ActORM, act_code)
                if not existing:
                    domain_act = Act(
                        act_id=act_code,
                        name=desc,
                        short_name=short_name,
                        year=year,
                        description=desc,
                    )
                    orm_obj = ActMapper.to_orm(domain_act)
                    db.merge(orm_obj)

            for act_data in SEED_ACTS:
                existing = db.get(ActORM, act_data["act_id"])
                if not existing:
                    domain_act = Act(
                        act_id=act_data["act_id"],
                        name=act_data["name"],
                        short_name=act_data["short_name"],
                        year=act_data["year"],
                        description=act_data["description"],
                    )
                    orm_obj = ActMapper.to_orm(domain_act)
                    db.merge(orm_obj)
            db.commit()
            app_logger.info("ActRepository (SQLAlchemy) initialized.")
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to initialize acts: %s", e)
        finally:
            db.close()

    @classmethod
    def create_act(cls, act: Act) -> Act:
        db = SessionLocal()
        try:
            orm_obj = ActMapper.to_orm(act)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = ActMapper.to_domain(orm_obj)
            app_logger.info("Act created in DB | ID=%s", res.act_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create act: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_act_by_id(cls, act_id: str) -> Optional[Act]:
        db = SessionLocal()
        try:
            orm_obj = db.get(ActORM, act_id)
            if not orm_obj:
                return None
            return ActMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_act_by_short_name(cls, short_name: str, year: int) -> Optional[Act]:
        db = SessionLocal()
        try:
            stmt = select(ActORM).where(ActORM.shortname.ilike(short_name))
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            return ActMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_acts_by_ids(cls, act_ids: list[str]) -> list[Act]:
        db = SessionLocal()
        try:
            stmt = select(ActORM).where(ActORM.actcode.in_(act_ids))
            orm_list = db.scalars(stmt).all()
            return [ActMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    @classmethod
    def update_act(cls, act: Act) -> Optional[Act]:
        db = SessionLocal()
        try:
            orm_obj = db.get(ActORM, act.act_id)
            if not orm_obj:
                return None
            new_orm = ActMapper.to_orm(act)
            orm_obj.shortname = new_orm.shortname
            orm_obj.actdescription = new_orm.actdescription
            db.commit()
            db.refresh(orm_obj)
            return ActMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to update act: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_act(cls, act_id: str) -> bool:
        db = SessionLocal()
        try:
            orm_obj = db.get(ActORM, act_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to delete act: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def query_acts(
        cls, options: ActQueryOptions
    ) -> tuple[list[Act], int]:
        db = SessionLocal()
        try:
            stmt = select(ActORM)
            if hasattr(options, "short_name") and options.short_name:
                stmt = stmt.where(ActORM.shortname.ilike(f"%{options.short_name}%"))
            if hasattr(options, "name") and options.name:
                stmt = stmt.where(ActORM.actdescription.ilike(f"%{options.name}%"))
            search_term = getattr(options, "search_term", None)
            if search_term:
                term = f"%{search_term}%"
                stmt = stmt.where(
                    (ActORM.shortname.ilike(term))
                    | (ActORM.actdescription.ilike(term))
                )

            orm_list = db.scalars(stmt).all()
            domain_list = [ActMapper.to_domain(o) for o in orm_list]

            if hasattr(options, "sort_by") and options.sort_by:
                sort_field = str(options.sort_by).lower()
                is_desc = hasattr(options, "sort_order") and str(options.sort_order).lower().endswith("desc")

                if "year" in sort_field:
                    domain_list.sort(key=lambda a: a.year or 0, reverse=is_desc)
                elif "short_name" in sort_field or "name" in sort_field:
                    domain_list.sort(key=lambda a: (a.short_name or "").lower(), reverse=is_desc)

            total = len(domain_list)
            page = getattr(options, "page", 1) or 1
            size = getattr(options, "page_size", 10) or 10
            start = (page - 1) * size
            end = start + size

            return domain_list[start:end], total
        finally:
            db.close()
