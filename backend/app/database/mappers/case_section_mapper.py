"""
Mapper between CaseSectionAssociation domain model and ActSectionAssociationORM.
"""

from datetime import datetime
from typing import Optional
from app.models.case_section import CaseSectionAssociation
from app.database.orm.case_section import ActSectionAssociationORM


class CaseSectionMapper:
    @staticmethod
    def _parse_case_id(val: str) -> int:
        clean = str(val).replace("CM-", "")
        try:
            return int(clean)
        except ValueError:
            return abs(hash(val)) % 2147483647

    @classmethod
    def to_domain(cls, orm: ActSectionAssociationORM) -> CaseSectionAssociation:
        assoc_id = f"CSA-{orm.casemasterid}-{orm.sectionid}"
        now = datetime.now()
        return CaseSectionAssociation(
            association_id=assoc_id,
            case_master_id=f"CM-{orm.casemasterid}",
            section_id=orm.sectionid,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: CaseSectionAssociation) -> ActSectionAssociationORM:
        return ActSectionAssociationORM(
            casemasterid=cls._parse_case_id(domain.case_master_id),
            actid="BNS",  # Default act code
            sectionid=domain.section_id,
        )
