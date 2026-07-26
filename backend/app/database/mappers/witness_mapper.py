"""
Mapper between Witness domain model and WitnessORM.
"""

from datetime import datetime
from app.models.witness import Witness
from app.database.orm.witness import WitnessORM
from app.common.enums import Gender


class WitnessMapper:
    @classmethod
    def to_domain(cls, orm: WitnessORM) -> Witness:
        now = datetime.now()
        is_hostile = (orm.witness_type == "Hostile") if orm.witness_type else False
        return Witness(
            witness_id=orm.witness_id,
            case_master_id=orm.case_master_id,
            name=orm.witness_name,
            gender=Gender.MALE,
            statement=orm.statement_summary,
            mobile_no=orm.contact_number,
            occupation=orm.witness_type if not is_hostile else None,
            is_hostile=is_hostile,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: Witness) -> WitnessORM:
        witness_type = "Hostile" if domain.is_hostile else (domain.occupation or "General")
        return WitnessORM(
            witness_id=domain.witness_id or "",
            case_master_id=domain.case_master_id,
            witness_name=domain.name,
            witness_type=witness_type,
            statement_summary=domain.statement,
            contact_number=domain.mobile_no,
        )
