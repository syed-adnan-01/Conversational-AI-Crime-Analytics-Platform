from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.timeline_repository import TimelineRepository


def run_tests():
    print("Initializing TestClient for Timeline...")
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

        # Clear existing repository data
        CaseRepository._cases.clear()
        TimelineRepository._events.clear()

        # 2. Register a mock case
        case_payload = {
            "crime_no": "CR-2026-TL01",
            "crime_registered_date": "2026-07-20T10:00:00",
            "police_station_id": 101,
            "place_of_occurrence": "M.G. Road, Bengaluru",
            "brief_facts": "Timeline test case",
        }
        case_res = c.post("/cases/", json=case_payload, headers=headers)
        assert case_res.status_code == 201
        case_id = case_res.json()["case_master_id"]

        # 3. Verify automatic CASE_CREATED timeline event
        tl_res = c.get(f"/cases/{case_id}/timeline", headers=headers)
        assert tl_res.status_code == 200
        tl_data = tl_res.json()
        assert len(tl_data["items"]) >= 1
        assert tl_data["items"][0]["event_type"] == "CASE_CREATED"

        # 4. Record a manual timeline event
        event_payload = {
            "event_type": "EVIDENCE_COLLECTED",
            "title": "Initial Scene Survey",
            "description": "Inspected crime location and gathered initial evidence.",
            "reference_id": case_id,
            "reference_type": "CaseMaster",
        }
        create_res = c.post(
            f"/cases/{case_id}/timeline",
            json=event_payload,
            headers=headers,
        )
        assert create_res.status_code == 201, f"Create timeline event failed: {create_res.json()}"
        event_id = create_res.json()["event_id"]
        assert event_id.startswith("EV-")

        # 5. Retrieve timeline event by ID
        get_res = c.get(f"/timeline/{event_id}", headers=headers)
        assert get_res.status_code == 200
        assert get_res.json()["title"] == "Initial Scene Survey"

        # 6. Verify chronological ordering
        list_res = c.get(f"/cases/{case_id}/timeline", headers=headers)
        assert list_res.status_code == 200
        items = list_res.json()["items"]
        assert len(items) >= 2

        print("🎉 Timeline tests passed successfully!")


def test_timeline():
    run_tests()


if __name__ == "__main__":
    run_tests()
