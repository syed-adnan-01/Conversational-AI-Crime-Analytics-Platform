from app.repository.user_repository import UserRepository
from app.repository.officer_repository import OfficerRepository
from app.core.roles import UserRole
class AdminService:
 def users(self): return [u.model_dump(mode='json') for u in UserRepository.list_users()]
 def officers(self): return [o.model_dump(mode='json') for o in OfficerRepository.list_officers()]
 def roles(self): return [r.value for r in UserRole]
 def departments(self): return sorted({u['department'] for u in self.users()})
 def audit(self): return [] # TODO: audit persistence is exposed by security APIs, not an application repository.
