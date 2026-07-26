"""
Mapper between User domain model and UserORM.
"""

from typing import Dict
from app.models.user import User
from app.database.orm.user import UserORM
from app.core.roles import UserRole

DEPT_MAP: Dict[str, str] = {
    "EMP001": "Cyber Crime",
    "EMP002": "Crime Analytics",
    "EMP003": "Investigation",
}


class UserMapper:
    @classmethod
    def register_department(cls, employee_id: str, department: str):
        if employee_id and department:
            DEPT_MAP[employee_id] = department

    @classmethod
    def to_domain(cls, orm: UserORM) -> User:
        role_val = UserRole.INVESTIGATOR
        try:
            role_val = UserRole(orm.role)
        except ValueError:
            pass

        dept = DEPT_MAP.get(orm.employee_id, "Police")

        return User(
            user_id=orm.employee_id,
            employee_id=orm.employee_id,
            name=orm.full_name,
            email=f"{orm.employee_id.lower()}@crime.gov.in",
            department=dept,
            role=role_val,
            is_active=orm.is_active,
        )

    @classmethod
    def to_orm(cls, domain: User, hashed_password: str = "") -> UserORM:
        if domain.employee_id and domain.department:
            DEPT_MAP[domain.employee_id] = domain.department
        return UserORM(
            employee_id=domain.employee_id,
            full_name=domain.name,
            role=domain.role.value if hasattr(domain.role, "value") else str(domain.role),
            is_active=domain.is_active,
            hashed_password=hashed_password,
        )
