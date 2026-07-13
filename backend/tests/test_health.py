import os

os.environ["DATABASE_URL"] = "sqlite:///./test_aivoa_crm.db"

from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_seeded_hcps_are_searchable():
    with TestClient(app) as client:
        response = client.get("/api/hcps", params={"q": "Cardiology"})
        assert response.status_code == 200
        assert response.json()[0]["name"] == "Dr. Sarah Mitchell"
