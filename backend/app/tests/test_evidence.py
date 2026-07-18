import sys
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.victim_repository import VictimRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.section_repository import SectionRepository
from app.repository.act_repository import ActRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.user_repository import UserRepository
from app.core.password import PasswordManager
from app.core.roles import UserRole
from app.models.victim import Victim
from app.models.accused import Accused
from app.common.enums import Gender, IdentificationType


def run_tests():
    print("Initializing TestClient for Evidence Management...")
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

        # 1. Login roles
        print("Logging in roles...")
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

        login_ana = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP002",
                "password": "password123",
                "department": "Crime Analytics",
            },
        )
        ana_headers = {"Authorization": f"Bearer {login_ana.json()['access_token']}"}

        # Clear repositories to start fresh
        CaseRepository._cases.clear()
        VictimRepository._victims.clear()
        AccusedRepository._accused.clear()
        ActRepository._acts.clear()
        ActRepository.initialize()
        SectionRepository._sections.clear()
        SectionRepository.initialize()
        EvidenceRepository._evidence_list.clear()

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

        # 3. Inject mock Victim and Accused
        print("Injecting mock Victim and Accused...")
        mock_victim = Victim(
            victim_id="VT-VICTIM123",
            case_master_id=case_id,
            name="John Doe",
            gender=Gender.MALE,
            age=34,
            mobile_no="9876543210",
            email="johndoe@email.com",
            nationality="Indian",
            occupation="Engineer",
            id_type=IdentificationType.AADHAAR,
            id_number="1234-5678-9012",
        )
        VictimRepository.create_victim(mock_victim)

        mock_accused = Accused(
            accused_id="AC-ACCUSED123",
            case_master_id=case_id,
            name="Jane Criminal",
            gender=Gender.FEMALE,
            age=28,
            mobile_no="9123456780",
            email="jane@criminal.com",
            nationality="Indian",
            occupation="Unemployed",
            id_type=IdentificationType.PASSPORT,
            id_number="A1234567",
        )
        AccusedRepository.create_accused(mock_accused)

        # Get seeded section
        sections_res = c.get("/sections?section_number=66D", headers=inv_headers)
        assert sections_res.status_code == 200
        sec_items = sections_res.json()["items"]
        assert len(sec_items) > 0
        section_id = sec_items[0]["section_id"]

        # 4. Register Evidence (Investigator - Success)
        print("Registering new evidence (Investigator)...")
        evidence_payload = {
            "evidence_number": "EVN-2026-9999",
            "title": "Suspect Laptop",
            "description": "Dell XPS 15 laptop retrieved from suspect residence.",
            "evidence_type": "DIGITAL_DEVICE",
            "evidence_category": "Digital",
            "status": "COLLECTED",
            "custody_status": "In Custody",
            "collected_by": "Inspector Sharma",
            "collection_date": "2026-07-18T14:30:00",
            "collection_location": "Suspect House, Bengaluru",
            "storage_location": "Locker A-1, Bengaluru Police Station",
            "storage_key": "evidence/2026/laptop.img",
            "mime_type": "application/octet-stream",
            "file_size": 512000000000,
            "checksum": "d131dd02c5e6e4cedd3408a68e8e66e86663f707f168cdff80891d4e08210332",
            "checksum_algorithm": "SHA-256",
            "remarks": "Contains suspect login credentials.",
            "victim_id": "VT-VICTIM123",
            "accused_id": "AC-ACCUSED123",
            "section_id": section_id,
        }

        res = c.post(f"/cases/{case_id}/evidence", json=evidence_payload, headers=inv_headers)
        assert res.status_code == 201, f"Failed to register evidence: {res.json()}"
        evidence_id = res.json()["evidence_id"]
        assert evidence_id.startswith("EV-")
        print(f"Evidence registered successfully. ID: {evidence_id}")

        # 5. Check auto-generation of evidence number
        print("Testing auto-generation of evidence number...")
        auto_payload = evidence_payload.copy()
        auto_payload["evidence_number"] = None
        auto_payload["title"] = "Suspect Phone"
        auto_payload["storage_key"] = None
        res_auto = c.post(f"/cases/{case_id}/evidence", json=auto_payload, headers=inv_headers)
        assert res_auto.status_code == 201
        auto_data = res_auto.json()
        assert auto_data["evidence_number"].startswith("EVN-")
        print(f"Auto-generated evidence number is: {auto_data['evidence_number']}")

        # 6. Test duplicate detection (same evidence_number under same case)
        print("Testing duplicate evidence number detection...")
        res = c.post(f"/cases/{case_id}/evidence", json=evidence_payload, headers=inv_headers)
        assert res.status_code == 409
        print("Duplicate evidence number check passed (409).")

        # 7. Test referential integrity
        print("Testing referential integrity (non-existent Case)...")
        res = c.post("/cases/CM-NONEXISTENT/evidence", json=evidence_payload, headers=inv_headers)
        assert res.status_code == 404

        print("Testing referential integrity (non-existent Victim)...")
        bad_victim_payload = evidence_payload.copy()
        bad_victim_payload["evidence_number"] = "EVN-2026-BAD1"
        bad_victim_payload["victim_id"] = "VT-NONEXISTENT"
        res = c.post(f"/cases/{case_id}/evidence", json=bad_victim_payload, headers=inv_headers)
        assert res.status_code == 404

        print("Testing referential integrity (non-existent Accused)...")
        bad_accused_payload = evidence_payload.copy()
        bad_accused_payload["evidence_number"] = "EVN-2026-BAD2"
        bad_accused_payload["accused_id"] = "AC-NONEXISTENT"
        res = c.post(f"/cases/{case_id}/evidence", json=bad_accused_payload, headers=inv_headers)
        assert res.status_code == 404

        print("Testing referential integrity (non-existent Section)...")
        bad_section_payload = evidence_payload.copy()
        bad_section_payload["evidence_number"] = "EVN-2026-BAD3"
        bad_section_payload["section_id"] = "SEC-NONEXISTENT"
        res = c.post(f"/cases/{case_id}/evidence", json=bad_section_payload, headers=inv_headers)
        assert res.status_code == 404
        print("Referential integrity checks passed.")

        # 8. Test collection date validation (cannot be in the future)
        print("Testing collection date in future...")
        future_date = (datetime.now() + timedelta(days=2)).isoformat()
        future_payload = evidence_payload.copy()
        future_payload["evidence_number"] = "EVN-2026-FUTURE"
        future_payload["collection_date"] = future_date
        res = c.post(f"/cases/{case_id}/evidence", json=future_payload, headers=inv_headers)
        assert res.status_code in [400, 422], f"Expected 400 or 422, got {res.status_code}"
        print("Future collection date validation passed.")

        # 9. Test GET /evidence/{evidence_id} and de-normalized fields
        print("Retrieving evidence details...")
        res = c.get(f"/evidence/{evidence_id}", headers=ana_headers)
        assert res.status_code == 200
        details = res.json()
        assert details["title"] == "Suspect Laptop"
        assert details["victim_name"] == "John Doe"
        assert details["accused_name"] == "Jane Criminal"
        assert details["section_number"] == "66D"
        assert details["act_short_name"] == "IT Act"
        print("De-normalized details verified successfully.")

        # 10. Test GET /cases/{case_id}/evidence with explicit query filters & search
        print("Testing query searches and filters...")
        # 10a. Filter by evidence_type
        res = c.get(f"/cases/{case_id}/evidence?evidence_type=DIGITAL_DEVICE", headers=inv_headers)
        assert res.status_code == 200
        assert len(res.json()["items"]) >= 1

        # 10b. Filter by status
        res = c.get(f"/cases/{case_id}/evidence?status=COLLECTED", headers=inv_headers)
        assert res.status_code == 200
        assert len(res.json()["items"]) >= 1

        # 10c. Search by title (keyword)
        res = c.get(f"/cases/{case_id}/evidence?title=Laptop", headers=inv_headers)
        assert res.status_code == 200
        assert len(res.json()["items"]) == 1

        # 10d. Filter by related entity (victim_id)
        res = c.get(f"/cases/{case_id}/evidence?victim_id=VT-VICTIM123", headers=inv_headers)
        assert res.status_code == 200
        assert len(res.json()["items"]) == 1
        print("Query search and filters passed.")

        # 11. Test PUT /evidence/{evidence_id} (Update details)
        print("Updating evidence...")
        update_payload = {
            "title": "Suspect Laptop - Red Hat Enterprise Installed",
            "status": "SEALED",
            "custody_status": "Sealed",
            "remarks": "Investigator noted checksum verification matches original.",
        }
        res = c.put(f"/evidence/{evidence_id}", json=update_payload, headers=inv_headers)
        assert res.status_code == 200
        updated_data = res.json()
        assert updated_data["title"] == "Suspect Laptop - Red Hat Enterprise Installed"
        assert updated_data["status"] == "SEALED"
        assert updated_data["custody_status"] == "Sealed"
        assert updated_data["remarks"] == "Investigator noted checksum verification matches original."
        print("Evidence details updated successfully.")

        # 12. Test DELETE /evidence/{evidence_id} (RBAC check)
        print("Testing deletion RBAC (Investigator should be forbidden)...")
        res = c.delete(f"/evidence/{evidence_id}", headers=inv_headers)
        assert res.status_code == 403

        print("Deleting evidence with Supervisor credentials...")
        res = c.delete(f"/evidence/{evidence_id}", headers=sup_headers)
        assert res.status_code == 204

        # Verify removal
        res = c.get(f"/evidence/{evidence_id}", headers=inv_headers)
        assert res.status_code == 404
        print("Evidence deletion and RBAC verified successfully.")

        print("🎉 All Evidence Management tests passed successfully! 🎉")


if __name__ == "__main__":
    run_tests()
