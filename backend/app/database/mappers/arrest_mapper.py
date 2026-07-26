"""
Mapper between Arrest domain model and ArrestSurrenderORM with integer key attribute extension cache.
"""

from datetime import datetime, date
from typing import Optional, Dict
from app.models.arrest import Arrest, ArrestStatus
from app.database.orm.arrest import ArrestSurrenderORM

_ARREST_CACHE: Dict[int, Dict] = {}


class ArrestMapper:
    @staticmethod
    def _parse_id(val: Optional[str]) -> Optional[int]:
        if not val:
            return None
        if isinstance(val, int):
            return val
        clean = str(val).replace("ARR-", "").replace("AR-", "").replace("A-", "")
        try:
            return int(clean)
        except ValueError:
            return abs(hash(val)) % 2147483647

    @staticmethod
    def _parse_case_id(val: str) -> int:
        clean = str(val).replace("CM-", "")
        try:
            return int(clean)
        except ValueError:
            return abs(hash(val)) % 2147483647

    @staticmethod
    def _parse_accused_id(val: str) -> int:
        clean = str(val).replace("ACC-", "").replace("AC-", "").replace("A-", "")
        try:
            return int(clean)
        except ValueError:
            return abs(hash(val)) % 2147483647

    @classmethod
    def cache_domain(cls, domain: Arrest, db_id: Optional[int] = None):
        parsed = db_id or cls._parse_id(domain.arrest_id)
        if parsed is not None:
            _ARREST_CACHE[parsed] = {
                "arrest_id": domain.arrest_id,
                "arrest_location": domain.arrest_location,
                "grounds_for_arrest": domain.grounds_for_arrest,
                "arresting_officer": domain.arresting_officer,
                "status": domain.status,
            }

    @classmethod
    def to_domain(cls, orm: ArrestSurrenderORM) -> Arrest:
        cached = _ARREST_CACHE.get(orm.arrestsurrenderid, {})
        arrest_id = cached.get("arrest_id") or f"AR-{orm.arrestsurrenderid}"
        now = datetime.now()
        arr_date = now
        if orm.arrestsurrenderdate:
            arr_date = datetime.combine(orm.arrestsurrenderdate, datetime.min.time())

        return Arrest(
            arrest_id=arrest_id,
            case_master_id=f"CM-{orm.casemasterid}",
            accused_id=f"AC-{orm.accusedmasterid or 1}",
            arrest_date=arr_date,
            arrest_location=cached.get("arrest_location") or "Police Jurisdiction",
            grounds_for_arrest=cached.get("grounds_for_arrest") or "Investigation Findings",
            arresting_officer=cached.get("arresting_officer") or "Officer-in-charge",
            status=cached.get("status") or ArrestStatus.ARRESTED,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Arrest) -> ArrestSurrenderORM:
        cls.cache_domain(domain)
        arr_date = domain.arrest_date
        if isinstance(arr_date, datetime):
            arr_date = arr_date.date()

        kwargs = {
            "casemasterid": cls._parse_case_id(domain.case_master_id),
            "accusedmasterid": cls._parse_accused_id(domain.accused_id),
            "arrestsurrenderdate": arr_date,
            "isaccused": True,
        }
        parsed_id = cls._parse_id(domain.arrest_id)
        if parsed_id is not None:
            kwargs["arrestsurrenderid"] = parsed_id

        return ArrestSurrenderORM(**kwargs)
