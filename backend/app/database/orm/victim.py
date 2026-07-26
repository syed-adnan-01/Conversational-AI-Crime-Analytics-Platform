"""
ORM model for the 'victim' PostgreSQL table.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Sequence,
)
from app.database.session import Base


class VictimORM(Base):
    __tablename__ = "victim"

    victimmasterid = Column(
        Integer,
        Sequence("victim_victimmasterid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    casemasterid = Column(
        Integer, ForeignKey("casemaster.casemasterid"), nullable=False,
    )
    victimname = Column(String(150), nullable=False)
    ageyear = Column(Integer, nullable=True)
    genderid = Column(Integer, nullable=True)
    victimpolice = Column(Boolean, nullable=True, default=False)
