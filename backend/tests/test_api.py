import pytest
import os
import sys

# Ensure backend path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_admin_login_success():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "Admin@12345"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == "admin"

def test_admin_login_failure():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "WrongPassword"})
    assert response.status_code == 401

def test_public_announcements():
    response = client.get("/api/content/announcements")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_public_leadership():
    response = client.get("/api/committees/leadership")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_public_professionals():
    response = client.get("/api/professionals/list")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_membership_application_submission():
    import time
    unique_mobile = f"0344{int(time.time()) % 10000000:07d}"
    payload = {
        "full_name_ur": "امتحان خان",
        "full_name_en": "Imtihan Khan",
        "father_name_ur": "امتحان گل",
        "mobile_number": unique_mobile,
        "current_city": "Karachi",
        "current_area": "Manghopir",
        "ancestral_region": "Shangla",
        "ancestral_village": "Alpuri",
        "occupation": "استاد",
        "professional_category": "Teacher",
        "declaration_accepted": True
    }
    response = client.post("/api/members/apply", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "APP-" in data["application_number"]
    assert data["status"] == "PENDING"

def test_status_lookup():
    response = client.get("/api/members/status/03001234567")
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True

def test_card_public_verification():
    # Fetch token from existing member
    status_resp = client.get("/api/members/status/03001234567")
    token = status_resp.json()["card"]["verification_token"]
    
    verify_resp = client.get(f"/api/cards/verify/{token}")
    assert verify_resp.status_code == 200
    v_data = verify_resp.json()
    assert v_data["is_valid"] is True
    assert "MKQI-" in v_data["membership_id"]
    # Verify privacy preservation (no private phone or address leaked)
    assert "mobile_number" not in v_data
