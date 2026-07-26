import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.application.notifications.notification_router import router
from app.application.notifications.notification_store import notification_store

def get_test_app():
    app = FastAPI()
    app.include_router(router)
    return app

client = TestClient(get_test_app())

@pytest.fixture(autouse=True)
def clear_store():
    # Clear the in-memory store before each test
    notification_store._notifications.clear()

def test_empty_state():
    response = client.get("/notifications")
    assert response.status_code == 200
    assert response.json() == []

def test_create_notification():
    payload = {
        "title": "Test Note",
        "message": "This is a test",
        "category": "SYSTEM",
        "priority": "HIGH",
        "source": "Tests"
    }
    response = client.post("/notifications/internal/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["read"] is False
    assert "notification_id" in data

def test_list_notifications():
    payload = {
        "title": "Test Note",
        "message": "This is a test",
        "category": "SYSTEM",
        "priority": "HIGH",
        "source": "Tests"
    }
    client.post("/notifications/internal/create", json=payload)
    
    response = client.get("/notifications")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_unread_filtering():
    client.post("/notifications/internal/create", json={
        "title": "Note 1", "message": "msg", "category": "SYSTEM", "priority": "LOW", "source": "s1"
    })
    resp = client.post("/notifications/internal/create", json={
        "title": "Note 2", "message": "msg", "category": "SYSTEM", "priority": "LOW", "source": "s1"
    })
    note_id = resp.json()["notification_id"]
    
    # Mark second as read
    client.post(f"/notifications/read/{note_id}")
    
    unread_resp = client.get("/notifications/unread")
    assert unread_resp.status_code == 200
    assert len(unread_resp.json()) == 1
    assert unread_resp.json()[0]["title"] == "Note 1"

def test_mark_all_read():
    client.post("/notifications/internal/create", json={
        "title": "Note 1", "message": "msg", "category": "SYSTEM", "priority": "LOW", "source": "s1"
    })
    client.post("/notifications/internal/create", json={
        "title": "Note 2", "message": "msg", "category": "SYSTEM", "priority": "LOW", "source": "s1"
    })
    
    response = client.post("/notifications/read-all")
    assert response.status_code == 200
    
    unread_resp = client.get("/notifications/unread")
    assert len(unread_resp.json()) == 0

def test_delete_notification():
    resp = client.post("/notifications/internal/create", json={
        "title": "Note 1", "message": "msg", "category": "SYSTEM", "priority": "LOW", "source": "s1"
    })
    note_id = resp.json()["notification_id"]
    
    del_resp = client.delete(f"/notifications/{note_id}")
    assert del_resp.status_code == 204
    
    get_resp = client.get("/notifications")
    assert len(get_resp.json()) == 0

def test_count_endpoint():
    client.post("/notifications/internal/create", json={
        "title": "Note 1", "message": "msg", "category": "SYSTEM", "priority": "LOW", "source": "s1"
    })
    
    count_resp = client.get("/notifications/count")
    data = count_resp.json()
    assert data["total"] == 1
    assert data["unread"] == 1
