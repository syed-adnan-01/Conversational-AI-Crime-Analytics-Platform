"""
ORM model for the 'evidence' PostgreSQL table.
"""

from sqlalchemy import Column, String, Text, DateTime
from app.database.session import Base


class EvidenceORM(Base):
    __tablename__ = "evidence"

    evidence_id = Column(String(50), primary_key=True)
    case_master_id = Column(String(50), nullable=False)
    evidence_number = Column(String(100), nullable=False)
    evidence_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    collected_date = Column(DateTime, nullable=True)
    collected_by = Column(String(100), nullable=True)
    storage_location = Column(String(200), nullable=True)
