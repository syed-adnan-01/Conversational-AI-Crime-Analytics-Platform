from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.court_proceeding_repository import CourtProceedingRepository


def run_tests():
    print("Initializing TestClient for Court Proceedings...")
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
        CourtProceedingRepository._proceedings.clear()

        # 2. Register mock case
        case_res = c.post("/cases/", json={"crime_no": "CR-2026-CRT01", "crime_registered_date": "2026-07-20T10:00:00", "police_station_id": 101}, headers=headers)
        case_id = case_res.json()["case_master_id"]

        # 3. Create Court Proceeding Record
        proceeding_payload = {
            "court_name": "Chief Metropolitan Magistrate Court",
            "judge_name": "Hon. Justice Anand",
            "stage": "COGNIZANCE",
            "hearing_date": "2026-07-20T11:00:00",
            "next_hearing_date": "2026-08-05T10:30:00",
            "summary": "Court took cognizance of the chargesheet filed by police.",
            "order_passed": "Summons issued to accused.",
        }
        create_res = c.post(f"/cases/{case_id}/court-proceedings", json=proceeding_payload, headers=headers)
        assert create_res.status_code == 201, f"Proceeding create failed: {create_res.json()}"
        proceeding_id = create_res.json()["proceeding_id"]
        assert proceeding_id.startswith("CP-")

        # 4. Get Proceeding details
        get_res = c.get(f"/court-proceedings/{proceeding_id}", headers=headers)
        assert get_res.status_code == 200
        assert get_res.json()["stage"] == "COGNIZANCE"

        # 5. List Proceedings for case
        list_res = c.get(f"/cases/{case_id}/court-proceedings", headers=headers)
        assert list_res.status_code == 200
        assert len(list_res.json()["items"]) == 1

        # 6. Update Proceeding
        update_res = c.put(f"/court-proceedings/{proceeding_id}", json={"stage": "CHARGE_FRAMING"}, headers=headers)
        assert update_res.status_code == 200
        assert update_res.json()["stage"] == "CHARGE_FRAMING"

        # 7. Delete Proceeding (Supervisor required)
        sup_login = c.post("/auth/login", json={"employee_id": "EMP003", "password": "password123", "department": "Investigation"})
        sup_headers = {"Authorization": f"Bearer {sup_login.json()['access_token']}"}
        del_res = c.delete(f"/court-proceedings/{proceeding_id}", headers=sup_headers)
        assert del_res.status_code == 204

        print("🎉 Court Proceedings tests passed successfully!")


def test_court_proceedings():
    run_tests()


if __name__ == "__main__":
    run_tests()
