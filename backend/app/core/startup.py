from app.repository.case_repository import CaseRepository
from app.repository.complainant_repository import ComplainantRepository
from app.repository.user_repository import UserRepository
from app.repository.victim_repository import VictimRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.act_repository import ActRepository
from app.repository.section_repository import SectionRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.evidence_repository import EvidenceRepository


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