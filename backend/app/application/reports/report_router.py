from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.dependencies import get_current_user
from app.models.user import User

from .report_models import (
    ReportExportResponse,
    ReportGenerateRequest,
    ReportHealthResponse,
    ReportListResponse,
    ReportResponse,
    ReportFormat,
    ReportTypeResponse,
)
from .report_service import ReportService


router = APIRouter()
service = ReportService()


@router.get("", summary="List available reports", response_model=ReportListResponse)
def list_reports(current_user: User = Depends(get_current_user)):
    return service.list_reports(generated_by=current_user.name)


@router.get("/types", summary="List supported report types", response_model=ReportTypeResponse)
def report_types(current_user: User = Depends(get_current_user)):
    return service.list_types()


@router.get("/health", summary="Report engine health", response_model=ReportHealthResponse)
def health(current_user: User = Depends(get_current_user)):
    return service.health()


@router.post("/generate", summary="Generate a report", response_model=ReportResponse)
def generate_report(body: ReportGenerateRequest, current_user: User = Depends(get_current_user)):
    return service.generate_report(body.report_type, case_id=body.case_id, generated_by=current_user.name)


@router.get("/{report_id}/export", summary="Export a generated report", response_model=ReportExportResponse)
def export_report(
    report_id: str,
    format: ReportFormat = Query(default=ReportFormat.JSON, alias="format"),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.export_report(report_id, format, generated_by=current_user.name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{report_id}", summary="Get a generated report", response_model=ReportResponse)
def get_report(report_id: str, current_user: User = Depends(get_current_user)):
    try:
        return service.get_report(report_id, generated_by=current_user.name)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
