from __future__ import annotations

from datetime import datetime
from typing import Optional

from .report_models import (
    ReportCatalogItem,
    ReportFormat,
    ReportType,
    ReportTypeInfo,
)


REPORT_DEFINITIONS = {
    ReportType.CASE_SUMMARY: {
        "report_id": "case-summary",
        "title": "Case Summary",
        "description": "Concise summary of case facts and status.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV],
    },
    ReportType.INVESTIGATION_REPORT: {
        "report_id": "investigation-report",
        "title": "Investigation Report",
        "description": "Structured investigation report built from current case data.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV],
    },
    ReportType.EVIDENCE_REPORT: {
        "report_id": "evidence-report",
        "title": "Evidence Report",
        "description": "Evidence inventory grouped from repository-backed case data.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV],
    },
    ReportType.TIMELINE_REPORT: {
        "report_id": "timeline-report",
        "title": "Timeline Report",
        "description": "Chronological report derived from case timelines.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV],
    },
    ReportType.OFFICER_ACTIVITY_REPORT: {
        "report_id": "officer-activity-report",
        "title": "Officer Activity Report",
        "description": "Officer list and current assignment snapshot.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV],
    },
    ReportType.DASHBOARD_SUMMARY: {
        "report_id": "dashboard-summary",
        "title": "Dashboard Summary",
        "description": "Operational summary from the dashboard application service.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV, ReportFormat.PDF],
    },
    ReportType.ANALYTICS_SUMMARY: {
        "report_id": "analytics-summary",
        "title": "Analytics Summary",
        "description": "Case analytics snapshot from the analytics application service.",
        "export_formats": [ReportFormat.JSON, ReportFormat.CSV, ReportFormat.PDF],
    },
}


def normalize_report_type(value: ReportType | str) -> ReportType:
    if isinstance(value, ReportType):
        return value
    for report_type, definition in REPORT_DEFINITIONS.items():
        if value == report_type.value or value == definition["report_id"]:
            return report_type
    raise ValueError(f"Unsupported report type: {value}")


def report_definition(report_type: ReportType | str) -> dict:
    return REPORT_DEFINITIONS[normalize_report_type(report_type)]


def report_id_for(report_type: ReportType | str, case_id: Optional[str] = None) -> str:
    definition = report_definition(report_type)
    if case_id:
        return f"{definition['report_id']}-{case_id}"
    return definition["report_id"]


def report_type_from_id(report_id: str) -> tuple[ReportType, Optional[str]]:
    for report_type, definition in REPORT_DEFINITIONS.items():
        base_id = definition["report_id"]
        if report_id == base_id:
            return report_type, None
        prefix = f"{base_id}-"
        if report_id.startswith(prefix):
            return report_type, report_id[len(prefix):] or None
    raise ValueError(f"Unknown report id: {report_id}")


def catalog_item(report_type: ReportType, generated_by: str = "system") -> ReportCatalogItem:
    definition = REPORT_DEFINITIONS[report_type]
    return ReportCatalogItem(
        report_id=definition["report_id"],
        title=definition["title"],
        description=definition["description"],
        report_type=report_type,
        created_at=datetime.now(),
        generated_by=generated_by,
        export_formats=list(definition["export_formats"]),
    )


def type_info(report_type: ReportType) -> ReportTypeInfo:
    definition = REPORT_DEFINITIONS[report_type]
    return ReportTypeInfo(
        report_id=definition["report_id"],
        title=definition["title"],
        description=definition["description"],
        report_type=report_type,
        export_formats=list(definition["export_formats"]),
    )


def supported_report_types() -> list[ReportType]:
    return list(REPORT_DEFINITIONS.keys())


def report_title(report_type: ReportType | str) -> str:
    return report_definition(report_type)["title"]


def report_description(report_type: ReportType | str) -> str:
    return report_definition(report_type)["description"]


def report_formats(report_type: ReportType | str) -> list[ReportFormat]:
    return list(report_definition(report_type)["export_formats"])
