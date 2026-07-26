import os
from fastapi import UploadFile, HTTPException
from typing import Set

ALLOWED_EXTENSIONS: Set[str] = {".pdf", ".jpg", ".png", ".webp", ".mp4", ".mp3", ".wav"}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024 # 100MB configurable

class UploadValidator:
    @staticmethod
    def validate_file(file: UploadFile):
        # Check extension
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {ext}")
            
        # Check size - FastAPI UploadFile doesn't immediately know size unless we read/seek
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        
        if size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=400, detail=f"File exceeds maximum size of {MAX_FILE_SIZE_BYTES} bytes")
            
        return size
