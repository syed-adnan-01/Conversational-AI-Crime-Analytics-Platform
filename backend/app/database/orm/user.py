"""
ORM model for the 'users' PostgreSQL table.
"""

from sqlalchemy import Column, String, Boolean
from app.database.session import Base


class UserORM(Base):
    __tablename__ = "users"

    employee_id = Column(String(50), primary_key=True)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    hashed_password = Column(String(255), nullable=True)
