from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.officer_repository import OfficerRepository


def run_tests():
    print("Initializing TestClient for Officer Master & Assignment...")
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
        OfficerRepository._officers.clear()
        OfficerRepository._assignments.clear()

        # 2. Register Officer Master Record
        officer_payload = {
            "badge_number": "KA-POL-8842",
            "name": "Inspector Ramesh",
            "rank": "Inspector",
            "department": "Cyber Crime",
            "police_station_id": 101,
            "mobile_no": "9876543210",
            "email": "ramesh.pol@karnataka.gov.in",
        }
        create_off = c.post("/officers", json=officer_payload, headers=headers)
        assert create_off.status_code == 201, f"Officer create failed: {create_off.json()}"
        officer_id = create_off.json()["officer_id"]
        assert officer_id.startswith("OFF-")

        # Get Officer
        get_off = c.get(f"/officers/{officer_id}", headers=headers)
        assert get_off.status_code == 200
        assert get_off.json()["badge_number"] == "KA-POL-8842"

        # List Officers
        list_off = c.get("/officers", headers=headers)
        assert list_off.status_code == 200
        assert len(list_off.json()) == 1

        # 3. Create Case & Assign Officer
        case_res = c.post(
            "/cases/",
            json={"crime_no": "CR-2026-OFF01", "crime_registered_date": "2026-07-20T10:00:00", "police_station_id": 101},
            headers=headers,
        )
        case_id = case_res.json()["case_master_id"]

        assign_payload = {
            "officer_id": officer_id,
            "role": "Investigating Officer",
            "assigned_date": "2026-07-20T11:00:00",
            "remarks": "Assigned primary lead.",
        }
        assign_res = c.post(f"/cases/{case_id}/officer-assignments", json=assign_payload, headers=headers)
        assert assign_res.status_code == 201, f"Assignment create failed: {assign_res.json()}"
        assignment_id = assign_res.json()["assignment_id"]
        assert assignment_id.startswith("OA-")

        # 4. List assignments for case
        list_asg = c.get(f"/cases/{case_id}/officer-assignments", headers=headers)
        assert list_asg.status_code == 200
        assert len(list_asg.json()["items"]) == 1
        assert list_asg.json()["items"][0]["officer_name"] == "Inspector Ramesh"

        # 5. Relieve Officer Assignment
        relieve_res = c.put(
            f"/cases/{case_id}/officer-assignments/{assignment_id}",
            json={"relieved_date": "2026-07-21T18:00:00", "is_active": False, "remarks": "Case transferred."},
            headers=headers,
        )
        assert relieve_res.status_code == 200
        assert relieve_res.json()["is_active"] is False

        print("🎉 Officer Master & Assignment tests passed successfully!")


def test_officers():
    run_tests()


if __name__ == "__main__":
    run_tests()
