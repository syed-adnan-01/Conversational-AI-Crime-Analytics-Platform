from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UploadCategory(str, Enum):
    FIR_DOCUMENTS = "FIR documents"
    EVIDENCE_IMAGES = "Evidence images"
    EVIDENCE_VIDEOS = "Evidence videos"
    EVIDENCE_DOCUMENTS = "Evidence documents"
    AUDIO_RECORDINGS = "Audio recordings"
    CHARGESHEETS = "Chargesheets"
    COURT_DOCUMENTS = "Court documents"
    INVESTIGATION_REPORTS = "Investigation reports"
    MISCELLANEOUS = "Miscellaneous attachments"

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    content_type: str
    size: int
    category: UploadCategory
    upload_time: datetime
    storage_provider: str
    case_id: Optional[str] = None

class UploadHealthResponse(BaseModel):
    storage_backend: str
    writable: bool
    available_providers: list[str]
