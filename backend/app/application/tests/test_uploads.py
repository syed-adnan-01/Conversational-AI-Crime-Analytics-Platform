import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.application.uploads.upload_router import router
from app.application.uploads.upload_storage import upload_metadata_repo
import io
import os

def get_test_app():
    app = FastAPI()
    app.include_router(router)
    return app

client = TestClient(get_test_app())

@pytest.fixture(autouse=True)
def clear_store():
    # Clear the in-memory metadata store before each test
    upload_metadata_repo._metadata.clear()
    # clean up test dir if needed

def test_empty_state():
    response = client.get("/uploads")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_success():
    file_content = b"fake pdf content"
    response = client.post(
        "/uploads",
        data={"category": "FIR documents"},
        files={"file": ("test.pdf", io.BytesIO(file_content), "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["category"] == "FIR documents"
    assert "file_id" in data

def test_upload_validation_fail_extension():
    file_content = b"fake exe content"
    response = client.post(
        "/uploads",
        data={"category": "FIR documents"},
        files={"file": ("test.exe", io.BytesIO(file_content), "application/x-msdownload")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

def test_listing_and_filtering():
    # Upload 1
    client.post(
        "/uploads",
        data={"category": "FIR documents", "case_id": "C1"},
        files={"file": ("test1.pdf", io.BytesIO(b"content"), "application/pdf")}
    )
    # Upload 2
    client.post(
        "/uploads",
        data={"category": "Evidence images", "case_id": "C2"},
        files={"file": ("test2.png", io.BytesIO(b"content"), "image/png")}
    )
    
    # List all
    resp_all = client.get("/uploads")
    assert len(resp_all.json()) == 2
    
    # Filter by category
    resp_cat = client.get("/uploads?category=Evidence images")
    assert len(resp_cat.json()) == 1
    assert resp_cat.json()[0]["filename"] == "test2.png"
    
    # Filter by case_id
    resp_case = client.get("/uploads?case_id=C1")
    assert len(resp_case.json()) == 1
    assert resp_case.json()[0]["filename"] == "test1.pdf"

def test_download():
    # Upload
    file_content = b"downloadable content"
    resp = client.post(
        "/uploads",
        data={"category": "FIR documents"},
        files={"file": ("test.pdf", io.BytesIO(file_content), "application/pdf")}
    )
    file_id = resp.json()["file_id"]
    
    # Download
    download_resp = client.get(f"/uploads/{file_id}/download")
    assert download_resp.status_code == 200
    assert download_resp.content == file_content

def test_delete():
    # Upload
    resp = client.post(
        "/uploads",
        data={"category": "FIR documents"},
        files={"file": ("test.pdf", io.BytesIO(b"content"), "application/pdf")}
    )
    file_id = resp.json()["file_id"]
    
    # Delete
    del_resp = client.delete(f"/uploads/{file_id}")
    assert del_resp.status_code == 204
    
    # Verify metadata is gone
    get_resp = client.get(f"/uploads/{file_id}")
    assert get_resp.status_code == 404
