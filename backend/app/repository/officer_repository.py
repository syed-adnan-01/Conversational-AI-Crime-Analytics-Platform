"""
SQLAlchemy PostgreSQL implementation of OfficerRepository.
"""

from typing import Optional
from sqlalchemy import select, func
from app.core.logging import app_logger
from app.models.officer import OfficerMaster, OfficerAssignment
from app.database.session import SessionLocal
from app.database.orm.lookups import EmployeeORM
from app.database.mappers.officer_mapper import OfficerMapper
from app.common.queries.officer_query import OfficerAssignmentQueryOptions


from app.database.db_list import DBList


class OfficerRepository:
    _officers = DBList(EmployeeORM)
    _assignments: list[OfficerAssignment] = []

    @classmethod
    def initialize(cls) -> None:
        db = SessionLocal()
        try:
            emp = db.get(EmployeeORM, 1)
            if not emp:
                default_emp = EmployeeORM(
                    employeeid=1,
                    districtid=1,
                    unitid=1,
                    rankid=1,
                    designationid=1,
                    kgid="EMP001",
                    firstname="Default IO",
                )
                db.add(default_emp)
                db.commit()
            app_logger.info("OfficerRepository (SQLAlchemy) initialized.")
        except Exception as e:
            db.rollback()
            app_logger.error("Failed initializing OfficerRepository: %s", e)
        finally:
            db.close()

    @classmethod
    def create_officer(cls, officer: OfficerMaster) -> OfficerMaster:
        db = SessionLocal()
        try:
            orm_obj = OfficerMapper.to_orm(officer)
            db.add(orm_obj)
            db.commit()
            db.refresh(orm_obj)
            res = OfficerMapper.to_domain(orm_obj)
            app_logger.info("Officer stored in DB | ID=%s", res.officer_id)
            return res
        except Exception as e:
            db.rollback()
            app_logger.error("Failed to create officer: %s", e)
            raise
        finally:
            db.close()

    @classmethod
    def get_officer_by_id(cls, officer_id: str) -> Optional[OfficerMaster]:
        db = SessionLocal()
        try:
            parsed_id = OfficerMapper._parse_id(officer_id)
            if parsed_id is None:
                return None
            orm_obj = db.get(EmployeeORM, parsed_id)
            if not orm_obj:
                return None
            return OfficerMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def get_officer_by_badge(cls, badge_number: str) -> Optional[OfficerMaster]:
        db = SessionLocal()
        try:
            stmt = select(EmployeeORM).where(EmployeeORM.kgid.ilike(badge_number))
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            return OfficerMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def list_officers(cls) -> list[OfficerMaster]:
        db = SessionLocal()
        try:
            stmt = select(EmployeeORM)
            orm_list = db.scalars(stmt).all()
            return [OfficerMapper.to_domain(o) for o in orm_list]
        finally:
            db.close()

    # Officer Assignments (In-memory / Transients)
    @classmethod
    def create_assignment(cls, assignment: OfficerAssignment) -> OfficerAssignment:
        cls._assignments.append(assignment)
        return assignment

    @classmethod
    def get_assignment_by_id(cls, assignment_id: str) -> Optional[OfficerAssignment]:
        return next((a for a in cls._assignments if a.assignment_id == assignment_id), None)

    @classmethod
    def update_assignment(cls, assignment: OfficerAssignment) -> Optional[OfficerAssignment]:
        for idx, a in enumerate(cls._assignments):
            if a.assignment_id == assignment.assignment_id:
                cls._assignments[idx] = assignment
                return assignment
        return None

    @classmethod
    def delete_assignment(cls, assignment_id: str) -> bool:
        for idx, a in enumerate(cls._assignments):
            if a.assignment_id == assignment_id:
                del cls._assignments[idx]
                return True
        return False

    @classmethod
    def query_assignments(
        cls, options: OfficerAssignmentQueryOptions
    ) -> tuple[list[OfficerAssignment], int]:
        filtered = list(cls._assignments)
        if options.case_master_id:
            filtered = [a for a in filtered if a.case_master_id == options.case_master_id]
        total = len(filtered)
        return filtered, total
