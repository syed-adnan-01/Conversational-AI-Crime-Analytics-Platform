"""
ORM model for the 'act' PostgreSQL table.
"""

from sqlalchemy import Column, String, Boolean
from app.database.session import Base


class ActORM(Base):
    __tablename__ = "act"

    actcode = Column(String(20), primary_key=True)
    actdescription = Column(String(255), nullable=True)
    shortname = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
