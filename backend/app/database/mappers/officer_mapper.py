"""
Mapper between Officer domain model and EmployeeORM.
"""

from typing import Optional
from app.models.officer import OfficerMaster, OfficerRank
from app.database.orm.lookups import EmployeeORM


class OfficerMapper:
    @classmethod
    def _parse_id(cls, officer_id: str) -> Optional[int]:
        if not officer_id:
            return None
        clean = str(officer_id).replace("OFF-", "")
        if clean.isdigit():
            return int(clean)
        return None

    @classmethod
    def to_domain(cls, orm: EmployeeORM) -> OfficerMaster:
        return OfficerMaster(
            officer_id=f"OFF-{orm.employeeid}",
            badge_number=orm.kgid or f"BADGE-{orm.employeeid}",
            name=orm.firstname or "Unknown Officer",
            rank=OfficerRank.SUB_INSPECTOR,
            department="Police",
            is_active=True,
        )

    @classmethod
    def to_orm(cls, domain: OfficerMaster) -> EmployeeORM:
        emp_id = cls._parse_id(domain.officer_id)

        kwargs = {
            "districtid": 1,
            "unitid": getattr(domain, "police_station_id", None) or 1,
            "rankid": 1,
            "designationid": 1,
            "kgid": domain.badge_number,
            "firstname": domain.name,
        }
        if emp_id is not None:
            kwargs["employeeid"] = emp_id

        return EmployeeORM(**kwargs)
