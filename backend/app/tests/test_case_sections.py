import sys
from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.act_repository import ActRepository
from app.repository.section_repository import SectionRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.user_repository import UserRepository
from app.core.password import PasswordManager
from app.core.roles import UserRole


def run_tests():
    print("Initializing TestClient for Case Section Associations...")
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

        # 1. Login as Admin, Supervisor, and Investigator
        print("Logging in...")
        login_admin = c.post(
            "/auth/login",
            json={
                "employee_id": admin_employee_id,
                "password": admin_password,
                "department": admin_department,
            },
        )
        admin_headers = {"Authorization": f"Bearer {login_admin.json()['access_token']}"}

        login_sup = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP003",
                "password": "password123",
                "department": "Investigation",
            },
        )
        sup_headers = {"Authorization": f"Bearer {login_sup.json()['access_token']}"}

        login_inv = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        inv_headers = {"Authorization": f"Bearer {login_inv.json()['access_token']}"}

        # Clear repositories to start with fresh case & seed acts/sections
        CaseRepository._cases.clear()
        ActRepository._acts.clear()
        ActRepository.initialize()
        SectionRepository._sections.clear()
        SectionRepository.initialize()
        CaseSectionRepository._associations.clear()

        # 2. Register mock case
        print("Registering mock case...")
        case_payload = {
            "crime_no": "CR-2026-1111",
            "crime_registered_date": "2026-07-18T10:30:00",
            "police_station_id": 101,
            "place_of_occurrence": "M.G. Road, Bengaluru",
            "brief_facts": "Cyber fraud case.",
        }
        case_res = c.post("/cases/", json=case_payload, headers=inv_headers)
        assert case_res.status_code == 201
        case_id = case_res.json()["case_master_id"]
        print(f"Mock case registered. ID: {case_id}")

        # Get seeded Section ID (e.g. SEC-IT66D)
        sections_res = c.get("/sections?section_number=66D", headers=inv_headers)
        assert sections_res.status_code == 200
        sec_items = sections_res.json()["items"]
        assert len(sec_items) > 0
        section_id = sec_items[0]["section_id"]
        print(f"Section 66D found. ID: {section_id}")

        # 3. Assign Section to Case (Investigator role check - allowed)
        print("Assigning Section to Case...")
        link_payload = {
            "section_id": section_id,
            "remarks": "Primary cyber crime section applied.",
        }
        res = c.post(f"/cases/{case_id}/sections", json=link_payload, headers=inv_headers)
        assert res.status_code == 201, f"Failed to assign section: {res.json()}"
        association_id = res.json()["association_id"]
        assert association_id.startswith("CSA-"), f"Unexpected ID format: {association_id}"
        print(f"Section assigned successfully. Association ID: {association_id}")

        # 4. Attempt duplicate assignment
        print("Testing duplicate section assignment (should fail)...")
        res = c.post(f"/cases/{case_id}/sections", json=link_payload, headers=inv_headers)
        assert res.status_code == 409
        print("Duplicate assignment check passed.")

        # 5. Assign to non-existent Case ID
        print("Testing assignment to invalid Case ID...")
        res = c.post("/cases/CM-NONEXISTENT/sections", json=link_payload, headers=inv_headers)
        assert res.status_code == 404
        print("Invalid Case ID check passed.")

        # 6. Assign non-existent Section ID
        print("Testing assignment of invalid Section ID...")
        res = c.post(f"/cases/{case_id}/sections", json={"section_id": "SEC-NONEXISTENT"}, headers=inv_headers)
        assert res.status_code == 404
        print("Invalid Section ID check passed.")

        # 7. List Case Sections & Verify Premium De-normalized fields
        print("Listing case sections...")
        res = c.get(f"/cases/{case_id}/sections", headers=inv_headers)
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) == 1
        item = data["items"][0]
        assert item["association_id"] == association_id
        # Check de-normalized fields
        assert item["section_number"] == "66D"
        assert item["act_short_name"] == "IT Act"
        assert item["act_year"] == 2000
        assert item["is_cognizable"] is True
        assert item["is_bailable"] is True
        print("List case sections with expanded details passed.")

        # 8. Unassign Section Assignment (RBAC Check)
        print("Testing unassign section RBAC (Investigator should be forbidden)...")
        res = c.delete(f"/cases/{case_id}/sections/{association_id}", headers=inv_headers)
        assert res.status_code == 403
        print("RBAC check passed.")

        print("Deleting assignment with Supervisor credentials...")
        res = c.delete(f"/cases/{case_id}/sections/{association_id}", headers=sup_headers)
        assert res.status_code == 204

        # Verify removal
        res = c.get(f"/cases/{case_id}/sections", headers=inv_headers)
        assert len(res.json()["items"]) == 0
        print("Assignment removed successfully.")

        print("🎉 All Case-Section Association tests passed successfully! 🎉")


def test_case_sections():
    run_tests()


if __name__ == "__main__":
    run_tests()
