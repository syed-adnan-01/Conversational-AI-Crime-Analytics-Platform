from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.accused_repository import AccusedRepository
from app.repository.arrest_repository import ArrestRepository


def run_tests():
    print("Initializing TestClient for Arrest Management...")
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
        ArrestRepository._arrests.clear()

        # 2. Register mock case & accused
        case_res = c.post(
            "/cases/",
            json={"crime_no": "CR-2026-ARR01", "crime_registered_date": "2026-07-20T10:00:00", "police_station_id": 101},
            headers=headers,
        )
        case_id = case_res.json()["case_master_id"]

        acc_res = c.post(
            f"/cases/{case_id}/accused",
            json={"name": "Vijay M", "gender": "Male", "age": 35, "mobile_no": "9876543210"},
            headers=headers,
        )
        accused_id = acc_res.json()["accused_id"]

        # 3. Create Arrest Record
        arrest_payload = {
            "accused_id": accused_id,
            "arrest_date": "2026-07-20T14:30:00",
            "arrest_location": "Airport Terminal 1, Bengaluru",
            "grounds_for_arrest": "Attempting to flee jurisdiction.",
            "arresting_officer": "Ins. Vikram",
            "status": "ARRESTED",
        }
        create_res = c.post(
            f"/cases/{case_id}/arrests",
            json=arrest_payload,
            headers=headers,
        )
        assert create_res.status_code == 201, f"Arrest create failed: {create_res.json()}"
        arrest_id = create_res.json()["arrest_id"]
        assert arrest_id.startswith("AR-")

        # 4. Get Arrest details
        get_res = c.get(f"/arrests/{arrest_id}", headers=headers)
        assert get_res.status_code == 200
        assert get_res.json()["accused_name"] == "Vijay M"

        # 5. List Arrests
        list_res = c.get(f"/cases/{case_id}/arrests", headers=headers)
        assert list_res.status_code == 200
        assert len(list_res.json()["items"]) == 1

        # 6. Update Arrest (e.g., granting bail)
        update_res = c.put(
            f"/arrests/{arrest_id}",
            json={"status": "RELEASED_ON_BAIL"},
            headers=headers,
        )
        assert update_res.status_code == 200
        assert update_res.json()["status"] == "RELEASED_ON_BAIL"

        # 7. Delete Arrest (Supervisor required)
        sup_login = c.post("/auth/login", json={"employee_id": "EMP003", "password": "password123", "department": "Investigation"})
        sup_headers = {"Authorization": f"Bearer {sup_login.json()['access_token']}"}
        del_res = c.delete(f"/arrests/{arrest_id}", headers=sup_headers)
        assert del_res.status_code == 204

        print("🎉 Arrest Management tests passed successfully!")


def test_arrests():
    run_tests()


if __name__ == "__main__":
    run_tests()
