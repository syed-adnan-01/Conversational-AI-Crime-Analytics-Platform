from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from typing import List, Optional
from .upload_models import UploadCategory, UploadResponse, UploadHealthResponse
from .upload_service import UploadService

router = APIRouter(prefix="/uploads", tags=["Uploads"])
service = UploadService()

@router.post("", response_model=UploadResponse)
def upload_file(
    file: UploadFile = File(...),
    category: UploadCategory = Form(...),
    case_id: Optional[str] = Form(None)
):
    """Upload a multipart file."""
    return service.upload_file(file, category, case_id)

@router.get("", response_model=List[UploadResponse])
def list_uploads(category: Optional[UploadCategory] = None, case_id: Optional[str] = None):
    """List uploaded files."""
    return service.list_uploads(category, case_id)

@router.get("/health", response_model=UploadHealthResponse)
def get_health():
    """Get storage health status."""
    return service.get_health()

@router.get("/{file_id}", response_model=UploadResponse)
def get_upload_metadata(file_id: str):
    """Return metadata only."""
    metadata = service.get_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
    return metadata

@router.get("/{file_id}/download")
def download_file(file_id: str):
    """Return file stream or download URL."""
    metadata = service.get_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
        
    file_path = service.get_file_path(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File content not found in storage")
        
    return FileResponse(path=file_path, filename=metadata.filename, media_type=metadata.content_type)

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_upload(file_id: str):
    """Delete uploaded file."""
    success = service.delete_upload(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
