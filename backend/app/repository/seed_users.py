from app.core.roles import UserRole

SEED_USERS = [
    {
        "user_id": "USR001",
        "employee_id": "EMP001",
        "password": "password123",
        "name": "John Doe",
        "email": "john@crime.gov.in",
        "department": "Cyber Crime",
        "role": UserRole.INVESTIGATOR,
        "is_active": True,
    },
    {
        "user_id": "USR002",
        "employee_id": "EMP002",
        "password": "password123",
        "name": "Sarah Khan",
        "email": "sarah@crime.gov.in",
        "department": "Crime Analytics",
        "role": UserRole.ANALYST,
        "is_active": True,
    },
    {
        "user_id": "USR003",
        "employee_id": "EMP003",
        "password": "password123",
        "name": "Rahul Sharma",
        "email": "rahul@crime.gov.in",
        "department": "Investigation",
        "role": UserRole.SUPERVISOR,
        "is_active": True,
    },
]