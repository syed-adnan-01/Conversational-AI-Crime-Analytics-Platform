"""
Mapper between CourtProceeding domain model and CourtProceedingORM.
"""

from datetime import datetime
from app.models.court_proceeding import CourtProceeding, ProceedingStage
from app.database.orm.court_proceeding import CourtProceedingORM


class CourtProceedingMapper:
    @classmethod
    def to_domain(cls, orm: CourtProceedingORM) -> CourtProceeding:
        stage_val = ProceedingStage.HEARING_DATE if hasattr(ProceedingStage, "HEARING_DATE") else ProceedingStage.COGNIZANCE
        try:
            stage_val = ProceedingStage(orm.stage)
        except (ValueError, TypeError):
            pass

        now = datetime.now()

        return CourtProceeding(
            proceeding_id=orm.proceeding_id,
            case_master_id=orm.case_master_id,
            court_name=f"Court #{orm.court_id or 1}",
            judge_name=orm.judge_name or "Magistrate",
            hearing_date=orm.hearing_date or now,
            stage=stage_val,
            summary=orm.summary or "Court hearing completed",
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def to_orm(cls, domain: CourtProceeding) -> CourtProceedingORM:
        return CourtProceedingORM(
            proceeding_id=domain.proceeding_id or "",
            case_master_id=domain.case_master_id,
            court_id=1,
            hearing_date=domain.hearing_date,
            stage=domain.stage.value if hasattr(domain.stage, "value") else str(domain.stage),
            judge_name=domain.judge_name,
            summary=domain.summary,
        )
