"""
============================================================
SQLAlchemy Database Session & Engine Configuration
============================================================
"""

from typing import Generator
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

logger = logging.getLogger("crimesphere.database")

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def seed_reference_data():
    """Seed baseline foreign key rows if table is empty or missing defaults."""
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO employee (employeeid, districtid, unitid, rankid, designationid, firstname)
            VALUES (1, 1, 1, 1, 1, 'Default Officer')
            ON CONFLICT (employeeid) DO NOTHING;

            INSERT INTO unit (unitid, unitname, unittypeid) VALUES (1, 'Central Station', 1), (101, 'Indiranagar PS', 1)
            ON CONFLICT (unitid) DO NOTHING;

            INSERT INTO casecategory (casecategoryid, categoryname) VALUES (1, 'General Crime')
            ON CONFLICT (casecategoryid) DO NOTHING;

            INSERT INTO gravityoffence(gravityoffenceid, gravityname) VALUES (1, 'Cognizable')
            ON CONFLICT (gravityoffenceid) DO NOTHING;

            INSERT INTO crimehead (crimeheadid, headname) VALUES (1, 'Theft')
            ON CONFLICT (crimeheadid) DO NOTHING;

            INSERT INTO crimesubhead (crimesubheadid, subheadname) VALUES (1, 'Vehicle Theft')
            ON CONFLICT (crimesubheadid) DO NOTHING;

            INSERT INTO casestatusmaster (casestatusid, statusname) VALUES (1, 'Under Investigation')
            ON CONFLICT (casestatusid) DO NOTHING;

            INSERT INTO act (actcode, actdescription, shortname, active) VALUES ('BNS', 'Bharatiya Nyaya Sanhita', 'BNS 2023', true)
            ON CONFLICT (actcode) DO NOTHING;

            INSERT INTO section (sectioncode, actcode, sectiondescription, active) VALUES ('303', 'BNS', 'Theft', true)
            ON CONFLICT (sectioncode) DO NOTHING;
        """))
        conn.commit()


try:
    seed_reference_data()
except Exception as e:
    logger.warning("Reference data seed note: %s", e)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_database() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database ping successful.")
        return True
    except Exception as exc:
        logger.error("Database ping failed: %s", exc)
        return False
