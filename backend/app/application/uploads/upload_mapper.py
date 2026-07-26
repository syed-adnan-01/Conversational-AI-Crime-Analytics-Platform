from .upload_models import UploadResponse, UploadCategory
from .upload_storage import UploadEntity

class UploadMapper:
    @staticmethod
    def to_response(entity: UploadEntity) -> UploadResponse:
        return UploadResponse(
            file_id=entity.file_id,
            filename=entity.filename,
            content_type=entity.content_type,
            size=entity.size,
            category=UploadCategory(entity.category),
            upload_time=entity.upload_time,
            storage_provider=entity.storage_provider,
            case_id=entity.case_id
        )
