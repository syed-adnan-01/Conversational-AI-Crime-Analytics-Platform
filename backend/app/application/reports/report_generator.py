from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from app.application.analytics.service import AnalyticsService
from app.application.dashboard.service import DashboardService
from app.common.queries.officer_query import OfficerAssignmentQueryOptions
from app.models.case_master import CaseMaster
from app.repository.evidence_repository import EvidenceRepository
from app.repository.officer_repository import OfficerRepository
from app.repository.timeline_repository import TimelineRepository
from app.services.case_service import CaseService

from .report_mapper import (
    catalog_item,
    normalize_report_type,
    report_description,
    report_formats,
    report_id_for,
    report_title,
    report_type_from_id,
    supported_report_types,
)
from .report_models import ReportResponse, ReportSection, ReportType


def _dump(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [_dump(item) for item in value]
    return value


class ReportGenerator:
    def __init__(
        self,
        dashboard_service: DashboardService | None = None,
        analytics_service: AnalyticsService | None = None,
        case_service: type[CaseService] | None = None,
        evidence_repository: type[EvidenceRepository] | None = None,
        officer_repository: type[OfficerRepository] | None = None,
        timeline_repository: type[TimelineRepository] | None = None,
    ) -> None:
        self.dashboard_service = dashboard_service or DashboardService()
        self.analytics_service = analytics_service or AnalyticsService()
        self.case_service = case_service or CaseService
        self.evidence_repository = evidence_repository or EvidenceRepository
        self.officer_repository = officer_repository or OfficerRepository
        self.timeline_repository = timeline_repository or TimelineRepository
        self._cache: dict[str, ReportResponse] = {}

    def list_reports(self, generated_by: str = "system"):
        return [catalog_item(report_type, generated_by=generated_by) for report_type in supported_report_types()]

    def list_types(self):
        from .report_mapper import type_info

        return [type_info(report_type) for report_type in supported_report_types()]

    def get_report(self, report_id: str, generated_by: str = "system") -> ReportResponse:
        if report_id in self._cache:
            return self._cache[report_id]

        report_type, case_id = report_type_from_id(report_id)
        return self.generate(report_type=report_type, case_id=case_id, generated_by=generated_by)

    def generate(
        self,
        report_type: ReportType | str,
        case_id: Optional[str] = None,
        generated_by: str = "system",
    ) -> ReportResponse:
        normalized = normalize_report_type(report_type)
        report_id = report_id_for(normalized, case_id)
        created_at = datetime.now()

        if normalized == ReportType.CASE_SUMMARY:
            response = self._case_summary(report_id, normalized, created_at, generated_by, case_id)
        elif normalized == ReportType.INVESTIGATION_REPORT:
            response = self._investigation_report(report_id, normalized, created_at, generated_by, case_id)
        elif normalized == ReportType.EVIDENCE_REPORT:
            response = self._evidence_report(report_id, normalized, created_at, generated_by, case_id)
        elif normalized == ReportType.TIMELINE_REPORT:
            response = self._timeline_report(report_id, normalized, created_at, generated_by, case_id)
        elif normalized == ReportType.OFFICER_ACTIVITY_REPORT:
            response = self._officer_report(report_id, normalized, created_at, generated_by, case_id)
        elif normalized == ReportType.DASHBOARD_SUMMARY:
            response = self._dashboard_report(report_id, normalized, created_at, generated_by)
        else:
            response = self._analytics_report(report_id, normalized, created_at, generated_by)

        self._cache[report_id] = response
        return response

    def _empty_section(self, title: str, message: str) -> ReportSection:
        return ReportSection(title=title, items=[], todo=[message])

    def _get_case(self, case_id: Optional[str]) -> Optional[CaseMaster]:
        if not case_id:
            return None
        for case in self.case_service.get_all_cases():
            if case.case_master_id == case_id:
                return case
        return None

    def _case_summary(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
        case_id: Optional[str],
    ) -> ReportResponse:
        case = self._get_case(case_id)
        if case is None:
            return ReportResponse(
                report_id=report_id,
                title=report_title(report_type),
                description=report_description(report_type),
                report_type=report_type,
                created_at=created_at,
                generated_by=generated_by,
                export_formats=report_formats(report_type),
                summary={"todo": ["TODO: case_id was not provided or the case does not exist."]},
                sections=[self._empty_section("Case Summary", "TODO: no case data available."), self._empty_section("Evidence", "TODO: case evidence unavailable."), self._empty_section("Timeline", "TODO: case timeline unavailable.")],
                data={"case": None, "evidence": [], "timeline": [], "officers": []},
            )

        evidence = self.evidence_repository.get_case_evidence(case.case_master_id or "")
        timeline = self.timeline_repository.get_case_timeline(case.case_master_id or "")
        assignments = self.officer_repository.query_assignments(
            OfficerAssignmentQueryOptions(case_master_id=case.case_master_id or "")
        )[0]

        case_data = _dump(case)
        evidence_data = [_dump(item) for item in evidence]
        timeline_data = [_dump(item) for item in timeline]
        officer_data = [_dump(item) for item in assignments]

        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary={
                "case_master_id": case.case_master_id,
                "crime_no": case.crime_no,
                "evidence_count": len(evidence_data),
                "timeline_events": len(timeline_data),
                "officer_assignments": len(officer_data),
            },
            sections=[
                ReportSection(title="Case Summary", items=[case_data]),
                ReportSection(title="Evidence", items=evidence_data),
                ReportSection(title="Timeline", items=timeline_data),
                ReportSection(title="Officer Activity", items=officer_data),
            ],
            data={
                "case": case_data,
                "evidence": evidence_data,
                "timeline": timeline_data,
                "officers": officer_data,
            },
        )

    def _investigation_report(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
        case_id: Optional[str],
    ) -> ReportResponse:
        case = self._get_case(case_id)
        if case is None:
            return ReportResponse(
                report_id=report_id,
                title=report_title(report_type),
                description=report_description(report_type),
                report_type=report_type,
                created_at=created_at,
                generated_by=generated_by,
                export_formats=report_formats(report_type),
                summary={"todo": ["TODO: case_id was not provided or the case does not exist."]},
                sections=[self._empty_section("Investigation Report", "TODO: investigation data unavailable.")],
                data={"case": None, "evidence": [], "timeline": [], "officers": []},
            )

        evidence = self.evidence_repository.get_case_evidence(case.case_master_id or "")
        timeline = self.timeline_repository.get_case_timeline(case.case_master_id or "")
        assignments = self.officer_repository.query_assignments(
            OfficerAssignmentQueryOptions(case_master_id=case.case_master_id or "")
        )[0]

        case_data = _dump(case)
        evidence_data = [_dump(item) for item in evidence]
        timeline_data = [_dump(item) for item in timeline]
        officer_data = [_dump(item) for item in assignments]

        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary={
                "case_master_id": case.case_master_id,
                "crime_no": case.crime_no,
                "evidence_count": len(evidence_data),
                "timeline_events": len(timeline_data),
                "officer_assignments": len(officer_data),
            },
            sections=[
                ReportSection(title="Case Facts", items=[case_data]),
                ReportSection(title="Evidence Review", items=evidence_data),
                ReportSection(title="Chronology", items=timeline_data),
                ReportSection(title="Officers", items=officer_data),
            ],
            data={
                "case": case_data,
                "evidence": evidence_data,
                "timeline": timeline_data,
                "officers": officer_data,
            },
        )

    def _evidence_report(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
        case_id: Optional[str],
    ) -> ReportResponse:
        if case_id:
            evidence = self.evidence_repository.get_case_evidence(case_id)
            sections = [ReportSection(title="Evidence", items=[_dump(item) for item in evidence])]
            data = {"case_id": case_id, "evidence": [_dump(item) for item in evidence]}
            summary = {"case_id": case_id, "evidence_count": len(evidence)}
        else:
            all_cases = self.case_service.get_all_cases()
            grouped = []
            for case in all_cases:
                evidence = self.evidence_repository.get_case_evidence(case.case_master_id or "")
                grouped.append(
                    {
                        "case": _dump(case),
                        "evidence": [_dump(item) for item in evidence],
                    }
                )
            sections = [ReportSection(title="Evidence by Case", items=grouped)] if grouped else [self._empty_section("Evidence", "TODO: no evidence records available.")]
            data = {"cases": grouped}
            summary = {"case_count": len(grouped), "evidence_records": sum(len(item["evidence"]) for item in grouped)}

        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary=summary,
            sections=sections,
            data=data,
        )

    def _timeline_report(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
        case_id: Optional[str],
    ) -> ReportResponse:
        if case_id:
            events = self.timeline_repository.get_case_timeline(case_id)
            sections = [ReportSection(title="Timeline", items=[_dump(item) for item in events])]
            data = {"case_id": case_id, "timeline": [_dump(item) for item in events]}
            summary = {"case_id": case_id, "event_count": len(events)}
        else:
            all_cases = self.case_service.get_all_cases()
            grouped = []
            for case in all_cases:
                events = self.timeline_repository.get_case_timeline(case.case_master_id or "")
                grouped.append(
                    {
                        "case": _dump(case),
                        "timeline": [_dump(item) for item in events],
                    }
                )
            sections = [ReportSection(title="Timeline by Case", items=grouped)] if grouped else [self._empty_section("Timeline", "TODO: no timeline records available.")]
            data = {"cases": grouped}
            summary = {"case_count": len(grouped), "event_count": sum(len(item["timeline"]) for item in grouped)}

        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary=summary,
            sections=sections,
            data=data,
        )

    def _officer_report(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
        case_id: Optional[str],
    ) -> ReportResponse:
        officers = self.officer_repository.list_officers()
        officer_data = [_dump(item) for item in officers]
        if case_id:
            assignments = self.officer_repository.query_assignments(
                OfficerAssignmentQueryOptions(case_master_id=case_id)
            )[0]
            assignment_data = [_dump(item) for item in assignments]
            sections = [
                ReportSection(title="Officers", items=officer_data),
                ReportSection(title="Case Assignments", items=assignment_data),
            ]
            data = {"officers": officer_data, "assignments": assignment_data, "case_id": case_id}
            summary = {"officer_count": len(officer_data), "assignment_count": len(assignment_data)}
        else:
            assignments = self.officer_repository.query_assignments(OfficerAssignmentQueryOptions())[0]
            assignment_data = [_dump(item) for item in assignments]
            sections = [ReportSection(title="Officers", items=officer_data)]
            if assignment_data:
                sections.append(ReportSection(title="Assignments", items=assignment_data))
            data = {"officers": officer_data, "assignments": assignment_data}
            summary = {"officer_count": len(officer_data), "assignment_count": len(assignment_data)}

        if not officer_data:
            sections = [self._empty_section("Officers", "TODO: no officer records available.")]

        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary=summary,
            sections=sections,
            data=data,
        )

    def _dashboard_report(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
    ) -> ReportResponse:
        summary = self.dashboard_service.summary()
        recent_cases = self.dashboard_service.recent_cases()
        summary_data = _dump(summary)
        recent_case_data = [_dump(item) for item in recent_cases]
        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary=summary_data,
            sections=[
                ReportSection(title="Dashboard Summary", items=[summary_data]),
                ReportSection(title="Recent Cases", items=recent_case_data),
            ],
            data={"summary": summary_data, "recent_cases": recent_case_data},
        )

    def _analytics_report(
        self,
        report_id: str,
        report_type: ReportType,
        created_at: datetime,
        generated_by: str,
    ) -> ReportResponse:
        data = {
            "crime_types": self.analytics_service.crime_types(),
            "districts": self.analytics_service.districts(),
            "officers": self.analytics_service.officers(),
            "monthly": self.analytics_service.monthly(),
            "yearly": self.analytics_service.yearly(),
        }
        return ReportResponse(
            report_id=report_id,
            title=report_title(report_type),
            description=report_description(report_type),
            report_type=report_type,
            created_at=created_at,
            generated_by=generated_by,
            export_formats=report_formats(report_type),
            summary={"todo": []},
            sections=[
                ReportSection(title="Crime Types", items=[{"value": data["crime_types"]}]),
                ReportSection(title="Districts", items=[{"value": data["districts"]}]),
                ReportSection(title="Officers", items=[{"value": data["officers"]}]),
                ReportSection(title="Monthly Trend", items=data["monthly"]),
                ReportSection(title="Yearly Trend", items=data["yearly"]),
            ],
            data=data,
        )
