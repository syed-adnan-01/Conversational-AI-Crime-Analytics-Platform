"""
ORM models for lookup and reference tables in PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Boolean, Date, Sequence
from app.database.session import Base


class EmployeeORM(Base):
    __tablename__ = "employee"

    employeeid = Column(
        Integer,
        Sequence("employee_employeeid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    districtid = Column(Integer, nullable=False, default=1)
    unitid = Column(Integer, nullable=False, default=1)
    rankid = Column(Integer, nullable=False, default=1)
    designationid = Column(Integer, nullable=False, default=1)
    kgid = Column(String(50), nullable=True, unique=True)
    firstname = Column(String(100), nullable=False)
    employeedob = Column(Date, nullable=True)
    genderid = Column(Integer, nullable=True)
    bloodgroupid = Column(Integer, nullable=True)
    physicallychallenged = Column(Boolean, default=False)
    appointmentdate = Column(Date, nullable=True)


class UnitORM(Base):
    __tablename__ = "unit"

    unitid = Column(Integer, primary_key=True)
    unitname = Column(String(100), nullable=True)
    unittypeid = Column(Integer, nullable=True, default=1)
    stateid = Column(Integer, nullable=True, default=1)
    districtid = Column(Integer, nullable=True, default=1)


class CourtORM(Base):
    __tablename__ = "court"

    courtid = Column(Integer, primary_key=True)
    courtname = Column(String(150), nullable=True)


class CaseCategoryORM(Base):
    __tablename__ = "casecategory"

    casecategoryid = Column(Integer, primary_key=True)
    lookupvalue = Column(String(100), nullable=False, default="General Crime")


class GravityOffenceORM(Base):
    __tablename__ = "gravityoffence"

    gravityoffenceid = Column(Integer, primary_key=True)
    lookupvalue = Column(String(100), nullable=False, default="Cognizable")


class CrimeHeadORM(Base):
    __tablename__ = "crimehead"

    crimeheadid = Column(Integer, primary_key=True)
    crimegroupname = Column(String(150), nullable=False, default="Theft")
    active = Column(Boolean, default=True)


class CrimeSubHeadORM(Base):
    __tablename__ = "crimesubhead"

    crimesubheadid = Column(Integer, primary_key=True)
    crimeheadid = Column(Integer, nullable=False, default=1)
    crimeheadname = Column(String(150), nullable=False, default="Vehicle Theft")


class CaseStatusMasterORM(Base):
    __tablename__ = "casestatusmaster"

    casestatusid = Column(Integer, primary_key=True)
    casestatusname = Column(String(100), nullable=False, default="Under Investigation")
