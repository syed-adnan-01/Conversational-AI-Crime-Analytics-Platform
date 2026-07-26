from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ReportType(str, Enum):
    CASE_SUMMARY = "Case Summary"
    INVESTIGATION_REPORT = "Investigation Report"
    EVIDENCE_REPORT = "Evidence Report"
    TIMELINE_REPORT = "Timeline Report"
    OFFICER_ACTIVITY_REPORT = "Officer Activity Report"
    DASHBOARD_SUMMARY = "Dashboard Summary"
    ANALYTICS_SUMMARY = "Analytics Summary"


class ReportFormat(str, Enum):
    JSON = "JSON"
    CSV = "CSV"
    PDF = "PDF"


class ReportCatalogItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_id: str
    title: str
    description: str
    report_type: ReportType
    created_at: datetime
    generated_by: str
    export_formats: list[ReportFormat] = Field(default_factory=list)


class ReportTypeInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_id: str
    title: str
    description: str
    report_type: ReportType
    export_formats: list[ReportFormat] = Field(default_factory=list)


class ReportSection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    items: list[dict[str, Any]] = Field(default_factory=list)
    todo: list[str] = Field(default_factory=list)


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_id: str
    title: str
    description: str
    report_type: ReportType
    created_at: datetime
    generated_by: str
    export_formats: list[ReportFormat] = Field(default_factory=list)
    summary: dict[str, Any] = Field(default_factory=dict)
    sections: list[ReportSection] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)


class ReportGenerateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_type: ReportType
    case_id: Optional[str] = None


class ReportListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ReportCatalogItem] = Field(default_factory=list)
    total: int = 0


class ReportTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ReportTypeInfo] = Field(default_factory=list)
    total: int = 0


class ReportExportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    download_url: Optional[str] = None
    format: ReportFormat
    status: str


class ReportHealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_engine_status: str
    export_capability: dict[str, bool]
    supported_formats: list[ReportFormat] = Field(default_factory=list)
