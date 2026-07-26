"""
Mapper between Accused domain model and AccusedORM, with integer-keyed attribute extension cache.
"""

from datetime import datetime
from typing import Optional, Dict
from app.models.accused import Accused
from app.database.orm.accused import AccusedORM
from app.common.enums import Gender

_ACCUSED_CACHE: Dict[int, Dict] = {}


class AccusedMapper:
    @staticmethod
    def _parse_id(val: Optional[str]) -> Optional[int]:
        if not val:
            return None
        if isinstance(val, int):
            return val
        clean = str(val).replace("ACC-", "").replace("AC-", "").replace("A-", "")
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
    def cache_domain(cls, domain: Accused, db_id: Optional[int] = None):
        parsed = db_id or cls._parse_id(domain.accused_id)
        if parsed is not None:
            _ACCUSED_CACHE[parsed] = {
                "accused_id": domain.accused_id,
                "mobile_no": domain.mobile_no,
                "email": domain.email,
                "address": domain.address,
                "nationality": domain.nationality,
                "occupation": domain.occupation,
                "id_type": domain.id_type,
                "id_number": domain.id_number,
            }

    @classmethod
    def to_domain(cls, orm: AccusedORM) -> Accused:
        cached = _ACCUSED_CACHE.get(orm.accusedmasterid, {})
        accused_id = cached.get("accused_id") or f"AC-{orm.accusedmasterid}"

        gender_val = None
        if orm.genderid == 1:
            gender_val = Gender.MALE
        elif orm.genderid == 2:
            gender_val = Gender.FEMALE
        elif orm.genderid == 3:
            gender_val = Gender.TRANSGENDER

        now = datetime.now()

        return Accused(
            accused_id=accused_id,
            case_master_id=f"CM-{orm.casemasterid}",
            name=orm.accusedname,
            gender=gender_val,
            age=orm.ageyear,
            mobile_no=cached.get("mobile_no"),
            email=cached.get("email"),
            address=cached.get("address"),
            nationality=cached.get("nationality"),
            occupation=cached.get("occupation"),
            id_type=cached.get("id_type"),
            id_number=cached.get("id_number") or orm.personid,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Accused) -> AccusedORM:
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
            "accusedname": domain.name,
            "ageyear": domain.age,
            "genderid": gender_id,
            "personid": domain.id_number,
        }
        parsed_id = cls._parse_id(domain.accused_id)
        if parsed_id is not None:
            kwargs["accusedmasterid"] = parsed_id

        return AccusedORM(**kwargs)
