"""
ORM model for the 'court_proceeding' PostgreSQL table.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text
from app.database.session import Base


class CourtProceedingORM(Base):
    __tablename__ = "court_proceeding"

    proceeding_id = Column(String(50), primary_key=True)
    case_master_id = Column(String(50), nullable=False)
    court_id = Column(Integer, nullable=True)
    hearing_date = Column(DateTime, nullable=True)
    stage = Column(String(100), nullable=True)
    judge_name = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
