from typing import Optional, List
from fastapi import UploadFile
from .upload_models import UploadCategory, UploadResponse, UploadHealthResponse
from .upload_storage import UploadStorage, UploadMetadataRepository, UploadEntity, default_storage, upload_metadata_repo
from .upload_validator import UploadValidator
from .upload_mapper import UploadMapper

class UploadService:
    def __init__(self, 
                 storage: UploadStorage = default_storage, 
                 metadata_repo: UploadMetadataRepository = upload_metadata_repo):
        self.storage = storage
        self.metadata_repo = metadata_repo
        
    def upload_file(self, file: UploadFile, category: UploadCategory, case_id: Optional[str] = None) -> UploadResponse:
        size = UploadValidator.validate_file(file)
        
        entity = UploadEntity(
            filename=file.filename or "unknown",
            content_type=file.content_type or "application/octet-stream",
            size=size,
            category=category.value,
            storage_provider=self.storage.__class__.__name__,
            case_id=case_id
        )
        
        # Save to storage
        self.storage.save(entity.file_id, entity.filename, file.file)
        
        # Save metadata
        self.metadata_repo.add(entity)
        
        return UploadMapper.to_response(entity)
        
    def get_metadata(self, file_id: str) -> Optional[UploadResponse]:
        entity = self.metadata_repo.get_by_id(file_id)
        if entity:
            return UploadMapper.to_response(entity)
        return None
        
    def list_uploads(self, category: Optional[UploadCategory] = None, case_id: Optional[str] = None) -> List[UploadResponse]:
        cat_value = category.value if category else None
        entities = self.metadata_repo.get_all(category=cat_value, case_id=case_id)
        return [UploadMapper.to_response(e) for e in entities]
        
    def delete_upload(self, file_id: str) -> bool:
        entity = self.metadata_repo.get_by_id(file_id)
        if not entity:
            return False
            
        # Delete from storage
        self.storage.delete(entity.file_id, entity.filename)
        
        # Delete from metadata repo
        return self.metadata_repo.delete(file_id)
        
    def get_file_path(self, file_id: str) -> Optional[str]:
        entity = self.metadata_repo.get_by_id(file_id)
        if not entity:
            return None
        return self.storage.get_path(entity.file_id, entity.filename)
        
    def get_health(self) -> UploadHealthResponse:
        return UploadHealthResponse(
            storage_backend=self.storage.__class__.__name__,
            writable=self.storage.is_writable(),
            available_providers=["LocalFilesystemStorage"] # Add more when implemented
        )
