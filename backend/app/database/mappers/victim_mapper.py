"""
Mapper between Victim domain model and VictimORM with integer key attribute extension cache.
"""

from datetime import datetime
from typing import Optional, Dict
from app.models.victim import Victim
from app.database.orm.victim import VictimORM
from app.common.enums import Gender

_VICTIM_CACHE: Dict[int, Dict] = {}


class VictimMapper:
    @staticmethod
    def _parse_id(val: Optional[str]) -> Optional[int]:
        if not val:
            return None
        if isinstance(val, int):
            return val
        clean = str(val).replace("VIC-", "").replace("V-", "")
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
    def cache_domain(cls, domain: Victim, db_id: Optional[int] = None):
        parsed = db_id or cls._parse_id(domain.victim_id)
        if parsed is not None:
            _VICTIM_CACHE[parsed] = {
                "victim_id": domain.victim_id,
                "mobile_no": getattr(domain, "mobile_no", None),
                "email": getattr(domain, "email", None),
                "address": getattr(domain, "address", None),
                "nationality": getattr(domain, "nationality", None),
                "occupation": getattr(domain, "occupation", None),
                "id_type": getattr(domain, "id_type", None),
                "id_number": getattr(domain, "id_number", None),
                "injury_details": getattr(domain, "injury_details", None),
            }

    @classmethod
    def to_domain(cls, orm: VictimORM) -> Victim:
        cached = _VICTIM_CACHE.get(orm.victimmasterid, {})
        victim_id = cached.get("victim_id") or f"VIC-{orm.victimmasterid}"

        gender_val = None
        if orm.genderid == 1:
            gender_val = Gender.MALE
        elif orm.genderid == 2:
            gender_val = Gender.FEMALE
        elif orm.genderid == 3:
            gender_val = Gender.TRANSGENDER

        now = datetime.now()

        return Victim(
            victim_id=victim_id,
            case_master_id=f"CM-{orm.casemasterid}",
            name=orm.victimname,
            gender=gender_val,
            age=orm.ageyear,
            mobile_no=cached.get("mobile_no"),
            email=cached.get("email"),
            address=cached.get("address"),
            nationality=cached.get("nationality"),
            occupation=cached.get("occupation"),
            id_type=cached.get("id_type"),
            id_number=cached.get("id_number"),
            injury_details=cached.get("injury_details"),
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Victim) -> VictimORM:
        cls.cache_domain(domain)
        gender_id = None
        if domain.gender == Gender.MALE:
            gender_id = 1
        elif domain.gender == Gender.FEMALE:
            gender_id = 2
        elif domain.gender == Gender.TRANSGENDER:
            gender_id = 3

        kwargs = {
            "casemasterid": cls._parse_case_id(domain.case_master_id),
            "victimname": domain.name,
            "ageyear": domain.age,
            "genderid": gender_id,
            "victimpolice": False,
        }
        parsed_id = cls._parse_id(domain.victim_id)
        if parsed_id is not None:
            kwargs["victimmasterid"] = parsed_id

        return VictimORM(**kwargs)
