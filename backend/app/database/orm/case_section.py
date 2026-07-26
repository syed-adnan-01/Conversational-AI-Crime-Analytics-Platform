"""
ORM model for the 'actsectionassociation' PostgreSQL table.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.session import Base


class ActSectionAssociationORM(Base):
    __tablename__ = "actsectionassociation"

    casemasterid = Column(Integer, ForeignKey("casemaster.casemasterid"), primary_key=True)
    actid = Column(String(20), ForeignKey("act.actcode"), primary_key=True)
    sectionid = Column(String(20), ForeignKey("section.sectioncode"), primary_key=True)
    actorderid = Column(Integer, nullable=True)
    sectionorderid = Column(Integer, nullable=True)
