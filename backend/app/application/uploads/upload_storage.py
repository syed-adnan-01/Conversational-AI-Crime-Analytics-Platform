from abc import ABC, abstractmethod
import os
import shutil
from typing import BinaryIO, Optional
import uuid
from threading import Lock
from datetime import datetime, timezone

class UploadStorage(ABC):
    @abstractmethod
    def save(self, file_id: str, filename: str, content: BinaryIO) -> str:
        """Saves a file and returns the storage path/identifier."""
        pass
        
    @abstractmethod
    def get_path(self, file_id: str, filename: str) -> str:
        """Gets the path or URL for a stored file."""
        pass
        
    @abstractmethod
    def delete(self, file_id: str, filename: str) -> bool:
        """Deletes a file."""
        pass
        
    @abstractmethod
    def is_writable(self) -> bool:
        """Checks if storage is writable."""
        pass

class LocalFilesystemStorage(UploadStorage):
    def __init__(self, base_dir: str = "/tmp/uploads"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
    def save(self, file_id: str, filename: str, content: BinaryIO) -> str:
        file_path = os.path.join(self.base_dir, f"{file_id}_{filename}")
        with open(file_path, "wb") as f:
            shutil.copyfileobj(content, f)
        return file_path
        
    def get_path(self, file_id: str, filename: str) -> str:
        return os.path.join(self.base_dir, f"{file_id}_{filename}")
        
    def delete(self, file_id: str, filename: str) -> bool:
        file_path = self.get_path(file_id, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
        
    def is_writable(self) -> bool:
        return os.access(self.base_dir, os.W_OK)

class UploadEntity:
    def __init__(self, filename: str, content_type: str, size: int, category: str, storage_provider: str, case_id: Optional[str] = None):
        self.file_id = str(uuid.uuid4())
        self.filename = filename
        self.content_type = content_type
        self.size = size
        self.category = category
        self.storage_provider = storage_provider
        self.upload_time = datetime.now(timezone.utc)
        self.case_id = case_id

class UploadMetadataRepository:
    def __init__(self):
        self._metadata: dict[str, UploadEntity] = {}
        self._lock = Lock()
        
    def add(self, entity: UploadEntity) -> UploadEntity:
        with self._lock:
            self._metadata[entity.file_id] = entity
        return entity
        
    def get_by_id(self, file_id: str) -> Optional[UploadEntity]:
        with self._lock:
            return self._metadata.get(file_id)
            
    def get_all(self, category: Optional[str] = None, case_id: Optional[str] = None) -> list[UploadEntity]:
        with self._lock:
            results = list(self._metadata.values())
            if category:
                results = [r for r in results if r.category == category]
            if case_id:
                results = [r for r in results if r.case_id == case_id]
            return results
            
    def delete(self, file_id: str) -> bool:
        with self._lock:
            if file_id in self._metadata:
                del self._metadata[file_id]
                return True
            return False

upload_metadata_repo = UploadMetadataRepository()
default_storage = LocalFilesystemStorage()
