"""
Mapper between CaseMaster domain model and CaseMasterORM.
"""

from datetime import datetime, date
from typing import Optional
from app.models.case_master import CaseMaster
from app.database.orm.case_master import CaseMasterORM


class CaseMapper:
    @staticmethod
    def _parse_id(case_master_id: Optional[str]) -> Optional[int]:
        if not case_master_id:
            return None
        if isinstance(case_master_id, int):
            return case_master_id
        clean = case_master_id.replace("CM-", "")
        try:
            return int(clean)
        except ValueError:
            return abs(hash(case_master_id)) % 2147483647

    @staticmethod
    def _format_id(val: Optional[int]) -> Optional[str]:
        if val is None:
            return None
        return f"CM-{val}"

    @classmethod
    def to_domain(cls, orm: CaseMasterORM) -> CaseMaster:
        reg_date = orm.crimeregistereddate
        if isinstance(reg_date, date) and not isinstance(reg_date, datetime):
            reg_date = datetime.combine(reg_date, datetime.min.time())

        now = datetime.now()

        return CaseMaster(
            case_master_id=cls._format_id(orm.casemasterid),
            crime_no=orm.crimeno,
            case_no=orm.caseno,
            crime_registered_date=reg_date,
            police_person_id=orm.policepersonid,
            police_station_id=orm.policestationid or 1,
            case_category_id=orm.casecategoryid,
            gravity_offence_id=orm.gravityoffenceid,
            crime_major_head_id=orm.crimemajorheadid,
            crime_minor_head_id=orm.crimeminorheadid,
            case_status_id=orm.casestatusid,
            court_id=orm.courtid,
            incident_from_date=orm.incidentfromdate,
            incident_to_date=orm.incidenttodate,
            info_received_ps_date=orm.inforeceivedpsdate,
            latitude=float(orm.latitude) if orm.latitude is not None else None,
            longitude=float(orm.longitude) if orm.longitude is not None else None,
            brief_facts=orm.brieffacts,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: CaseMaster) -> CaseMasterORM:
        reg_date = domain.crime_registered_date
        if isinstance(reg_date, datetime):
            reg_date = reg_date.date()

        orm_kwargs = {
            "crimeno": domain.crime_no,
            "caseno": domain.case_no or "",
            "crimeregistereddate": reg_date,
            "policepersonid": domain.police_person_id or 1,
            "policestationid": domain.police_station_id or 1,
            "casecategoryid": domain.case_category_id or 1,
            "gravityoffenceid": domain.gravity_offence_id or 1,
            "crimemajorheadid": domain.crime_major_head_id or 1,
            "crimeminorheadid": domain.crime_minor_head_id or 1,
            "casestatusid": domain.case_status_id or 1,
            "courtid": domain.court_id,
            "incidentfromdate": domain.incident_from_date,
            "incidenttodate": domain.incident_to_date,
            "inforeceivedpsdate": domain.info_received_ps_date,
            "latitude": domain.latitude,
            "longitude": domain.longitude,
            "brieffacts": domain.brief_facts,
        }

        parsed_id = cls._parse_id(domain.case_master_id)
        if parsed_id is not None:
            orm_kwargs["casemasterid"] = parsed_id

        return CaseMasterORM(**orm_kwargs)
