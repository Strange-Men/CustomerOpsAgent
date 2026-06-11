"""Tests for health endpoint."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """GET /health returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "customerops-agent"
    assert data["mode"] == "mock"


def test_health_response_structure():
    """GET /health returns expected fields."""
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert "mode" in data
