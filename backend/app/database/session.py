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

db_url = settings.DATABASE_URL
_using_sqlite_fallback = False
if not db_url:
    logger.warning("DATABASE_URL is empty! Falling back to in-memory SQLite to prevent startup crash.")
    db_url = "sqlite:///:memory:"
    _using_sqlite_fallback = True

engine_kwargs = {}
if not db_url.startswith("sqlite"):
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_engine(
    db_url,
    **engine_kwargs
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

            INSERT INTO unit (unitid, unitname, unittypeid, stateid, districtid) VALUES (1, 'Central Station', 1, 1, 1), (101, 'Indiranagar PS', 1, 1, 1)
            ON CONFLICT (unitid) DO NOTHING;

            INSERT INTO casecategory (casecategoryid, lookupvalue) VALUES (1, 'General Crime')
            ON CONFLICT (casecategoryid) DO NOTHING;

            INSERT INTO gravityoffence(gravityoffenceid, lookupvalue) VALUES (1, 'Cognizable')
            ON CONFLICT (gravityoffenceid) DO NOTHING;

            INSERT INTO crimehead (crimeheadid, crimegroupname) VALUES (1, 'Theft')
            ON CONFLICT (crimeheadid) DO NOTHING;

            INSERT INTO crimesubhead (crimesubheadid, crimeheadid, crimeheadname) VALUES (1, 1, 'Vehicle Theft')
            ON CONFLICT (crimesubheadid) DO NOTHING;

            INSERT INTO casestatusmaster (casestatusid, casestatusname) VALUES (1, 'Under Investigation')
            ON CONFLICT (casestatusid) DO NOTHING;

            INSERT INTO act (actcode, actdescription, shortname, active) VALUES ('BNS', 'Bharatiya Nyaya Sanhita', 'BNS 2023', true)
            ON CONFLICT (actcode) DO NOTHING;

            INSERT INTO section (sectioncode, actcode, sectiondescription, active) VALUES ('303', 'BNS', 'Theft', true)
            ON CONFLICT (sectioncode) DO NOTHING;
        """))
        conn.commit()


if not _using_sqlite_fallback:
    try:
        seed_reference_data()
    except Exception as e:
        logger.warning("Reference data seed note: %s", e)
else:
    logger.info("Skipping reference data seed — using SQLite fallback (no DATABASE_URL).")


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
