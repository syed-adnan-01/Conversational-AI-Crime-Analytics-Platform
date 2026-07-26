"""
Mapper between Complainant domain model and ComplainantDetailsORM with integer key attribute extension cache.
"""

from datetime import datetime
from typing import Optional, Dict
from app.models.complainant import Complainant
from app.database.orm.complainant import ComplainantDetailsORM
from app.common.enums import Gender

_COMPLAINANT_CACHE: Dict[int, Dict] = {}


class ComplainantMapper:
    @staticmethod
    def _parse_id(val: Optional[str]) -> Optional[int]:
        if not val:
            return None
        if isinstance(val, int):
            return val
        clean = str(val).replace("COMP-", "").replace("C-", "")
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
    def cache_domain(cls, domain: Complainant, db_id: Optional[int] = None):
        parsed = db_id or cls._parse_id(domain.complainant_id)
        if parsed is not None:
            _COMPLAINANT_CACHE[parsed] = {
                "complainant_id": domain.complainant_id,
                "mobile_no": getattr(domain, "mobile_no", None),
                "email": getattr(domain, "email", None),
                "address": getattr(domain, "address", None),
                "nationality": getattr(domain, "nationality", None),
                "occupation": getattr(domain, "occupation", None),
                "id_type": getattr(domain, "id_type", None),
                "id_number": getattr(domain, "id_number", None),
                "relationship_to_case": getattr(domain, "relationship_to_case", None),
            }

    @classmethod
    def to_domain(cls, orm: ComplainantDetailsORM) -> Complainant:
        cached = _COMPLAINANT_CACHE.get(orm.complainantid, {})
        complainant_id = cached.get("complainant_id") or f"COMP-{orm.complainantid}"

        gender_val = None
        if orm.genderid == 1:
            gender_val = Gender.MALE
        elif orm.genderid == 2:
            gender_val = Gender.FEMALE
        elif orm.genderid == 3:
            gender_val = Gender.TRANSGENDER

        now = datetime.now()

        return Complainant(
            complainant_id=complainant_id,
            case_master_id=f"CM-{orm.casemasterid}",
            name=orm.complainantname,
            gender=gender_val,
            age=orm.ageyear,
            mobile_no=cached.get("mobile_no"),
            email=cached.get("email"),
            address=cached.get("address"),
            nationality=cached.get("nationality"),
            occupation=cached.get("occupation"),
            id_type=cached.get("id_type"),
            id_number=cached.get("id_number"),
            relationship_to_case=cached.get("relationship_to_case"),
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Complainant) -> ComplainantDetailsORM:
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
            "complainantname": domain.name,
            "ageyear": domain.age,
            "genderid": gender_id,
        }
        parsed_id = cls._parse_id(domain.complainant_id)
        if parsed_id is not None:
            kwargs["complainantid"] = parsed_id

        return ComplainantDetailsORM(**kwargs)
