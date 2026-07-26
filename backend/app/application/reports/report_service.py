from __future__ import annotations

from typing import Optional

from .report_export import ReportExportService
from .report_generator import ReportGenerator
from .report_models import (
    ReportExportResponse,
    ReportFormat,
    ReportHealthResponse,
    ReportListResponse,
    ReportResponse,
    ReportType,
    ReportTypeResponse,
)


class ReportService:
    def __init__(self, generator: ReportGenerator | None = None, exporter: ReportExportService | None = None) -> None:
        self.generator = generator or ReportGenerator()
        self.exporter = exporter or ReportExportService()

    def list_reports(self, generated_by: str = "system") -> ReportListResponse:
        items = self.generator.list_reports(generated_by=generated_by)
        return ReportListResponse(items=items, total=len(items))

    def list_types(self) -> ReportTypeResponse:
        items = self.generator.list_types()
        return ReportTypeResponse(items=items, total=len(items))

    def generate_report(
        self,
        report_type: ReportType | str,
        case_id: Optional[str] = None,
        generated_by: str = "system",
    ) -> ReportResponse:
        return self.generator.generate(report_type=report_type, case_id=case_id, generated_by=generated_by)

    def get_report(self, report_id: str, generated_by: str = "system") -> ReportResponse:
        return self.generator.get_report(report_id, generated_by=generated_by)

    def export_report(self, report_id: str, export_format: ReportFormat, generated_by: str = "system") -> ReportExportResponse:
        report = self.get_report(report_id, generated_by=generated_by)
        return self.exporter.build_export(report, export_format)

    def health(self) -> ReportHealthResponse:
        supported_formats = [ReportFormat.JSON, ReportFormat.CSV, ReportFormat.PDF]
        export_capability = {format_item.value: format_item != ReportFormat.PDF for format_item in supported_formats}
        return ReportHealthResponse(
            report_engine_status="ready",
            export_capability=export_capability,
            supported_formats=supported_formats,
        )
