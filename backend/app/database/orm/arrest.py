"""
ORM model for the 'arrestsurrender' PostgreSQL table.
"""

from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey, Sequence
from app.database.session import Base


class ArrestSurrenderORM(Base):
    __tablename__ = "arrestsurrender"

    arrestsurrenderid = Column(
        Integer,
        Sequence("arrestsurrender_arrestsurrenderid_seq"),
        primary_key=True,
        autoincrement=True,
    )
    casemasterid = Column(Integer, ForeignKey("casemaster.casemasterid"), nullable=False)
    arrestsurrendertypeid = Column(Integer, nullable=True)
    arrestsurrenderdate = Column(Date, nullable=True)
    arrestsurrenderstateid = Column(Integer, nullable=True)
    arrestsurrenderdistrictid = Column(Integer, nullable=True)
    policestationid = Column(Integer, nullable=True)
    ioid = Column(Integer, nullable=True)
    courtid = Column(Integer, nullable=True)
    accusedmasterid = Column(Integer, ForeignKey("accused.accusedmasterid"), nullable=True)
    isaccused = Column(Boolean, default=True)
    iscomplainantaccused = Column(Boolean, default=False)
