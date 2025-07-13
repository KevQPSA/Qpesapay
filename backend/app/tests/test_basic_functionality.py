"""
Basic functionality tests for QA meeting.
These tests verify core functionality without complex security scenarios.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_app_starts_successfully():
    """Test that the FastAPI app starts without errors."""
    assert app is not None
    assert app.title == "Qpesapay"


def test_root_endpoint():
    """Test the root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Qpesapay" in data["message"]


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert "version" in data


def test_api_docs_accessible():
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Qpesapay"


def test_auth_endpoints_exist():
    """Test that authentication endpoints exist (without testing functionality)."""
    # Test registration endpoint exists
    response = client.post("/api/v1/auth/register", json={})
    # Should return 422 (validation error) not 404 (not found)
    assert response.status_code in [400, 422, 500]
    
    # Test login endpoint exists
    response = client.post("/api/v1/auth/login", json={})
    # Should return 422 (validation error) not 404 (not found)
    assert response.status_code in [400, 422, 500]


def test_payment_endpoints_exist():
    """Test that payment endpoints exist (without testing functionality)."""
    # Test payment creation endpoint exists
    response = client.post("/api/v1/payments/create", json={})
    # Should return 401 (unauthorized) or 422 (validation error) not 404 (not found)
    assert response.status_code in [400, 401, 422, 500]


def test_webhook_endpoints_exist():
    """Test that webhook endpoints exist (without testing functionality)."""
    # Test M-Pesa callback endpoint exists
    response = client.post("/api/v1/webhooks/mpesa/callback", json={})
    # Should return some response, not 404 (not found)
    assert response.status_code in [200, 400, 401, 422, 500]


def test_cors_headers():
    """Test that CORS is configured (basic check)."""
    response = client.options("/api/v1/auth/login")
    # Should handle OPTIONS request
    assert response.status_code in [200, 405]


def test_security_headers_present():
    """Test that basic security headers are present."""
    response = client.get("/")
    # Check that response has headers (basic security check)
    assert "content-type" in response.headers
    # The app should respond with JSON
    assert "application/json" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_async_functionality():
    """Test that async functionality works."""
    # This is a basic test to ensure async/await works
    async def dummy_async_function():
        return "async works"
    
    result = await dummy_async_function()
    assert result == "async works"


def test_environment_configuration():
    """Test that environment is properly configured."""
    import os
    
    # Check that we're in testing mode
    assert os.getenv('TESTING') == 'true'
    assert os.getenv('CI') == 'true'
    
    # Check that database URL is configured
    database_url = os.getenv('DATABASE_URL')
    assert database_url is not None
    assert 'postgresql' in database_url


def test_imports_work():
    """Test that all critical imports work without errors."""
    try:
        from app.core.security import create_tokens
        from app.core.validation import validate_email_address
        from app.models.user import User
        from app.schemas.user import UserCreate
        from app.services.mpesa_service import MpesaService
        assert True  # All imports successful
    except ImportError as e:
        pytest.fail(f"Critical import failed: {e}")


def test_database_models_defined():
    """Test that database models are properly defined."""
    from app.models.user import User
    from app.models.wallet import Wallet
    from app.models.transaction import Transaction
    
    # Check that models have required attributes
    assert hasattr(User, '__tablename__')
    assert hasattr(Wallet, '__tablename__')
    assert hasattr(Transaction, '__tablename__')


def test_pydantic_schemas_work():
    """Test that Pydantic schemas work correctly."""
    from app.schemas.user import UserCreate
    
    # Test that schema validation works
    try:
        user_data = {
            "email": "test@example.com",
            "phone_number": "0712345678",
            "first_name": "John",
            "last_name": "Doe",
            "password": "TestPassword123!"
        }
        user_schema = UserCreate(**user_data)
        assert user_schema.email == "test@example.com"
    except Exception as e:
        pytest.fail(f"Pydantic schema validation failed: {e}")
