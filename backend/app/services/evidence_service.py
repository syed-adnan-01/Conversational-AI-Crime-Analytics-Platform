import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional
from fastapi import Depends

from app.core.logging import app_logger
from app.common.exceptions import (
    CaseNotFoundException,
    VictimNotFoundException,
    AccusedNotFoundException,
    SectionNotFoundException,
    EvidenceNotFoundException,
    DuplicateEvidenceException,
    InvalidDateRangeException,
)
from app.models.evidence import Evidence
from app.repository.case_repository import CaseRepository
from app.repository.victim_repository import VictimRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.section_repository import SectionRepository
from app.repository.act_repository import ActRepository
from app.repository.evidence_repository import EvidenceRepository
from app.common.queries.evidence_query import EvidenceQueryOptions
from app.schemas.evidence import (
    EvidenceCreate,
    EvidenceUpdate,
    EvidenceResponse,
    EvidenceSummary,
    EvidenceListResponse,
)
from app.schemas.complainant import PaginationMeta


# ==============================================================
# EVIDENCE PROCESSING HOOK INTERFACE
# ==============================================================

class EvidenceProcessingHook(ABC):
    """
    Interface for downstream processing of evidence (e.g. AI forensic scanning, file integrity hashing, indexing).
    """

    @abstractmethod
    def on_evidence_created(self, evidence: Evidence) -> None:
        """Invoked immediately after evidence has been created."""
        pass

    @abstractmethod
    def on_evidence_updated(self, evidence: Evidence) -> None:
        """Invoked immediately after evidence has been modified."""
        pass


class DefaultLoggingProcessingHook(EvidenceProcessingHook):
    """
    Default hook that logs activities.
    """

    def on_evidence_created(self, evidence: Evidence) -> None:
        app_logger.info(
            "[EvidenceHook] Pre-processing triggered for newly created Evidence. ID=%s | Type=%s",
            evidence.evidence_id,
            evidence.evidence_type.value,
        )

    def on_evidence_updated(self, evidence: Evidence) -> None:
        app_logger.info(
            "[EvidenceHook] Pre-processing triggered for modified Evidence. ID=%s | Status=%s",
            evidence.evidence_id,
            evidence.status.value,
        )


# ==============================================================
# EVIDENCE SERVICE
# ==============================================================

class EvidenceService:
    """
    Service layer handling core business rules for Evidence Management.
    """

    def __init__(
        self,
        case_repo: CaseRepository = Depends(lambda: CaseRepository),
        victim_repo: VictimRepository = Depends(lambda: VictimRepository),
        accused_repo: AccusedRepository = Depends(lambda: AccusedRepository),
        section_repo: SectionRepository = Depends(lambda: SectionRepository),
        act_repo: ActRepository = Depends(lambda: ActRepository),
        evidence_repo: EvidenceRepository = Depends(lambda: EvidenceRepository),
        hook: EvidenceProcessingHook = Depends(lambda: DefaultLoggingProcessingHook()),
    ):
        self.case_repo = case_repo
        self.victim_repo = victim_repo
        self.accused_repo = accused_repo
        self.section_repo = section_repo
        self.act_repo = act_repo
        self.evidence_repo = evidence_repo
        self.hook = hook

    # ----------------------------------------------------------
    # Helper to build detailed EvidenceResponse
    # ----------------------------------------------------------

    def _build_response(self, evidence: Evidence) -> EvidenceResponse:
        """
        Builds EvidenceResponse with de-normalized values for premium API consumption.
        """
        victim_name = None
        if evidence.victim_id:
            victim = self.victim_repo.get_victim_by_id(evidence.victim_id)
            victim_name = victim.name if victim else "Unknown"

        accused_name = None
        if evidence.accused_id:
            accused = self.accused_repo.get_accused_by_id(evidence.accused_id)
            accused_name = accused.name if accused else "Unknown"

        section_number = None
        act_short_name = None
        if evidence.section_id:
            section = self.section_repo.get_section_by_id(evidence.section_id)
            if section:
                section_number = section.section_number
                act = self.act_repo.get_act_by_id(section.act_id)
                act_short_name = act.short_name if act else "Unknown"

        return EvidenceResponse(
            evidence_id=evidence.evidence_id,
            case_master_id=evidence.case_master_id,
            evidence_number=evidence.evidence_number,
            title=evidence.title,
            description=evidence.description,
            evidence_type=evidence.evidence_type,
            evidence_category=evidence.evidence_category,
            status=evidence.status,
            custody_status=evidence.custody_status,
            collected_by=evidence.collected_by,
            collection_date=evidence.collection_date,
            collection_location=evidence.collection_location,
            storage_location=evidence.storage_location,
            storage_key=evidence.storage_key,
            mime_type=evidence.mime_type,
            file_size=evidence.file_size,
            checksum=evidence.checksum,
            checksum_algorithm=evidence.checksum_algorithm,
            remarks=evidence.remarks,
            victim_id=evidence.victim_id,
            accused_id=evidence.accused_id,
            section_id=evidence.section_id,
            victim_name=victim_name,
            accused_name=accused_name,
            section_number=section_number,
            act_short_name=act_short_name,
            created_at=evidence.created_at,
            updated_at=evidence.updated_at,
        )

    # ----------------------------------------------------------
    # Register / Link Evidence under Case
    # ----------------------------------------------------------

    def create_evidence(
        self, case_id: str, schema: EvidenceCreate
    ) -> EvidenceResponse:
        """
        Registers a new Evidence item under a case.
        Validates case, victim, accused, section existence.
        Generates evidence numbers, prefixes IDs, checks future collection_date.
        """
        # 1. Validate Case presence
        case = self.case_repo.get_case_by_id(case_id)
        if case is None:
            raise CaseNotFoundException(case_id)

        # 2. Check collection date (cannot be in the future)
        if schema.collection_date > datetime.now():
            raise InvalidDateRangeException("Collection date cannot be in the future.")

        # 3. Validate optional references
        if schema.victim_id:
            victim = self.victim_repo.get_victim_by_id(schema.victim_id)
            if victim is None or victim.case_master_id != case_id:
                raise VictimNotFoundException(schema.victim_id)

        if schema.accused_id:
            accused = self.accused_repo.get_accused_by_id(schema.accused_id)
            if accused is None or accused.case_master_id != case_id:
                raise AccusedNotFoundException(schema.accused_id)

        if schema.section_id:
            section = self.section_repo.get_section_by_id(schema.section_id)
            if section is None:
                raise SectionNotFoundException(schema.section_id)

        # 4. Resolve/Generate Evidence Number
        evidence_no = schema.evidence_number
        if not evidence_no or not evidence_no.strip():
            evidence_no = f"EVN-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
        else:
            evidence_no = evidence_no.strip()
            # Uniqueness check: check duplicate evidence_number within case
            existing = [
                e
                for e in self.evidence_repo.get_case_evidence(case_id)
                if e.evidence_number.lower() == evidence_no.lower()
            ]
            if existing:
                raise DuplicateEvidenceException(evidence_no, case_id)

        # 5. Populate and Create
        evidence_id = f"EV-{uuid.uuid4().hex[:12].upper()}"
        evidence = Evidence(
            evidence_id=evidence_id,
            case_master_id=case_id,
            evidence_number=evidence_no,
            title=schema.title.strip(),
            description=schema.description.strip(),
            evidence_type=schema.evidence_type,
            evidence_category=schema.evidence_category,
            status=schema.status,
            custody_status=schema.custody_status,
            collected_by=schema.collected_by.strip(),
            collection_date=schema.collection_date,
            collection_location=schema.collection_location.strip(),
            storage_location=schema.storage_location.strip(),
            storage_key=schema.storage_key,
            mime_type=schema.mime_type,
            file_size=schema.file_size,
            checksum=schema.checksum,
            checksum_algorithm=schema.checksum_algorithm,
            remarks=schema.remarks,
            victim_id=schema.victim_id,
            accused_id=schema.accused_id,
            section_id=schema.section_id,
        )

        stored = self.evidence_repo.create_evidence(evidence)

        # Call downstream hooks
        try:
            self.hook.on_evidence_created(stored)
        except Exception as e:
            app_logger.error("Failed to run post-create hook: %s", str(e))

        return self._build_response(stored)

    # ----------------------------------------------------------
    # Retrieve Evidence
    # ----------------------------------------------------------

    def get_evidence_by_id(self, evidence_id: str) -> EvidenceResponse:
        """
        Retrieves a single evidence record by ID.
        """
        evidence = self.evidence_repo.get_evidence_by_id(evidence_id)
        if evidence is None:
            raise EvidenceNotFoundException(evidence_id)

        return self._build_response(evidence)

    # ----------------------------------------------------------
    # Update Evidence
    # ----------------------------------------------------------

    def update_evidence(
        self, evidence_id: str, schema: EvidenceUpdate
    ) -> EvidenceResponse:
        """
        Replaces/updates an existing evidence record.
        Validates updated referenced entity keys.
        """
        existing = self.evidence_repo.get_evidence_by_id(evidence_id)
        if existing is None:
            raise EvidenceNotFoundException(evidence_id)

        case_id = existing.case_master_id

        # Validate updating references
        updated_victim_id = existing.victim_id
        if schema.victim_id is not None:
            if schema.victim_id != "":
                victim = self.victim_repo.get_victim_by_id(schema.victim_id)
                if victim is None or victim.case_master_id != case_id:
                    raise VictimNotFoundException(schema.victim_id)
                updated_victim_id = schema.victim_id
            else:
                updated_victim_id = None

        updated_accused_id = existing.accused_id
        if schema.accused_id is not None:
            if schema.accused_id != "":
                accused = self.accused_repo.get_accused_by_id(schema.accused_id)
                if accused is None or accused.case_master_id != case_id:
                    raise AccusedNotFoundException(schema.accused_id)
                updated_accused_id = schema.accused_id
            else:
                updated_accused_id = None

        updated_section_id = existing.section_id
        if schema.section_id is not None:
            if schema.section_id != "":
                section = self.section_repo.get_section_by_id(schema.section_id)
                if section is None:
                    raise SectionNotFoundException(schema.section_id)
                updated_section_id = schema.section_id
            else:
                updated_section_id = None

        # Verify collection date
        updated_collection_date = existing.collection_date
        if schema.collection_date is not None:
            if schema.collection_date > datetime.now():
                raise InvalidDateRangeException("Collection date cannot be in the future.")
            updated_collection_date = schema.collection_date

        # Update remaining attributes
        updated_fields = {
            "victim_id": updated_victim_id,
            "accused_id": updated_accused_id,
            "section_id": updated_section_id,
            "collection_date": updated_collection_date,
        }

        for attr in [
            "title",
            "description",
            "evidence_type",
            "evidence_category",
            "status",
            "custody_status",
            "collected_by",
            "collection_location",
            "storage_location",
            "storage_key",
            "mime_type",
            "file_size",
            "checksum",
            "checksum_algorithm",
            "remarks",
        ]:
            val = getattr(schema, attr)
            if val is not None:
                updated_fields[attr] = val

        updated_obj = existing.model_copy(update=updated_fields)
        stored = self.evidence_repo.update_evidence(updated_obj)

        # Call downstream hooks
        try:
            self.hook.on_evidence_updated(stored)
        except Exception as e:
            app_logger.error("Failed to run post-update hook: %s", str(e))

        return self._build_response(stored)

    # ----------------------------------------------------------
    # Delete Evidence
    # ----------------------------------------------------------

    def delete_evidence(self, evidence_id: str) -> None:
        """
        Deletes a specific evidence record.
        """
        existing = self.evidence_repo.get_evidence_by_id(evidence_id)
        if existing is None:
            raise EvidenceNotFoundException(evidence_id)

        self.evidence_repo.delete_evidence(evidence_id)

    # ----------------------------------------------------------
    # Search Evidence
    # ----------------------------------------------------------

    def search_evidence(
        self, options: EvidenceQueryOptions
    ) -> EvidenceListResponse:
        """
        Queries and lists evidence records with pagination.
        """
        records, total = self.evidence_repo.query_evidence(options)
        summaries = []
        for r in records:
            summaries.append(
                EvidenceSummary(
                    evidence_id=r.evidence_id,
                    case_master_id=r.case_master_id,
                    evidence_number=r.evidence_number,
                    title=r.title,
                    evidence_type=r.evidence_type,
                    evidence_category=r.evidence_category,
                    status=r.status,
                    custody_status=r.custody_status,
                    collected_by=r.collected_by,
                    collection_date=r.collection_date,
                )
            )

        meta = PaginationMeta.calculate(
            total=total, page=options.page, page_size=options.page_size
        )
        return EvidenceListResponse(items=summaries, pagination=meta)
