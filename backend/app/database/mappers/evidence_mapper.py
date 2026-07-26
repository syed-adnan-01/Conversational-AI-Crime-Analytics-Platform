"""
Mapper between Evidence domain model and EvidenceORM.
"""

from datetime import datetime
from typing import Dict, Any
from app.models.evidence import Evidence, EvidenceType, EvidenceStatus
from app.database.orm.evidence import EvidenceORM

_EVIDENCE_CACHE: Dict[str, Dict[str, Any]] = {}


class EvidenceMapper:
    @classmethod
    def cache_domain(cls, domain: Evidence):
        if not domain:
            return
        data = {
            "title": domain.title,
            "victim_id": domain.victim_id,
            "accused_id": domain.accused_id,
            "section_id": domain.section_id,
            "evidence_category": domain.evidence_category,
            "status": domain.status,
            "custody_status": domain.custody_status,
            "storage_key": domain.storage_key,
            "mime_type": domain.mime_type,
            "file_size": domain.file_size,
            "checksum": domain.checksum,
            "checksum_algorithm": domain.checksum_algorithm,
            "remarks": domain.remarks,
        }
        if domain.evidence_id:
            _EVIDENCE_CACHE[domain.evidence_id] = data
        if domain.evidence_number:
            _EVIDENCE_CACHE[domain.evidence_number] = data

    @classmethod
    def to_domain(cls, orm: EvidenceORM) -> Evidence:
        ev_type = EvidenceType.OTHER
        try:
            ev_type = EvidenceType(orm.evidence_type)
        except ValueError:
            pass

        now = datetime.now()
        cached = _EVIDENCE_CACHE.get(orm.evidence_id) or _EVIDENCE_CACHE.get(orm.evidence_number) or {}

        title = cached.get("title") or orm.evidence_number

        return Evidence(
            evidence_id=orm.evidence_id,
            case_master_id=orm.case_master_id,
            victim_id=cached.get("victim_id"),
            accused_id=cached.get("accused_id"),
            section_id=cached.get("section_id"),
            evidence_number=orm.evidence_number,
            title=title,
            description=orm.description or "",
            evidence_type=ev_type,
            evidence_category=cached.get("evidence_category"),
            status=cached.get("status") or EvidenceStatus.COLLECTED,
            custody_status=cached.get("custody_status"),
            collected_by=orm.collected_by or "Unknown",
            collection_date=orm.collected_date or now,
            collection_location=orm.storage_location or "Station Storage",
            storage_location=orm.storage_location or "Station Storage",
            storage_key=cached.get("storage_key"),
            mime_type=cached.get("mime_type"),
            file_size=cached.get("file_size"),
            checksum=cached.get("checksum"),
            checksum_algorithm=cached.get("checksum_algorithm"),
            remarks=cached.get("remarks"),
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Evidence) -> EvidenceORM:
        cls.cache_domain(domain)
        return EvidenceORM(
            evidence_id=domain.evidence_id or "",
            case_master_id=domain.case_master_id,
            evidence_number=domain.evidence_number,
            evidence_type=domain.evidence_type.value if hasattr(domain.evidence_type, 'value') else str(domain.evidence_type),
            description=domain.description,
            collected_date=domain.collection_date,
            collected_by=domain.collected_by,
            storage_location=domain.storage_location,
        )
