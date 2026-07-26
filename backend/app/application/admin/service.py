from app.repository.user_repository import UserRepository
from app.repository.officer_repository import OfficerRepository
from app.core.roles import UserRole

ROLE_META = {
    "admin":        {"clearance_level": 5, "description": "Full system access. Can manage users, roles, and all data.", "permissions": ["cases:read", "cases:write", "cases:delete", "users:manage", "reports:all", "admin:all"]},
    "supervisor":   {"clearance_level": 4, "description": "Oversees investigation teams and reviews reports.", "permissions": ["cases:read", "cases:write", "reports:read", "users:read"]},
    "investigator": {"clearance_level": 3, "description": "Handles active case investigations.", "permissions": ["cases:read", "cases:write", "evidence:manage", "reports:read"]},
    "analyst":      {"clearance_level": 2, "description": "Analyzes crime data and produces insights.", "permissions": ["cases:read", "analytics:read", "reports:read"]},
    "policy_maker": {"clearance_level": 1, "description": "Reviews high-level reports and policy data.", "permissions": ["reports:read", "analytics:read"]},
}

class AdminService:
    def users(self):
        return [u.model_dump(mode='json') for u in UserRepository.list_users()]

    def officers(self):
        raw = OfficerRepository.list_officers()
        dept_map = UserRepository.get_department_map()
        result = []
        for o in raw:
            o_dict = o.model_dump(mode='json')
            result.append({
                "id": o_dict.get("officer_id", ""),
                "name": o_dict.get("name") or "Unknown Officer",
                "badge_number": o_dict.get("badge_number") or "-",
                "email": o_dict.get("email", ""),
                "role": o_dict.get("rank", "Officer"),
                "district": dept_map.get(o_dict.get("officer_id", ""), o_dict.get("department", "Unassigned")),
                "clearance_level": 2,
                "mfa_enabled": True,
                "status": "active" if o_dict.get("is_active", True) else "inactive",
                "last_login": None,
            })
        return result


    def roles(self):
        result = []
        users_list = self.users()
        for r in UserRole:
            meta = ROLE_META.get(r.value, {"clearance_level": 1, "description": r.value, "permissions": []})
            count = sum(1 for u in users_list if u.get("role") == r.value)
            result.append({
                "id": r.value,
                "name": r.value.replace("_", " ").title(),
                "clearance_level": meta["clearance_level"],
                "description": meta["description"],
                "permissions": meta["permissions"],
                "userCount": count,
            })
        return result

    def departments(self):
        dept_map = UserRepository.get_department_map()
        return sorted(set(dept_map.values())) if dept_map else ["Administration", "Investigation", "Crime Analytics", "Cyber Crime"]

    def audit(self):
        return []  # TODO: wire to a persistent audit log store

