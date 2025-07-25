"""
Health check tests for the application.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data  # Updated to match actual response structure
    assert "version" in data

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    # Update expectation to match actual response
    json_response = response.json()
    assert "message" in json_response
    assert "Qpesapay" in json_response["message"]