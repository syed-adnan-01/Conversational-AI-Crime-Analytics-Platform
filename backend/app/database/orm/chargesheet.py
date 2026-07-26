"""
ORM model for the 'chargesheetdetails' PostgreSQL table.
"""

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Sequence
from app.database.session import Base


class ChargesheetDetailsORM(Base):
    __tablename__ = "chargesheetdetails"

    csid = Column(
        Integer,
        Sequence("chargesheetdetails_csid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    casemasterid = Column(Integer, ForeignKey("casemaster.casemasterid"), nullable=False)
    csdate = Column(DateTime, nullable=True)
    cstype = Column(String(1), nullable=True)
    policepersonid = Column(Integer, nullable=True)
