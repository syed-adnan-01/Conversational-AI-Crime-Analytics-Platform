from datetime import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.reports.report_router import router as reports_router
from app.application.reports.report_models import ReportType
from app.application.reports.report_service import ReportService
from app.core.roles import UserRole
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.case_master import CaseMaster
from app.models.evidence import CustodyStatus, Evidence, EvidenceCategory, EvidenceStatus, EvidenceType
from app.models.timeline import TimelineEvent, TimelineEventType
from app.repository.case_repository import CaseRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.officer_repository import OfficerRepository
from app.repository.timeline_repository import TimelineRepository


def _reports_client() -> TestClient:
    reports_app = FastAPI()
    reports_app.include_router(reports_router, prefix="/reports")
    reports_app.dependency_overrides[get_current_user] = lambda: User(
        user_id="USR-TEST",
        employee_id="EMP001",
        name="Test Officer",
        email="test.officer@example.com",
        department="Cyber Crime",
        role=UserRole.ADMIN,
        is_active=True,
    )
    return TestClient(reports_app)


def _clear_repositories() -> None:
    CaseRepository._cases.clear()
    EvidenceRepository._evidence_list.clear()
    TimelineRepository._events.clear()
    OfficerRepository._assignments.clear()


def _seed_case(case_id: str = "CM-RPT-001") -> CaseMaster:
    case = CaseMaster(
        case_master_id=case_id,
        crime_no="CR-2026-RPT-001",
        crime_registered_date=datetime(2026, 7, 20, 10, 30),
        police_station_id=101,
        case_status_id=1,
        brief_facts="Report test case",
        police_person_id=1,
    )
    return CaseRepository.create_case(case)


def _seed_case_evidence(case_id: str) -> None:
    evidence = Evidence(
        case_master_id=case_id,
        evidence_number="EVN-RPT-001",
        title="Test Device",
        description="Synthetic evidence for report testing.",
        evidence_type=EvidenceType.DIGITAL_DEVICE,
        evidence_category=EvidenceCategory.DIGITAL,
        status=EvidenceStatus.COLLECTED,
        custody_status=CustodyStatus.IN_CUSTODY,
        collected_by="Inspector One",
        collection_date=datetime(2026, 7, 20, 11, 0),
        collection_location="Bengaluru",
        storage_location="Locker 1",
    )
    EvidenceRepository.create_evidence(evidence)


def _seed_case_timeline(case_id: str) -> None:
    event = TimelineEvent(
        case_master_id=case_id,
        event_type=TimelineEventType.CASE_CREATED,
        title="Case Created",
        description="Synthetic timeline event for report testing.",
        reference_id=case_id,
        reference_type="CaseMaster",
        event_time=datetime(2026, 7, 20, 10, 30),
    )
    TimelineRepository.create_event(event)


def test_report_service_reuses_application_services():
    called = {"dashboard": False, "analytics": False, "cases": False}

    class FakeDashboardService:
        def summary(self):
            called["dashboard"] = True
            return {"total_cases": 1}

        def recent_cases(self):
            return []

    class FakeAnalyticsService:
        def crime_types(self):
            called["analytics"] = True
            return {"THEFT": 1}

        def districts(self):
            return {}

        def officers(self):
            return {}

        def monthly(self):
            return []

        def yearly(self):
            return []

    class FakeCaseService:
        @staticmethod
        def get_all_cases():
            called["cases"] = True
            return []

    service = ReportService()
    service.generator.dashboard_service = FakeDashboardService()
    service.generator.analytics_service = FakeAnalyticsService()
    service.generator.case_service = FakeCaseService

    case_report = service.generate_report(ReportType.CASE_SUMMARY, case_id="CASE-001")
    dashboard_report = service.generate_report(ReportType.DASHBOARD_SUMMARY)
    analytics_report = service.generate_report(ReportType.ANALYTICS_SUMMARY)

    assert called["dashboard"] is True
    assert called["analytics"] is True
    assert called["cases"] is True
    assert case_report.report_type == ReportType.CASE_SUMMARY
    assert dashboard_report.report_type == ReportType.DASHBOARD_SUMMARY
    assert analytics_report.report_type == ReportType.ANALYTICS_SUMMARY


def test_reports_generation_and_export_endpoints():
    client = _reports_client()
    with client as c:
        _clear_repositories()
        case = _seed_case()
        _seed_case_evidence(case.case_master_id or "")
        _seed_case_timeline(case.case_master_id or "")

        response = c.post(
            "/reports/generate",
            json={"report_type": "Case Summary", "case_id": case.case_master_id},
        )
        assert response.status_code == 200
        report = response.json()
        assert report["report_type"] == "Case Summary"
        assert report["summary"]["evidence_count"] == 1
        assert report["summary"]["timeline_events"] == 1

        export_json = c.get(f"/reports/{report['report_id']}/export?format=JSON")
        assert export_json.status_code == 200
        export_payload = export_json.json()
        assert export_payload["status"] == "ready"
        assert export_payload["format"] == "JSON"
        assert export_payload["download_url"]

        export_csv = c.get(f"/reports/{report['report_id']}/export?format=CSV")
        assert export_csv.status_code == 200
        assert export_csv.json()["status"] == "ready"

        export_pdf = c.get(f"/reports/{report['report_id']}/export?format=PDF")
        assert export_pdf.status_code == 200
        assert export_pdf.json()["status"] == "not_implemented"


def test_reports_empty_state_and_metadata():
    client = _reports_client()
    with client as c:
        _clear_repositories()

        catalog = c.get("/reports")
        assert catalog.status_code == 200
        assert catalog.json()["total"] >= 7

        report_types = c.get("/reports/types")
        assert report_types.status_code == 200
        assert report_types.json()["total"] >= 7

        health = c.get("/reports/health")
        assert health.status_code == 200
        assert health.json()["report_engine_status"] == "ready"
        assert health.json()["export_capability"]["PDF"] is False

        report = c.get("/reports/case-summary")
        assert report.status_code == 200
        payload = report.json()
        assert payload["report_type"] == "Case Summary"
        assert payload["sections"][0]["todo"]
