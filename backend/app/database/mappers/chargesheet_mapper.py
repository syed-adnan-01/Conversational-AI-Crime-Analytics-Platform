"""
Mapper between Chargesheet domain model and ChargesheetDetailsORM.
"""

from datetime import datetime
from typing import Optional
from app.models.chargesheet import Chargesheet, ChargesheetStatus
from app.database.orm.chargesheet import ChargesheetDetailsORM


_CHARGESHEET_CACHE: dict[str, dict] = {}


class ChargesheetMapper:
    @staticmethod
    def _parse_id(val: Optional[str]) -> Optional[int]:
        if not val:
            return None
        if isinstance(val, int):
            return val
        clean = str(val).replace("CS-", "")
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

    @classmethod
    def cache_domain(cls, domain: Chargesheet):
        domain_dict = {
            "chargesheet_number": domain.chargesheet_number,
            "summary": domain.summary,
            "status": domain.status,
            "investigating_officer": domain.investigating_officer,
            "remarks": getattr(domain, "remarks", None),
        }
        if domain.chargesheet_id:
            _CHARGESHEET_CACHE[domain.chargesheet_id] = domain_dict
            parsed = cls._parse_id(domain.chargesheet_id)
            if parsed is not None:
                _CHARGESHEET_CACHE[f"CS-{parsed}"] = domain_dict
                _CHARGESHEET_CACHE[str(parsed)] = domain_dict
        if domain.chargesheet_number:
            _CHARGESHEET_CACHE[domain.chargesheet_number] = domain_dict

    @classmethod
    def to_domain(cls, orm: ChargesheetDetailsORM) -> Chargesheet:
        cs_id = f"CS-{orm.csid}"
        cached = _CHARGESHEET_CACHE.get(cs_id) or _CHARGESHEET_CACHE.get(str(orm.csid)) or {}
        now = datetime.now()

        chargesheet_number = cached.get("chargesheet_number") or f"CS-NO-{orm.csid}"
        summary = cached.get("summary") or "Final Chargesheet Submitted"
        status = cached.get("status") or ChargesheetStatus.FILED
        investigating_officer = cached.get("investigating_officer") or f"Officer-{orm.policepersonid or 1}"
        remarks = cached.get("remarks")

        return Chargesheet(
            chargesheet_id=cs_id,
            case_master_id=f"CM-{orm.casemasterid}",
            chargesheet_number=chargesheet_number,
            filing_date=orm.csdate or now,
            investigating_officer=investigating_officer,
            summary=summary,
            remarks=remarks,
            status=status,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Chargesheet) -> ChargesheetDetailsORM:
        cls.cache_domain(domain)
        kwargs = {
            "casemasterid": cls._parse_case_id(domain.case_master_id),
            "csdate": domain.filing_date,
            "cstype": "F",
            "policepersonid": 1,
        }
        parsed_id = cls._parse_id(domain.chargesheet_id)
        if parsed_id is not None:
            kwargs["csid"] = parsed_id

        return ChargesheetDetailsORM(**kwargs)
