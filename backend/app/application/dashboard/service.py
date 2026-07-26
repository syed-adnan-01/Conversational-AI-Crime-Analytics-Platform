from collections import Counter
from app.services.case_service import CaseService
from app.repository.evidence_repository import EvidenceRepository
from app.repository.officer_repository import OfficerRepository
from .models import DashboardSummary, RecentCase
class DashboardService:
    def _cases(self): return CaseService.get_all_cases()
    def summary(self):
        cases=self._cases(); status=Counter(str(c.case_status_id) for c in cases); evidence=sum(len(EvidenceRepository.get_case_evidence(c.case_master_id or '')) for c in cases)
        closed=status.get('0',0); pending=status.get('1',0); total=len(cases)
        return DashboardSummary(total_cases=total,open_cases=max(0,total-closed-pending),closed_cases=closed,pending_cases=pending,investigation_completion_percent=round(closed/total*100,2) if total else 0,evidence_uploaded=evidence,officers_assigned=len([c for c in cases if c.police_person_id is not None]))
    def recent_cases(self):
        return [RecentCase(case_id=str(c.case_master_id),case_number=c.case_no,fir=c.crime_no,district=str(c.police_station_id) if c.police_station_id else None,officer=str(c.police_person_id) if c.police_person_id else None,priority=str(c.gravity_offence_id) if c.gravity_offence_id else None,status=str(c.case_status_id) if c.case_status_id else None,created_date=c.crime_registered_date,risk_score=None) for c in sorted(self._cases(),key=lambda x:x.crime_registered_date,reverse=True)[:10]]
