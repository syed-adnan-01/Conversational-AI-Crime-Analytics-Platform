"""
ORM model for the 'casemaster' PostgreSQL table.

Maps to the CaseMaster Pydantic domain model via the mapper layer.
Database uses integer PKs with sequences; domain uses string IDs.
"""

from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Numeric, Text,
    ForeignKey, Sequence,
)
from app.database.session import Base


class CaseMasterORM(Base):
    __tablename__ = "casemaster"

    casemasterid = Column(
        Integer,
        Sequence("casemaster_casemasterid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    crimeno = Column(String, nullable=False, unique=True)
    caseno = Column(String, nullable=False)
    crimeregistereddate = Column(Date, nullable=False)
    policepersonid = Column(
        Integer, ForeignKey("employee.employeeid"), nullable=False,
    )
    policestationid = Column(
        Integer, ForeignKey("unit.unitid"), nullable=False,
    )
    casecategoryid = Column(
        Integer, ForeignKey("casecategory.casecategoryid"), nullable=False,
    )
    gravityoffenceid = Column(
        Integer, ForeignKey("gravityoffence.gravityoffenceid"), nullable=False,
    )
    crimemajorheadid = Column(
        Integer, ForeignKey("crimehead.crimeheadid"), nullable=False,
    )
    crimeminorheadid = Column(
        Integer, ForeignKey("crimesubhead.crimesubheadid"), nullable=False,
    )
    casestatusid = Column(
        Integer, ForeignKey("casestatusmaster.casestatusid"), nullable=False,
    )
    courtid = Column(Integer, ForeignKey("court.courtid"), nullable=True)
    incidentfromdate = Column(DateTime, nullable=True)
    incidenttodate = Column(DateTime, nullable=True)
    inforeceivedpsdate = Column(DateTime, nullable=True)
    latitude = Column(Numeric, nullable=True)
    longitude = Column(Numeric, nullable=True)
    brieffacts = Column(Text, nullable=True)
