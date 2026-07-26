"""
ORM model for the 'accused' PostgreSQL table.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey, Sequence,
)
from app.database.session import Base


class AccusedORM(Base):
    __tablename__ = "accused"

    accusedmasterid = Column(
        Integer,
        Sequence("accused_accusedmasterid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    casemasterid = Column(
        Integer, ForeignKey("casemaster.casemasterid"), nullable=False,
    )
    accusedname = Column(String(150), nullable=False)
    ageyear = Column(Integer, nullable=True)
    genderid = Column(Integer, nullable=True)
    personid = Column(String(20), nullable=True)
