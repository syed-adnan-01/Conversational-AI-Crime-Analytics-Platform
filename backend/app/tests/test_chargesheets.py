from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.section_repository import SectionRepository
from app.repository.evidence_repository import EvidenceRepository
from app.repository.chargesheet_repository import ChargesheetRepository


def run_tests():
    print("Initializing TestClient for Chargesheet Management...")
    client = TestClient(app)

    with client as c:
        # 1. Login
        login_res = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Clear repositories
        CaseRepository._cases.clear()
        AccusedRepository._accused.clear()
        SectionRepository._sections.clear()
        EvidenceRepository._evidence_list.clear()
        ChargesheetRepository._chargesheets.clear()

        # 2. Register mock dependencies
        case_res = c.post("/cases/", json={"crime_no": "CR-2026-CHG01", "crime_registered_date": "2026-07-20T10:00:00", "police_station_id": 101}, headers=headers)
        case_id = case_res.json()["case_master_id"]

        acc_res = c.post(f"/cases/{case_id}/accused", json={"name": "Rajesh K", "gender": "Male", "age": 29, "mobile_no": "9876543210"}, headers=headers)
        accused_id = acc_res.json()["accused_id"]

        # Inject admin user for creating acts & sections
        admin_login = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP003",
                "password": "password123",
                "department": "Investigation",
            },
        )
        admin_token = admin_login.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        act_res = c.post("/acts", json={"name": "Indian Penal Code", "short_name": "IPC", "year": 1860}, headers=admin_headers)
        act_id = act_res.json()["act_id"]

        sec_res = c.post(f"/sections?act_id={act_id}", json={"section_number": "379", "title": "Punishment for theft"}, headers=admin_headers)
        section_id = sec_res.json()["section_id"]

        ev_res = c.post(
            f"/cases/{case_id}/evidence",
            json={
                "title": "Stolen Phone",
                "description": "Recovered iPhone 14 Pro",
                "evidence_type": "DIGITAL_DEVICE",
                "collected_by": "Ins. Ramesh",
                "collection_date": "2026-07-20T11:00:00",
                "collection_location": "MG Road",
                "storage_location": "Locker A1",
            },
            headers=headers,
        )
        evidence_id = ev_res.json()["evidence_id"]

        # 3. Create Chargesheet
        chargesheet_payload = {
            "chargesheet_number": "CS-2026-0001",
            "filing_date": "2026-07-20T16:00:00",
            "investigating_officer": "Ins. Ramesh",
            "summary": "Investigation completed. Evidence gathered linking accused to crime.",
            "status": "FILED",
            "accused_links": [
                {
                    "accused_id": accused_id,
                    "charges_summary": "IPC 379 Theft",
                }
            ],
            "evidence_links": [
                {
                    "evidence_id": evidence_id,
                    "relevance_notes": "Key physical evidence recovered from accused possession.",
                }
            ],
            "section_links": [
                {
                    "section_id": section_id,
                    "offence_details": "Primary theft charge.",
                }
            ],
        }

        create_res = c.post(f"/cases/{case_id}/chargesheets", json=chargesheet_payload, headers=headers)
        assert create_res.status_code == 201, f"Chargesheet create failed: {create_res.json()}"
        chargesheet_id = create_res.json()["chargesheet_id"]
        assert chargesheet_id.startswith("CS-")

        # 4. Get Chargesheet details
        get_res = c.get(f"/chargesheets/{chargesheet_id}", headers=headers)
        assert get_res.status_code == 200
        cs_data = get_res.json()
        assert cs_data["chargesheet_number"] == "CS-2026-0001"
        assert len(cs_data["accused"]) == 1
        assert cs_data["accused"][0]["accused_name"] == "Rajesh K"

        # 5. List Chargesheets for case
        list_res = c.get(f"/cases/{case_id}/chargesheets", headers=headers)
        assert list_res.status_code == 200
        assert len(list_res.json()["items"]) == 1

        # 6. Update Chargesheet
        update_res = c.put(f"/chargesheets/{chargesheet_id}", json={"summary": "Updated summary after court submission."}, headers=headers)
        assert update_res.status_code == 200
        assert update_res.json()["summary"] == "Updated summary after court submission."

        # 7. Delete Chargesheet (Supervisor required)
        sup_login = c.post("/auth/login", json={"employee_id": "EMP003", "password": "password123", "department": "Investigation"})
        sup_headers = {"Authorization": f"Bearer {sup_login.json()['access_token']}"}
        del_res = c.delete(f"/chargesheets/{chargesheet_id}", headers=sup_headers)
        assert del_res.status_code == 204

        print("🎉 Chargesheet Management tests passed successfully!")


def test_chargesheets():
    run_tests()


if __name__ == "__main__":
    run_tests()
