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


def initialize_application() -> None:
    """
    Initialize all application resources.
    """

    UserRepository.initialize()
    print("✅ User repository initialized.")

    CaseRepository.initialize()
    print("✅ Case repository initialized.")

    ComplainantRepository.initialize()
    print("✅ Complainant repository initialized.")

    VictimRepository.initialize()
    print("✅ Victim repository initialized.")

    AccusedRepository.initialize()
    print("✅ Accused repository initialized.")

    ActRepository.initialize()
    print("✅ Act repository initialized.")

    SectionRepository.initialize()
    print("✅ Section repository initialized.")

    CaseSectionRepository.initialize()
    print("✅ CaseSection repository initialized.")

    EvidenceRepository.initialize()
    print("✅ Evidence repository initialized.")

    TimelineRepository.initialize()
    print("✅ Timeline repository initialized.")

    WitnessRepository.initialize()
    print("✅ Witness repository initialized.")

    ArrestRepository.initialize()
    print("✅ Arrest repository initialized.")

    OfficerRepository.initialize()
    print("✅ Officer repository initialized.")

    ChargesheetRepository.initialize()
    print("✅ Chargesheet repository initialized.")

    CourtProceedingRepository.initialize()
    print("✅ CourtProceeding repository initialized.")