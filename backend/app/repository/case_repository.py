"""
SQLAlchemy PostgreSQL implementation of CaseRepository.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import select, func, or_, text
from app.core.logging import case_logger
from app.models.case_master import CaseMaster
from app.database.session import SessionLocal
from app.database.orm.case_master import CaseMasterORM
from app.database.orm.lookups import EmployeeORM
from app.database.mappers.case_mapper import CaseMapper
from app.schemas.case import SortField, SortOrder
from app.common.queries.case_query import CaseQueryOptions
from app.database.db_list import DBList


class CaseRepository:
    """
    SQLAlchemy-backed repository for CaseMaster entities in PostgreSQL.
    """
    _cases = DBList(CaseMasterORM)

    @classmethod
    def initialize(cls) -> None:
        """
        Verify database connection and seed baseline reference lookups.
        """
        db = SessionLocal()
        try:
            db.execute(text("""
                INSERT INTO employee (employeeid, districtid, unitid, rankid, designationid, firstname)
                VALUES (1, 1, 1, 1, 1, 'Default Officer')
                ON CONFLICT (employeeid) DO NOTHING;

                INSERT INTO unit (unitid, unitname, unittypeid, stateid, districtid)
                VALUES (1, 'Central Station', 1, 1, 1), (101, 'Indiranagar PS', 1, 1, 1)
                ON CONFLICT (unitid) DO NOTHING;

                INSERT INTO casecategory (casecategoryid, lookupvalue) VALUES (1, 'General Crime')
                ON CONFLICT (casecategoryid) DO NOTHING;

                INSERT INTO gravityoffence(gravityoffenceid, lookupvalue) VALUES (1, 'Cognizable')
                ON CONFLICT (gravityoffenceid) DO NOTHING;

                INSERT INTO crimehead (crimeheadid, crimegroupname) VALUES (1, 'Theft')
                ON CONFLICT (crimeheadid) DO NOTHING;

                INSERT INTO crimesubhead (crimesubheadid, crimeheadid, crimeheadname) VALUES (1, 1, 'Vehicle Theft')
                ON CONFLICT (crimesubheadid) DO NOTHING;

                INSERT INTO casestatusmaster (casestatusid, casestatusname) VALUES (1, 'Under Investigation')
                ON CONFLICT (casestatusid) DO NOTHING;
            """))
            db.commit()
            case_logger.info("CaseRepository (SQLAlchemy) initialized.")
        except Exception as e:
            db.rollback()
            case_logger.error("Failed initializing CaseRepository lookups: %s", e)
        finally:
            db.close()

    @classmethod
    def create_case(cls, case: CaseMaster) -> CaseMaster:
        db = SessionLocal()
        try:
            orm_obj = CaseMapper.to_orm(case)
            emp = db.get(EmployeeORM, orm_obj.policepersonid)
            if not emp:
                existing_emp_id = db.scalar(select(EmployeeORM.employeeid))
                if existing_emp_id:
                    orm_obj.policepersonid = existing_emp_id
                else:
                    new_emp = EmployeeORM(
                        employeeid=orm_obj.policepersonid,
                        districtid=1,
                        unitid=1,
                        rankid=1,
                        designationid=1,
                        kgid="EMP001",
                        firstname="Default IO",
                    )
                    db.add(new_emp)
                    db.flush()
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = CaseMapper.to_domain(orm_obj)
            case_logger.info("Case created in DB | ID=%s", res.case_master_id)
            return res
        except Exception as e:
            db.rollback()
            case_logger.error("Failed to create case in DB: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_case_by_id(cls, case_master_id: str) -> Optional[CaseMaster]:
        db = SessionLocal()
        try:
            parsed_id = CaseMapper._parse_id(case_master_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(CaseMasterORM, parsed_id)
            if not orm_obj:
                return None
            return CaseMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_case_by_crime_no(cls, crime_no: str) -> Optional[CaseMaster]:
        db = SessionLocal()
        try:
            stmt = select(CaseMasterORM).where(CaseMasterORM.crimeno == crime_no)
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            return CaseMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_case_by_crime_number(cls, crime_no: str) -> Optional[CaseMaster]:
        """Alias method to support CaseService queries."""
        return cls.get_case_by_crime_no(crime_no)

    @classmethod
    def update_case(cls, case: CaseMaster) -> Optional[CaseMaster]:
        db = SessionLocal()
        try:
            parsed_id = CaseMapper._parse_id(case.case_master_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(CaseMasterORM, parsed_id)
            if not orm_obj:
                return None
            new_orm = CaseMapper.to_orm(case)
            orm_obj.crimeno = new_orm.crimeno
            orm_obj.caseno = new_orm.caseno
            orm_obj.crimeregistereddate = new_orm.crimeregistereddate
            orm_obj.brieffacts = new_orm.brieffacts
            orm_obj.policestationid = new_orm.policestationid
            orm_obj.policepersonid = new_orm.policepersonid
            orm_obj.casecategoryid = new_orm.casecategoryid
            orm_obj.gravityoffenceid = new_orm.gravityoffenceid
            orm_obj.crimemajorheadid = new_orm.crimemajorheadid
            orm_obj.crimeminorheadid = new_orm.crimeminorheadid
            orm_obj.casestatusid = new_orm.casestatusid
            orm_obj.courtid = new_orm.courtid
            orm_obj.latitude = new_orm.latitude
            orm_obj.longitude = new_orm.longitude
            db.commit()
            db.refresh(orm_obj)
            return CaseMapper.to_domain(orm_obj)
        except Exception as e:
            db.rollback()
            case_logger.error("Failed to update case: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def delete_case(cls, case_master_id: str) -> bool:
        db = SessionLocal()
        try:
            parsed_id = CaseMapper._parse_id(case_master_id)
            if parsed_id is None:
                return False
            orm_obj = db.get(CaseMasterORM, parsed_id)
            if not orm_obj:
                return False
            db.delete(orm_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            case_logger.error("Failed to delete case: %s", e)
            return False
        finally:
            db.close()

    @classmethod
    def get_all_cases(cls) -> list[CaseMaster]:
        db = SessionLocal()
        try:
            orm_list = db.scalars(select(CaseMasterORM)).all()
            return [CaseMapper.to_domain(item) for item in orm_list]
        finally:
            db.close()

    @classmethod
    def query_cases(
        cls, options: CaseQueryOptions
    ) -> tuple[list[CaseMaster], int]:
        db = SessionLocal()
        try:
            stmt = select(CaseMasterORM)
            if options.crime_no:
                stmt = stmt.where(CaseMasterORM.crimeno.ilike(f"%{options.crime_no}%"))
            if options.case_no:
                stmt = stmt.where(CaseMasterORM.caseno.ilike(f"%{options.case_no}%"))
            if options.status:
                status_id = getattr(options.status, "value", str(options.status))
                try:
                    stmt = stmt.where(CaseMasterORM.casestatusid == int(status_id))
                except ValueError:
                    pass
            if options.category:
                cat_id = getattr(options.category, "value", str(options.category))
                try:
                    stmt = stmt.where(CaseMasterORM.casecategoryid == int(cat_id))
                except ValueError:
                    pass
            if options.io_emp_id:
                try:
                    stmt = stmt.where(CaseMasterORM.policepersonid == int(options.io_emp_id))
                except ValueError:
                    pass
            if options.date_from:
                stmt = stmt.where(CaseMasterORM.crimeregistereddate >= options.date_from)
            if options.date_to:
                stmt = stmt.where(CaseMasterORM.crimeregistereddate <= options.date_to)
            if options.search_term:
                term = f"%{options.search_term}%"
                stmt = stmt.where(
                    (CaseMasterORM.crimeno.ilike(term))
                    | (CaseMasterORM.caseno.ilike(term))
                    | (CaseMasterORM.brieffacts.ilike(term))
                )

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = db.scalar(count_stmt) or 0

            # Sorting
            if options.sort_by:
                sort_col = CaseMasterORM.crimeregistereddate
                if options.sort_by == SortField.CRIME_NO:
                    sort_col = CaseMasterORM.crimeno
                elif options.sort_by == SortField.INCIDENT_DATE:
                    sort_col = CaseMasterORM.incidentfromdate
                elif options.sort_by == SortField.CREATED_DATE:
                    sort_col = CaseMasterORM.crimeregistereddate

                if options.sort_order == SortOrder.DESC:
                    stmt = stmt.order_by(sort_col.desc())
                else:
                    stmt = stmt.order_by(sort_col.asc())

            page = options.page or 1
            size = options.page_size or 10
            stmt = stmt.offset((page - 1) * size).limit(size)

            orm_list = db.scalars(stmt).all()
            return [CaseMapper.to_domain(o) for o in orm_list], total
        finally:
            db.close()
