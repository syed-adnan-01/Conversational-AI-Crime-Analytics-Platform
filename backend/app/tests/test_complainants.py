import sys
from fastapi.testclient import TestClient

from app.main import app
from app.repository.case_repository import CaseRepository
from app.repository.complainant_repository import ComplainantRepository


def run_tests():
    print("Initializing TestClient...")
    client = TestClient(app)

    with client as c:
        print("TestClient active in lifespan context.")

        # 1. Login to retrieve token
        print("Attempting login...")
        login_res = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP001",
                "password": "password123",
                "department": "Cyber Crime",
            },
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.json()}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful. Token obtained.")

        # Clear existing data to ensure clean test state
        CaseRepository._cases.clear()
        ComplainantRepository._complainants.clear()

        # 2. Register a mock case first (Complainant requires a valid case)
        print("Registering mock case...")
        case_payload = {
            "crime_no": "CR-2026-9999",
            "crime_registered_date": "2026-07-18T10:30:00",
            "police_station_id": 101,
            "place_of_occurrence": "Indiranagar, Bengaluru",
            "brief_facts": "Theft of mobile phone from vehicle.",
        }
        case_res = c.post("/cases/", json=case_payload, headers=headers)
        assert (
            case_res.status_code == 201
        ), f"Failed to create case: {case_res.json()}"
        case_id = case_res.json()["case_master_id"]
        print(f"Mock case registered. ID: {case_id}")

        # 3. Create Complainant (Happy Path)
        print("Creating complainant...")
        complainant_payload = {
            "name": "Suresh Kumar",
            "gender": "Male",
            "age": 42,
            "mobile_no": "9876543210",
            "email": "suresh@example.com",
            "address": "123, 5th Cross, Bengaluru",
            "relationship_type": "Victim",
        }
        res = c.post(
            f"/cases/{case_id}/complainants",
            json=complainant_payload,
            headers=headers,
        )
        assert res.status_code == 201, f"Failed to create complainant: {res.json()}"
        comp_id = res.json()["complainant_id"]
        assert comp_id.startswith("CP-"), f"Unexpected ID format: {comp_id}"
        print(f"Complainant created successfully. ID: {comp_id}")

        # 4. Create Complainant with non-existent Case ID (Orphan check)
        print("Testing orphan complainant creation (should fail)...")
        res = c.post(
            "/cases/CM-NONEXISTENT/complainants",
            json=complainant_payload,
            headers=headers,
        )
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"
        assert "Case not found" in res.json()["message"]
        print("Orphan check passed (404 received).")

        # 5. Create Duplicate Complainant (Same Case, Name and Phone) (Duplicate check)
        print("Testing duplicate complainant (should fail)...")
        res = c.post(
            f"/cases/{case_id}/complainants",
            json=complainant_payload,
            headers=headers,
        )
        assert res.status_code == 409, f"Expected 409, got {res.status_code}"
        assert "is already registered for case" in res.json()["message"]
        print("Duplicate check passed (409 received).")

        # 6. Create Complainant with invalid mobile number
        print("Testing invalid mobile number format (should fail)...")
        invalid_phone_payload = complainant_payload.copy()
        invalid_phone_payload["name"] = "Different Name"
        invalid_phone_payload["mobile_no"] = "12345"
        res = c.post(
            f"/cases/{case_id}/complainants",
            json=invalid_phone_payload,
            headers=headers,
        )
        assert res.status_code == 422, f"Expected 422, got {res.status_code}"
        assert "Invalid mobile number format" in res.json()["message"]
        print("Invalid mobile number validation passed.")

        # 7. Create Complainant with invalid email format
        print("Testing invalid email format (should fail)...")
        invalid_email_payload = complainant_payload.copy()
        invalid_email_payload["name"] = "Different Name"
        invalid_email_payload["email"] = "not_an_email"
        res = c.post(
            f"/cases/{case_id}/complainants",
            json=invalid_email_payload,
            headers=headers,
        )
        assert res.status_code == 422, f"Expected 422, got {res.status_code}"
        assert "Invalid email format" in res.json()["message"]
        print("Invalid email format validation passed.")

        # 8. Retrieve complainant details
        print("Retrieving complainant details...")
        res = c.get(f"/complainants/{comp_id}", headers=headers)
        assert res.status_code == 200, f"Failed to get complainant: {res.json()}"
        data = res.json()
        assert data["name"] == "Suresh Kumar"
        assert data["mobile_no"] == "9876543210"
        assert data["email"] == "suresh@example.com"
        print("Complainant details retrieved successfully.")

        # 9. List case complainants
        print("Listing complainants for case...")
        res = c.get(f"/cases/{case_id}/complainants", headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "Suresh Kumar"
        print("List complainants verification passed.")

        # 10. Create second complainant for sorting/pagination tests
        print("Creating second complainant for sorting...")
        comp2_payload = {
            "name": "Abhishek Sharma",
            "gender": "Male",
            "age": 30,
            "mobile_no": "9887766554",
            "email": "abhishek@example.com",
            "address": "456, 10th Main, Bengaluru",
            "relationship_type": "Witness",
        }
        res = c.post(
            f"/cases/{case_id}/complainants", json=comp2_payload, headers=headers
        )
        assert res.status_code == 201
        comp2_id = res.json()["complainant_id"]

        # Sort by Name ASC (Abhishek first, Suresh second)
        res = c.get(
            f"/cases/{case_id}/complainants?sort_by=name&sort_order=asc",
            headers=headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) == 2
        assert data["items"][0]["name"] == "Abhishek Sharma"
        assert data["items"][1]["name"] == "Suresh Kumar"

        # Sort by Name DESC (Suresh first, Abhishek second)
        res = c.get(
            f"/cases/{case_id}/complainants?sort_by=name&sort_order=desc",
            headers=headers,
        )
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) == 2
        assert data["items"][0]["name"] == "Suresh Kumar"
        assert data["items"][1]["name"] == "Abhishek Sharma"

        # 11. Update Complainant
        print("Updating complainant...")
        update_payload = {
            "name": "Suresh Kumar Updated",
            "age": 43,
            "mobile_no": "9999988888",
        }
        res = c.put(
            f"/complainants/{comp_id}", json=update_payload, headers=headers
        )
        assert res.status_code == 200, f"Update failed: {res.json()}"
        data = res.json()
        assert data["name"] == "Suresh Kumar Updated"
        assert data["age"] == 43
        assert data["mobile_no"] == "9999988888"
        print("Complainant updated successfully.")

        # 12. Delete Complainant (RBAC and Happy Path)
        print("Testing delete complainant RBAC (investigator should be forbidden)...")
        res = c.delete(f"/complainants/{comp_id}", headers=headers)
        assert res.status_code == 403, f"Expected 403, got {res.status_code}"
        print("Delete RBAC test passed (403 received).")

        print("Logging in as supervisor to perform deletion...")
        login_sup = c.post(
            "/auth/login",
            json={
                "employee_id": "EMP003",
                "password": "password123",
                "department": "Investigation",
            },
        )
        assert login_sup.status_code == 200
        sup_token = login_sup.json()["access_token"]
        sup_headers = {"Authorization": f"Bearer {sup_token}"}

        print("Deleting complainant with supervisor credentials...")
        res = c.delete(f"/complainants/{comp_id}", headers=sup_headers)
        assert res.status_code == 204

        # Retrieve deleted complainant (should fail)
        res = c.get(f"/complainants/{comp_id}", headers=headers)
        assert res.status_code == 404
        print("Complainant deleted and verified absent.")

        print("🎉 All Complainant Management tests passed successfully! 🎉")


def test_complainants():
    run_tests()


if __name__ == "__main__":
    run_tests()
