import logging
from app.repository.case_repository import CaseRepository
from app.repository.complainant_repository import ComplainantRepository
from app.repository.user_repository import UserRepository
from app.repository.victim_repository import VictimRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.act_repository import ActRepository
from app.repository.section_repository import SectionRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.timeline_repository import TimelineRepository
from app.repository.witness_repository import WitnessRepository
from app.repository.arrest_repository import ArrestRepository
from app.repository.officer_repository import OfficerRepository
from app.repository.chargesheet_repository import ChargesheetRepository
from app.repository.court_proceeding_repository import CourtProceedingRepository

logger = logging.getLogger("crimesphere.startup")

repos = [
    ("User", UserRepository),
    ("Case", CaseRepository),
    ("Complainant", ComplainantRepository),
    ("Victim", VictimRepository),
    ("Accused", AccusedRepository),
    ("Act", ActRepository),
    ("Section", SectionRepository),
    ("CaseSection", CaseSectionRepository),
    ("Evidence", EvidenceRepository),
    ("Timeline", TimelineRepository),
    ("Witness", WitnessRepository),
    ("Arrest", ArrestRepository),
    ("Officer", OfficerRepository),
    ("Chargesheet", ChargesheetRepository),
    ("CourtProceeding", CourtProceedingRepository),
]


def initialize_application() -> None:
    """
    Initialize all application resources safely.
    """
    try:
        from app.database.session import _using_sqlite_fallback
        if _using_sqlite_fallback:
            logger.info("⚡ SQLite fallback active — skipping baseline repository database seeds.")
            return
    except Exception as exc:
        logger.warning("Could not check sqlite fallback state: %s", exc)

    for name, repo in repos:
        try:
            repo.initialize()
            logger.info("✅ %s repository initialized.", name)
        except Exception as e:
            logger.warning("⚠️ Could not initialize %s repository: %s", name, e)