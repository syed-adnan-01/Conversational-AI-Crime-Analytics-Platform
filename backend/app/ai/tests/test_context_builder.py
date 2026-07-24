"""
============================================================
AI Context Builder Test Suite
============================================================

Module  : AI Context Builder
Purpose : Comprehensive tests for context building, metadata, summary,
          plugins, serializers, exceptions, and API endpoints.
"""

from datetime import datetime
import pytest
from fastapi.testclient import TestClient

from app.ai.context.context_builder import AIContextBuilder
from app.ai.context.context_models import DetailLevel, InvestigationContext
from app.ai.context.plugins.base import ContextPlugin
from app.ai.context.serializers import InvestigationContextSerializer
from app.ai.services.context_service import ContextService
from app.common.enums import Gender
from app.common.exceptions import CaseNotFoundException
from app.main import app
from app.models.accused import Accused
from app.models.arrest import Arrest
from app.models.case_master import CaseMaster
from app.models.case_section import CaseSectionAssociation
from app.models.chargesheet import Chargesheet
from app.models.complainant import Complainant
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.officer import OfficerAssignment
from app.models.section import Section
from app.models.timeline import TimelineEvent
from app.models.victim import Victim
from app.models.witness import Witness
from app.repository.accused_repository import AccusedRepository
from app.repository.arrest_repository import ArrestRepository
from app.repository.case_repository import CaseRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.chargesheet_repository import ChargesheetRepository
from app.repository.complainant_repository import ComplainantRepository
from app.repository.court_proceeding_repository import CourtProceedingRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.officer_repository import OfficerRepository
from app.repository.section_repository import SectionRepository
from app.repository.timeline_repository import TimelineRepository
from app.repository.victim_repository import VictimRepository
from app.repository.witness_repository import WitnessRepository


class DummyAnalyticsPlugin(ContextPlugin):
    """Test plugin to verify context enrichment mechanism."""
    def enrich(self, context: InvestigationContext) -> None:
        context.analytics = {"risk_score": 88, "pattern": "Cyber Fraud"}


def clear_all_repositories():
    """Reset repository in-memory stores before tests."""
    CaseRepository._cases.clear()
    ComplainantRepository._complainants.clear()
    VictimRepository._victims.clear()
    AccusedRepository._accused.clear()
    WitnessRepository._witnesses.clear()
    SectionRepository._sections.clear()
    CaseSectionRepository._associations.clear()
    EvidenceRepository._evidence_list.clear()
    ArrestRepository._arrests.clear()
    ChargesheetRepository._chargesheets.clear()
    CourtProceedingRepository._proceedings.clear()
    OfficerRepository._assignments.clear()
    TimelineRepository._events.clear()
    AIContextBuilder.clear_plugins()


def setup_sample_case_data() -> str:
    """Helper to populate full investigation data for a case and return case_id."""
    clear_all_repositories()

    now = datetime.now()

    # Case
    case = CaseMaster(
        crime_no="CR-2026-0088",
        case_no="CC-2026-101",
        crime_registered_date=now,
        police_station_id=1,
    )
    stored_case = CaseRepository.create_case(case)
    case_id = stored_case.case_master_id

    # Complainant
    comp = Complainant(
        complainant_id="COMP-001",
        case_master_id=case_id,
        name="John Doe",
        gender=Gender.MALE,
        age=35,
        mobile_no="9876543210",
        address="Bangalore",
    )
    ComplainantRepository.create_complainant(comp)

    # Victim
    victim = Victim(
        victim_id="VIC-001",
        case_master_id=case_id,
        name="Jane Doe",
        gender=Gender.FEMALE,
        age=32,
        condition="Recovered",
    )
    VictimRepository.create_victim(victim)

    # Accused
    accused = Accused(
        accused_id="ACC-001",
        case_master_id=case_id,
        name="Robert Smith",
        alias="Bob",
    )
    AccusedRepository.create_accused(accused)

    # Witness
    witness = Witness(
        witness_id="WIT-001",
        case_master_id=case_id,
        name="Alice Walker",
        gender=Gender.FEMALE,
        mobile_no="9123456789",
    )
    WitnessRepository.create_witness(witness)

    # Act & Section
    section = Section(
        section_id="SEC-420",
        act_id="ACT-IPC",
        section_number="420",
        title="Cheating and dishonestly inducing delivery of property",
    )
    SectionRepository.create_section(section)

    assoc = CaseSectionAssociation(
        association_id="CSA-001",
        case_master_id=case_id,
        section_id="SEC-420",
    )
    CaseSectionRepository.assign_section_to_case(assoc)

    # Evidence
    evidence = Evidence(
        evidence_id="EVI-001",
        case_master_id=case_id,
        evidence_number="E-01",
        title="Server Logs & Transaction Receipts",
        description="Encrypted server logs and transaction receipts",
        evidence_type="DIGITAL_DEVICE",
        status="COLLECTED",
        collected_by="OFF-001",
        collection_date=now,
        collection_location="Server Room",
        storage_location="Locker 4",
    )
    EvidenceRepository.create_evidence(evidence)

    # Arrest
    arrest = Arrest(
        arrest_id="ARR-001",
        case_master_id=case_id,
        accused_id="ACC-001",
        arrest_date=now,
        arrest_location="MG Road, Bangalore",
        grounds_for_arrest="Accused of cyber fraud under Sec 420",
        arresting_officer="OFF-001",
        status="ARRESTED",
    )
    ArrestRepository.create_arrest(arrest)

    # Chargesheet
    cs = Chargesheet(
        chargesheet_id="CS-001",
        case_master_id=case_id,
        chargesheet_number="CS-2026-01",
        filing_date=now,
        investigating_officer="OFF-001",
        summary="Investigation complete. Evidence gathered.",
        status="FILED",
    )
    ChargesheetRepository.create_chargesheet(cs)

    # Court Proceeding
    cp = CourtProceeding(
        proceeding_id="CP-001",
        case_master_id=case_id,
        court_name="City Civil Court",
        judge_name="Justice Sharma",
        hearing_date=now,
        stage="CHARGE_FRAMING",
        summary="Framing of charges under IPC 420",
    )
    CourtProceedingRepository.create_proceeding(cp)

    # Officer Assignment
    assign = OfficerAssignment(
        assignment_id="OAS-001",
        case_master_id=case_id,
        officer_id="OFF-001",
        role="Investigating Officer",
        assigned_date=now,
    )
    OfficerRepository.create_assignment(assign)

    # Timeline Event
    event = TimelineEvent(
        event_id="EVT-001",
        case_master_id=case_id,
        event_type="CASE_CREATED",
        title="FIR Registered",
        description="FIR officially registered at station",
        event_time=now,
    )
    TimelineRepository.create_event(event)

    return case_id


# ==============================================================
# Unit & Integration Tests
# ==============================================================

def test_build_context_success():
    """Verify building a complete investigation context with all sub-entities."""
    case_id = setup_sample_case_data()

    context = ContextService.build_context(case_id)

    assert context is not None
    assert context.case.case_master_id == case_id
    assert context.complainant is not None
    assert context.complainant.name == "John Doe"
    assert len(context.victims) == 1
    assert len(context.accused) == 1
    assert len(context.witnesses) == 1
    assert len(context.sections) == 1
    assert len(context.evidence) == 1
    assert len(context.arrests) == 1
    assert len(context.chargesheets) == 1
    assert len(context.court_proceedings) == 1
    assert len(context.officer_assignments) == 1
    assert len(context.timeline_events) == 1

    # Metadata & Readiness
    assert context.metadata.case_id == case_id
    assert context.metadata.context_version == "1.0.0"
    assert context.metadata.is_ai_ready is True
    assert context.metadata.total_entities == 11
    assert context.metadata.entity_counts["evidence"] == 1
    assert len(context.metadata.context_hash) == 64  # SHA-256 length


def test_build_context_missing_case():
    """Verify CaseNotFoundException is raised for non-existent case_id."""
    clear_all_repositories()
    with pytest.raises(CaseNotFoundException):
        ContextService.build_context("NON-EXISTENT-CASE-ID")


def test_build_context_empty_case():
    """Verify context assembly for an empty case with no sub-entities."""
    clear_all_repositories()
    case = CaseMaster(
        crime_no="CR-EMPTY-01",
        crime_registered_date=datetime.now(),
        police_station_id=1,
    )
    stored = CaseRepository.create_case(case)
    case_id = stored.case_master_id

    context = ContextService.build_context(case_id)

    assert context.case.case_master_id == case_id
    assert context.complainant is None
    assert len(context.victims) == 0
    assert len(context.accused) == 0
    assert len(context.evidence) == 0
    assert context.metadata.is_ai_ready is False
    assert context.metadata.total_entities == 0


def test_context_hash_fingerprint():
    """Verify context_hash stays identical for same state and changes on modification."""
    case_id = setup_sample_case_data()

    ctx1 = ContextService.build_context(case_id)
    hash1 = ctx1.metadata.context_hash

    ctx2 = ContextService.build_context(case_id)
    hash2 = ctx2.metadata.context_hash

    assert hash1 == hash2

    # Add a second evidence item
    new_evidence = Evidence(
        evidence_id="EVI-002",
        case_master_id=case_id,
        evidence_number="E-02",
        title="Hard Drive Dump",
        description="Physical HD dump",
        evidence_type="DIGITAL_DEVICE",
        status="COLLECTED",
        collected_by="OFF-001",
        collection_date=datetime.now(),
        collection_location="Office",
        storage_location="Locker 5",
    )
    EvidenceRepository.create_evidence(new_evidence)

    ctx3 = ContextService.build_context(case_id)
    hash3 = ctx3.metadata.context_hash

    assert hash1 != hash3


def test_plugin_enrichment():
    """Verify context plugin enrichment mechanism."""
    case_id = setup_sample_case_data()

    plugin = DummyAnalyticsPlugin()
    AIContextBuilder.register_plugin(plugin)

    context = ContextService.build_context(case_id)

    assert context.analytics is not None
    assert context.analytics["risk_score"] == 88
    assert context.analytics["pattern"] == "Cyber Fraud"

    AIContextBuilder.clear_plugins()


def test_serializers_and_detail_levels():
    """Verify JSON, Markdown, and Text serializers across detail levels."""
    case_id = setup_sample_case_data()

    context = ContextService.build_context(case_id)

    # JSON Serializer
    json_summary = InvestigationContextSerializer.to_json(context, level=DetailLevel.SUMMARY)
    assert '"summary"' in json_summary
    assert '"metadata"' in json_summary

    json_full = InvestigationContextSerializer.to_json(context, level=DetailLevel.STANDARD)
    assert '"case"' in json_full
    assert '"complainant"' in json_full

    # Markdown Serializer
    md_summary = InvestigationContextSerializer.to_markdown(context, level=DetailLevel.SUMMARY)
    assert "# INVESTIGATION CONTEXT REPORT" in md_summary
    assert "## CONTEXT SUMMARY & STATISTICS" in md_summary

    md_standard = InvestigationContextSerializer.to_markdown(context, level=DetailLevel.STANDARD)
    assert "## COMPLAINANT" in md_standard
    assert "## VICTIMS" in md_standard
    assert "## EVIDENCE REGISTERED" in md_standard

    # Text Serializer
    text_out = InvestigationContextSerializer.to_text(context, level=DetailLevel.STANDARD)
    assert "INVESTIGATION SUMMARY:" in text_out
    assert "COMPLAINANT:" in text_out
    assert "EVIDENCE:" in text_out


def test_api_endpoints():
    """Verify API routes for GET /ai/context/{case_id} and sub-routes."""
    clear_all_repositories()
    client = TestClient(app)

    with client as c:
        # 1. Authenticate user
        login_res = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Register a mock case
        case_payload = {
            "crime_no": "CR-API-2026",
            "crime_registered_date": "2026-07-20T12:00:00",
            "police_station_id": 101,
        }
        case_res = c.post("/cases/", json=case_payload, headers=headers)
        assert case_res.status_code == 201
        case_id = case_res.json()["case_master_id"]

        # 3. GET /ai/context/{case_id}/summary
        summary_res = c.get(f"/ai/context/{case_id}/summary", headers=headers)
        assert summary_res.status_code == 200
        assert summary_res.json()["case_title"] == "FIR No. CR-API-2026"

        # 4. GET /ai/context/{case_id}
        ctx_res = c.get(f"/ai/context/{case_id}", headers=headers)
        assert ctx_res.status_code == 200
        assert ctx_res.json()["case"]["case_master_id"] == case_id

        # 5. GET /ai/context/{case_id}/markdown
        md_res = c.get(f"/ai/context/{case_id}/markdown", headers=headers)
        assert md_res.status_code == 200
        assert "text/markdown" in md_res.headers["content-type"]
        assert "# INVESTIGATION CONTEXT REPORT" in md_res.text

        # 6. GET /ai/context/{case_id}/text
        text_res = c.get(f"/ai/context/{case_id}/text", headers=headers)
        assert text_res.status_code == 200
        assert "text/plain" in text_res.headers["content-type"]
        assert "INVESTIGATION SUMMARY:" in text_res.text

        # 7. Missing case 404
        missing_res = c.get("/ai/context/NON-EXISTENT-CASE", headers=headers)
        assert missing_res.status_code == 404
