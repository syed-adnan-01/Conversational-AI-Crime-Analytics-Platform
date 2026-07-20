from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.witness_repository import WitnessRepository


def run_tests():
    print("Initializing TestClient for Witness Management...")
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
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Clear repository data
        CaseRepository._cases.clear()
        WitnessRepository._witnesses.clear()

        # 2. Register mock case
        case_res = c.post(
            "/cases/",
            json={
                "crime_no": "CR-2026-WIT01",
                "crime_registered_date": "2026-07-20T10:00:00",
                "police_station_id": 101,
            },
            headers=headers,
        )
        assert case_res.status_code == 201
        case_id = case_res.json()["case_master_id"]

        # 3. Create Witness
        witness_payload = {
            "name": "Ramesh Rao",
            "gender": "Male",
            "age": 45,
            "mobile_no": "9876543210",
            "email": "ramesh@example.com",
            "statement": "Saw suspect running away at 10 PM.",
            "is_hostile": False,
        }
        create_res = c.post(
            f"/cases/{case_id}/witnesses",
            json=witness_payload,
            headers=headers,
        )
        assert create_res.status_code == 201
        witness_id = create_res.json()["witness_id"]
        assert witness_id.startswith("WT-")

        # 4. Get Witness details
        get_res = c.get(f"/witnesses/{witness_id}", headers=headers)
        assert get_res.status_code == 200
        assert get_res.json()["name"] == "Ramesh Rao"

        # 5. List witnesses
        list_res = c.get(f"/cases/{case_id}/witnesses", headers=headers)
        assert list_res.status_code == 200
        assert len(list_res.json()["items"]) == 1

        # 6. Update Witness
        update_res = c.put(
            f"/witnesses/{witness_id}",
            json={"is_hostile": True},
            headers=headers,
        )
        assert update_res.status_code == 200
        assert update_res.json()["is_hostile"] is True

        # 7. Delete Witness RBAC check (investigator should fail)
        del_res = c.delete(f"/witnesses/{witness_id}", headers=headers)
        assert del_res.status_code == 403

        # Supervisor delete
        sup_login = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP003",
                "password": "password123",
                "department": "Investigation",
            },
        )
        sup_headers = {"Authorization": f"Bearer {sup_login.json()['access_token']}"}
        del_res2 = c.delete(f"/witnesses/{witness_id}", headers=sup_headers)
        assert del_res2.status_code == 204

        print("🎉 Witness Management tests passed successfully!")


def test_witnesses():
    run_tests()


if __name__ == "__main__":
    run_tests()
