from __future__ import annotations

from .report_mapper import report_formats
from .report_models import ReportExportResponse, ReportFormat, ReportResponse


class ReportExportService:
    def build_export(self, report: ReportResponse, export_format: ReportFormat) -> ReportExportResponse:
        if export_format == ReportFormat.PDF:
            return ReportExportResponse(download_url=None, format=export_format, status="not_implemented")

        if export_format not in report_formats(report.report_type):
            return ReportExportResponse(download_url=None, format=export_format, status="not_implemented")

        download_url = f"/reports/{report.report_id}/export?format={export_format.value}"
        return ReportExportResponse(download_url=download_url, format=export_format, status="ready")
