"""
ORM model for the 'case_timeline' PostgreSQL table.
"""

from sqlalchemy import Column, String, DateTime, Text
from app.database.session import Base


class CaseTimelineORM(Base):
    __tablename__ = "case_timeline"

    timeline_id = Column(String(50), primary_key=True)
    case_master_id = Column(String(50), nullable=False)
    event_name = Column(String(150), nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    description = Column(Text, nullable=True)
    actor_id = Column(String(50), nullable=True)
