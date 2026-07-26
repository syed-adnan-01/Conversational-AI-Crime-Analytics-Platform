"""
SQLAlchemy PostgreSQL implementation of UserRepository.
"""

from typing import Optional
from sqlalchemy import select, delete
from app.core.password import PasswordManager
from app.models.user import User
from app.database.session import SessionLocal
from app.database.orm.user import UserORM
from app.database.mappers.user_mapper import UserMapper
from app.repository.seed_users import SEED_USERS
from app.database.db_list import DBList


class UserRepository:
    _users = DBList(UserORM)

    @classmethod
    def initialize(cls) -> None:
        """
        Seed / update initial users in PostgreSQL with hashed passwords.
        Remove temporary test users (EMP004, EMP005, etc.) so test lifespans start clean.
        """
        db = SessionLocal()
        try:
            # Clean up test dynamic users so test lifespans start fresh
            db.execute(delete(UserORM).where(UserORM.employee_id.notin_(["EMP001", "EMP002", "EMP003"])))

            for seed in SEED_USERS:
                stmt = select(UserORM).where(UserORM.employee_id == seed["employee_id"])
                existing = db.scalar(stmt)
                hashed = PasswordManager.hash_password(seed["password"])
                user_domain = User(
                    user_id=seed["employee_id"],
                    employee_id=seed["employee_id"],
                    name=seed["name"],
                    email=seed["email"],
                    department=seed["department"],
                    role=seed["role"],
                    is_active=seed["is_active"],
                )
                if not existing:
                    orm_obj = UserMapper.to_orm(user_domain, hashed_password=hashed)
                    db.add(orm_obj)
                else:
                    existing.hashed_password = hashed
                    existing.full_name = seed["name"]
                    existing.role = seed["role"].value if hasattr(seed["role"], "value") else str(seed["role"])
                UserMapper.register_department(seed["employee_id"], seed["department"])
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

    @classmethod
    def get_by_employee_id(cls, employee_id: str) -> Optional[dict]:
        db = SessionLocal()
        try:
            stmt = select(UserORM).where(UserORM.employee_id == employee_id)
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            user_domain = UserMapper.to_domain(orm_obj)
            res = user_domain.model_dump()
            res["password"] = orm_obj.hashed_password
            return res
        finally:
            db.close()

    @classmethod
    def get_user(cls, employee_id: str) -> Optional[User]:
        db = SessionLocal()
        try:
            stmt = select(UserORM).where(UserORM.employee_id == employee_id)
            orm_obj = db.scalar(stmt)
            if not orm_obj:
                return None
            return UserMapper.to_domain(orm_obj)
        finally:
            db.close()

    @classmethod
    def list_users(cls) -> list[User]:
        """Additive read-only query for application administration APIs."""
        db = SessionLocal()
        try:
            return [UserMapper.to_domain(item) for item in db.scalars(select(UserORM)).all()]
        finally:
            db.close()

    @classmethod
    def save_user(cls, user: User, password: str = "") -> User:
        db = SessionLocal()
        try:
            hashed = PasswordManager.hash_password(password) if password else ""
            orm_obj = UserMapper.to_orm(user, hashed_password=hashed)
            db.merge(orm_obj)
            db.commit()
            return UserMapper.to_domain(orm_obj)
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
