"""
ORM model for the 'complainantdetails' PostgreSQL table.
"""

from sqlalchemy import (
    Column, Integer, String, ForeignKey, Sequence,
)
from app.database.session import Base


class ComplainantDetailsORM(Base):
    __tablename__ = "complainantdetails"

    complainantid = Column(
        Integer,
        Sequence("complainantdetails_complainantid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    casemasterid = Column(
        Integer, ForeignKey("casemaster.casemasterid"), nullable=False,
    )
    complainantname = Column(String(150), nullable=False)
    ageyear = Column(Integer, nullable=True)
    occupationid = Column(Integer, nullable=True)
    religionid = Column(Integer, nullable=True)
    casteid = Column(Integer, nullable=True)
    genderid = Column(Integer, nullable=True)
