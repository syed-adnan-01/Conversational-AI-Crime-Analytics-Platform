from app.core.exceptions import CrimeSphereException


class CaseNotFoundException(CrimeSphereException):
    """Raised when a requested case does not exist."""

    def __init__(self, case_id: str):
        super().__init__(
            message=f"Case not found: {case_id}",
            status_code=404,
        )


class DuplicateCrimeNumberException(CrimeSphereException):
    """Raised when a crime number already exists in the system."""

    def __init__(self, crime_no: str):
        super().__init__(
            message=f"Crime number already exists: {crime_no}",
            status_code=409,
        )


class DuplicateCaseNumberException(CrimeSphereException):
    """Raised when a case number already exists in the system."""

    def __init__(self, case_no: str):
        super().__init__(
            message=f"Case number already exists: {case_no}",
            status_code=409,
        )


class InvalidDateRangeException(CrimeSphereException):
    """Raised when date fields are logically inconsistent."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=422,
        )


class ComplainantNotFoundException(CrimeSphereException):
    """Raised when a requested complainant does not exist."""

    def __init__(self, complainant_id: str):
        super().__init__(
            message=f"Complainant not found: {complainant_id}",
            status_code=404,
        )


class DuplicateComplainantException(CrimeSphereException):
    """Raised when a complainant already exists for a case."""

    def __init__(self, name: str, case_id: str):
        super().__init__(
            message=f"Complainant '{name}' is already registered for case: {case_id}",
            status_code=409,
        )


class VictimNotFoundException(CrimeSphereException):
    """Raised when a requested victim does not exist."""

    def __init__(self, victim_id: str):
        super().__init__(
            message=f"Victim not found: {victim_id}",
            status_code=404,
        )


class DuplicateVictimException(CrimeSphereException):
    """Raised when a victim already exists for a case."""

    def __init__(self, name: str, case_id: str):
        super().__init__(
            message=f"Victim '{name}' is already registered for case: {case_id}",
            status_code=409,
        )


class AccusedNotFoundException(CrimeSphereException):
    """Raised when a requested accused does not exist."""

    def __init__(self, accused_id: str):
        super().__init__(
            message=f"Accused not found: {accused_id}",
            status_code=404,
        )


class DuplicateAccusedException(CrimeSphereException):
    """Raised when an accused already exists for a case."""

    def __init__(self, name: str, case_id: str):
        super().__init__(
            message=f"Accused '{name}' is already registered for case: {case_id}",
            status_code=409,
        )


class ActNotFoundException(CrimeSphereException):
    """Raised when a requested act does not exist."""

    def __init__(self, act_id: str):
        super().__init__(
            message=f"Act not found: {act_id}",
            status_code=404,
        )


class SectionNotFoundException(CrimeSphereException):
    """Raised when a requested section does not exist."""

    def __init__(self, section_id: str):
        super().__init__(
            message=f"Section not found: {section_id}",
            status_code=404,
        )


class DuplicateActException(CrimeSphereException):
    """Raised when an act with same short name and year already exists."""

    def __init__(self, short_name: str, year: int):
        super().__init__(
            message=f"Act '{short_name}' ({year}) is already registered.",
            status_code=409,
        )


class DuplicateSectionException(CrimeSphereException):
    """Raised when a section with same number already exists within an act."""

    def __init__(self, section_number: str, act_id: str):
        super().__init__(
            message=f"Section '{section_number}' is already registered for Act: {act_id}",
            status_code=409,
        )


class DuplicateCaseSectionException(CrimeSphereException):
    """Raised when a section is already linked to a case."""

    def __init__(self, section_id: str, case_id: str):
        super().__init__(
            message=f"Section '{section_id}' is already assigned to case: {case_id}",
            status_code=409,
        )


class CaseSectionNotFoundException(CrimeSphereException):
    """Raised when a case section association does not exist."""

    def __init__(self, association_id: str):
        super().__init__(
            message=f"Case section association not found: {association_id}",
            status_code=404,
        )


class EvidenceNotFoundException(CrimeSphereException):
    """Raised when a requested evidence record does not exist."""

    def __init__(self, evidence_id: str):
        super().__init__(
            message=f"Evidence not found: {evidence_id}",
            status_code=404,
        )


class DuplicateEvidenceException(CrimeSphereException):
    """Raised when an evidence number already exists within a case."""

    def __init__(self, evidence_number: str, case_id: str):
        super().__init__(
            message=f"Evidence number '{evidence_number}' is already registered for case: {case_id}",
            status_code=409,
        )
