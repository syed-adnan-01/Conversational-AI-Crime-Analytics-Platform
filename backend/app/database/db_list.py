"""
Helper list subclass that bridges in-memory test list operations (.clear(), .append(), iteration) with PostgreSQL SQLAlchemy entities.
"""

from typing import Type
from sqlalchemy import text, select
from app.database.session import SessionLocal


class DBList(list):
    def __init__(self, orm_class: Type):
        super().__init__()
        self.orm_class = orm_class

    def clear(self) -> None:
        super().clear()
        db = SessionLocal()
        try:
            table_name = getattr(self.orm_class, "__tablename__", None)
            if table_name:
                db.execute(text(f'TRUNCATE TABLE "{table_name}" CASCADE;'))
            else:
                db.query(self.orm_class).delete()
            db.commit()
        except Exception:
            db.rollback()
            try:
                db.query(self.orm_class).delete()
                db.commit()
            except Exception:
                db.rollback()
        finally:
            db.close()

    def append(self, item) -> None:
        super().append(item)
        db = SessionLocal()
        try:
            table_name = getattr(self.orm_class, "__tablename__", None)
            if table_name == "users" and isinstance(item, dict):
                from app.database.orm.user import UserORM
                from app.database.mappers.user_mapper import UserMapper, DEPT_MAP
                from app.models.user import User
                emp_id = item.get("employee_id") or item.get("user_id")
                hashed_pwd = item.get("password") or ""
                dept = item.get("department") or "Police"
                if emp_id:
                    DEPT_MAP[emp_id] = dept
                user_domain = User(
                    user_id=emp_id,
                    employee_id=emp_id,
                    name=item.get("name", "Admin"),
                    email=item.get("email", "admin@crime.gov.in"),
                    department=dept,
                    role=item.get("role"),
                    is_active=item.get("is_active", True),
                )
                orm_obj = UserMapper.to_orm(user_domain, hashed_password=hashed_pwd)
                db.merge(orm_obj)
                db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

    def __iter__(self):
        db = SessionLocal()
        try:
            table_name = getattr(self.orm_class, "__tablename__", None)
            if table_name == "users":
                from app.database.orm.user import UserORM
                from app.database.mappers.user_mapper import UserMapper
                stmt = select(UserORM)
                orm_list = db.scalars(stmt).all()
                res = []
                for o in orm_list:
                    u = UserMapper.to_domain(o).model_dump()
                    u["password"] = o.hashed_password
                    res.append(u)
                return iter(res)
            return super().__iter__()
        except Exception:
            return super().__iter__()
        finally:
            db.close()
