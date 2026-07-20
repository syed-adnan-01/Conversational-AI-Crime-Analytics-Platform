import sys
from fastapi.testclient import TestClient

from app.main import app
from app.repository.act_repository import ActRepository
from app.repository.section_repository import SectionRepository
from app.repository.user_repository import UserRepository
from app.core.password import PasswordManager
from app.core.roles import UserRole


def run_tests():
    print("Initializing TestClient for Sections...")
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

        # 1. Login as Admin & Investigator
        print("Logging in...")
        login_admin = c.post(
            "/auth/login",
            json={
                "employee_id": admin_employee_id,
                "password": admin_password,
                "department": admin_department,
            },
        )
        assert login_admin.status_code == 200
        admin_headers = {"Authorization": f"Bearer {login_admin.json()['access_token']}"}

        login_inv = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        assert login_inv.status_code == 200
        inv_headers = {"Authorization": f"Bearer {login_inv.json()['access_token']}"}

        # Clear non-seed sections by resetting repositories
        ActRepository._acts.clear()
        ActRepository.initialize()
        SectionRepository._sections.clear()
        SectionRepository.initialize()

        # 2. Verify Seeded Sections
        print("Checking seeded sections...")
        res = c.get("/sections", headers=inv_headers)
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) >= 4, f"Expected at least 4 seeded sections, got {len(data['items'])}"
        
        # Verify specific section
        sec_numbers = [s["section_number"] for s in data["items"]]
        assert "103" in sec_numbers
        assert "303" in sec_numbers
        print("Seeded sections verification passed.")

        # Get parent Act ID for BNS (we will link new section to it)
        acts_res = c.get("/acts?short_name=bns", headers=inv_headers)
        bns_act_id = acts_res.json()["items"][0]["act_id"]

        # 3. Create Section (RBAC Check)
        print("Testing Section creation RBAC (Investigator should be forbidden)...")
        section_payload = {
            "section_number": " 304 / A ",
            "title": "Death by negligence",
            "description": "Punishment for causing death by negligence.",
            "is_cognizable": True,
            "is_bailable": True,
            "maximum_punishment": "Imprisonment up to 2 years, or with fine, or with both",
        }
        res = c.post(f"/sections?act_id={bns_act_id}", json=section_payload, headers=inv_headers)
        assert res.status_code == 403
        print("RBAC check passed.")

        print("Creating Section with Admin credentials...")
        res = c.post(f"/sections?act_id={bns_act_id}", json=section_payload, headers=admin_headers)
        assert res.status_code == 201, f"Failed to create section: {res.json()}"
        section_id = res.json()["section_id"]
        assert section_id.startswith("SEC-"), f"Unexpected ID format: {section_id}"
        
        # Check normalization (section_number " 304 / A " should normalize to "304A")
        assert res.json()["section_number"] == "304A"
        print(f"Section created and normalized successfully. ID: {section_id}")

        # 4. Create Section with non-existent Act ID
        print("Testing section creation with invalid Act ID (should fail)...")
        res = c.post("/sections?act_id=ACT-NONEXISTENT", json=section_payload, headers=admin_headers)
        assert res.status_code == 404
        print("Invalid Act ID check passed.")

        # 5. Create Duplicate Section (Same Act ID, same normalized section_number)
        print("Testing duplicate section creation (should fail)...")
        res = c.post(f"/sections?act_id={bns_act_id}", json=section_payload, headers=admin_headers)
        assert res.status_code == 409
        print("Duplicate section check passed.")

        # 6. List Sections under Act
        print("Testing list sections under specific Act...")
        res = c.get(f"/acts/{bns_act_id}/sections", headers=inv_headers)
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) >= 3  # 103, 303 seeded + 304A added
        print("List sections under Act endpoint passed.")

        # 7. Update Section
        print("Updating Section...")
        update_payload = {
            "title": "Death by negligence Updated",
            "is_bailable": False,
        }
        res = c.put(f"/sections/{section_id}", json=update_payload, headers=admin_headers)
        assert res.status_code == 200
        assert res.json()["title"] == "Death by negligence Updated"
        assert res.json()["is_bailable"] is False
        print("Section updated successfully.")

        # 8. Delete Section
        print("Deleting Section...")
        res = c.delete(f"/sections/{section_id}", headers=admin_headers)
        assert res.status_code == 204

        # Verify deletion
        res = c.get(f"/sections/{section_id}", headers=inv_headers)
        assert res.status_code == 404
        print("Section deleted and verified absent.")

        print("🎉 All Section Management tests passed successfully! 🎉")


def test_sections():
    run_tests()


if __name__ == "__main__":
    run_tests()
