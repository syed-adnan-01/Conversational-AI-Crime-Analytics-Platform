"""
ORM Models Package - Maps PostgreSQL tables to SQLAlchemy declarative models.
Imports all models to register them with Base.metadata.
"""

from app.database.orm.act import ActORM
from app.database.orm.section import SectionORM
from app.database.orm.case_section import ActSectionAssociationORM
from app.database.orm.case_master import CaseMasterORM
from app.database.orm.victim import VictimORM
from app.database.orm.accused import AccusedORM
from app.database.orm.complainant import ComplainantDetailsORM
from app.database.orm.witness import WitnessORM
from app.database.orm.evidence import EvidenceORM
from app.database.orm.arrest import ArrestSurrenderORM
from app.database.orm.chargesheet import ChargesheetDetailsORM
from app.database.orm.court_proceeding import CourtProceedingORM
from app.database.orm.timeline import CaseTimelineORM
from app.database.orm.user import UserORM
from app.database.orm.lookups import (
    EmployeeORM,
    UnitORM,
    CourtORM,
    CaseCategoryORM,
    GravityOffenceORM,
    CrimeHeadORM,
    CrimeSubHeadORM,
    CaseStatusMasterORM,
)

__all__ = [
    "ActORM",
    "SectionORM",
    "ActSectionAssociationORM",
    "CaseMasterORM",
    "VictimORM",
    "AccusedORM",
    "ComplainantDetailsORM",
    "WitnessORM",
    "EvidenceORM",
    "ArrestSurrenderORM",
    "ChargesheetDetailsORM",
    "CourtProceedingORM",
    "CaseTimelineORM",
    "UserORM",
    "EmployeeORM",
    "UnitORM",
    "CourtORM",
    "CaseCategoryORM",
    "GravityOffenceORM",
    "CrimeHeadORM",
    "CrimeSubHeadORM",
    "CaseStatusMasterORM",
]
