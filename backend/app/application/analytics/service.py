from collections import Counter,defaultdict
from app.services.case_service import CaseService
class AnalyticsService:
 def __init__(self,cases=None): self.cases=cases or CaseService.get_all_cases
 def _all(self): return self.cases()
 def crime_types(self): return dict(Counter(str(c.crime_major_head_id) for c in self._all() if c.crime_major_head_id is not None))
 def districts(self): return dict(Counter(str(c.police_station_id) for c in self._all() if c.police_station_id is not None))
 def officers(self): return dict(Counter(str(c.police_person_id) for c in self._all() if c.police_person_id is not None))
 def monthly(self):
  values=defaultdict(int)
  for c in self._all(): values[c.crime_registered_date.strftime('%Y-%m')]+=1
  return [{'period':k,'cases':v} for k,v in sorted(values.items())]
 def yearly(self):
  values=defaultdict(int)
  for c in self._all(): values[str(c.crime_registered_date.year)]+=1
  return [{'period':k,'cases':v} for k,v in sorted(values.items())]
