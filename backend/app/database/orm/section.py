"""
ORM model for the 'section' PostgreSQL table.
"""

from sqlalchemy import Column, String, Boolean, ForeignKey
from app.database.session import Base


class SectionORM(Base):
    __tablename__ = "section"

    sectioncode = Column(String(20), primary_key=True)
    actcode = Column(String(20), ForeignKey("act.actcode"), nullable=False)
    sectiondescription = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)
