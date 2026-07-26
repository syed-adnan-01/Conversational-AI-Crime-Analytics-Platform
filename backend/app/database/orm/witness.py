"""
ORM model for the 'witness' PostgreSQL table.
"""

from sqlalchemy import Column, String, Text
from app.database.session import Base


class WitnessORM(Base):
    __tablename__ = "witness"

    witness_id = Column(String(50), primary_key=True)
    case_master_id = Column(String(50), nullable=False)
    witness_name = Column(String(150), nullable=False)
    witness_type = Column(String(100), nullable=True)
    statement_summary = Column(Text, nullable=True)
    contact_number = Column(String(20), nullable=True)
