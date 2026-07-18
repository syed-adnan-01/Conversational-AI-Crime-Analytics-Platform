import sys
from fastapi.testclient import TestClient

from app.main import app
from app.repository.act_repository import ActRepository
from app.repository.user_repository import UserRepository
from app.core.password import PasswordManager
from app.core.roles import UserRole


def run_tests():
    print("Initializing TestClient for Acts...")
    client = TestClient(app)

    with client as c:
        print("TestClient active in lifespan context.")

        # Dynamically inject an Admin user to UserRepository for testing Admin-only features
        admin_employee_id = "EMP004"
        admin_password = "password123"
        admin_department = "IT Dept"

        # Ensure UserRepository is initialized
        UserRepository.initialize()

        # Check if Admin already injected
        if not any(u["employee_id"] == admin_employee_id for u in UserRepository._users):
            UserRepository._users.append({
                "user_id": "USR004",
                "employee_id": admin_employee_id,
                "password": PasswordManager.hash_password(admin_password),
                "name": "Admin User",
                "email": "admin@crime.gov.in",
                "department": admin_department,
                "role": UserRole.ADMIN,
                "is_active": True,
            })
            print("Dynamically injected Admin user into in-memory database.")

        # 1. Login as Admin
        print("Logging in as Admin...")
        login_res = c.post(
            "/auth/login",
            json={
                "employee_id": admin_employee_id,
                "password": admin_password,
                "department": admin_department,
            },
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.json()}"
        admin_token = login_res.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Login as Investigator
        print("Logging in as Investigator...")
        login_inv = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        assert login_inv.status_code == 200
        inv_token = login_inv.json()["access_token"]
        inv_headers = {"Authorization": f"Bearer {inv_token}"}

        # 2. Check Seeded Acts
        print("Checking seeded acts...")
        res = c.get("/acts", headers=inv_headers)
        assert res.status_code == 200, f"Failed to list acts: {res.json()}"
        data = res.json()
        assert len(data["items"]) >= 3, f"Expected at least 3 seeded acts, got {len(data['items'])}"
        
        # Verify specific seeded acts
        short_names = [a["short_name"] for a in data["items"]]
        assert "BNS" in short_names
        assert "BNSS" in short_names
        assert "IT Act" in short_names
        print("Seeded acts verification passed.")

        # Clear non-seed acts by resetting repository to seed values
        ActRepository._acts.clear()
        ActRepository.initialize()

        # 3. Create Act (RBAC Check)
        print("Testing Act creation RBAC (Investigator should be forbidden)...")
        act_payload = {
            "name": "Indian Penal Code",
            "short_name": "IPC",
            "year": 1860,
            "description": "Historical criminal code of India.",
        }
        res = c.post("/acts", json=act_payload, headers=inv_headers)
        assert res.status_code == 403, f"Expected 403, got {res.status_code}"
        print("RBAC check for creation passed (403 received).")

        print("Creating Act with Admin credentials...")
        res = c.post("/acts", json=act_payload, headers=admin_headers)
        assert res.status_code == 201, f"Failed to create act: {res.json()}"
        act_id = res.json()["act_id"]
        assert act_id.startswith("ACT-"), f"Unexpected ID format: {act_id}"
        print(f"Act created successfully. ID: {act_id}")

        # 4. Create Duplicate Act (Same short_name + year)
        print("Testing duplicate act creation (should fail)...")
        res = c.post("/acts", json=act_payload, headers=admin_headers)
        assert res.status_code == 409, f"Expected 409, got {res.status_code}"
        assert "is already registered" in res.json()["message"]
        print("Duplicate check passed (409 received).")

        # 5. Retrieve Act details
        print("Retrieving act details...")
        res = c.get(f"/acts/{act_id}", headers=inv_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "Indian Penal Code"
        assert data["short_name"] == "IPC"
        assert data["year"] == 1860
        print("Act details retrieved successfully.")

        # 6. Query/Search/Sorting/Pagination
        print("Testing query filters on acts...")
        res = c.get("/acts?short_name=ipc", headers=inv_headers)
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["short_name"] == "IPC"

        # Sorting
        print("Testing act sorting...")
        res = c.get("/acts?sort_by=year&sort_order=asc", headers=inv_headers)
        assert res.status_code == 200
        data = res.json()
        years = [a["year"] for a in data["items"]]
        assert years == sorted(years), f"Expected sorted years, got {years}"

        # 7. Update Act
        print("Updating Act...")
        update_payload = {
            "name": "Indian Penal Code Updated",
            "year": 1861,
        }
        res = c.put(f"/acts/{act_id}", json=update_payload, headers=admin_headers)
        assert res.status_code == 200
        data = res.json()
        assert data["name"] == "Indian Penal Code Updated"
        assert data["year"] == 1861
        print("Act updated successfully.")

        # 8. Delete Act (RBAC Check)
        print("Testing Act deletion RBAC (Investigator should be forbidden)...")
        res = c.delete(f"/acts/{act_id}", headers=inv_headers)
        assert res.status_code == 403
        print("RBAC check for deletion passed.")

        print("Deleting Act with Admin credentials...")
        res = c.delete(f"/acts/{act_id}", headers=admin_headers)
        assert res.status_code == 204

        # Verify deletion
        res = c.get(f"/acts/{act_id}", headers=inv_headers)
        assert res.status_code == 404
        print("Act deleted and verified absent.")

        print("🎉 All Act Management tests passed successfully! 🎉")


if __name__ == "__main__":
    run_tests()
