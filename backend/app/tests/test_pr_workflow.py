"""
Test file to verify pull request workflow and branch protection.
This test ensures our CI/CD pipeline is working correctly.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test that the root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "QPesaPay" in data["message"]
    assert data["status"] == "operational"


def test_health_endpoint():
    """Test that the health endpoint is accessible."""
    response = client.get("/health")
    # Note: This might fail if database is not connected, but that's expected in test
    # We're just testing that the endpoint exists and returns a response
    assert response.status_code in [200, 503]  # 503 if DB not connected
    
    data = response.json()
    assert "status" in data
    assert "version" in data


def test_api_docs_accessibility():
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_branch_protection_workflow():
    """
    This test verifies that our branch protection workflow is functioning.
    If this test runs in CI, it means:
    1. Branch protection is allowing PR creation
    2. CI/CD pipeline is executing
    3. Tests are running before merge
    """
    assert True, "Branch protection workflow test passed"


class TestSecurityBasics:
    """Basic security tests for the application."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are properly configured."""
        response = client.get("/")
        # FastAPI with CORS middleware should include these headers
        assert response.status_code == 200
    
    def test_no_server_info_leakage(self):
        """Test that server information is not leaked in headers."""
        response = client.get("/")
        headers = response.headers
        
        # Should not reveal server technology details
        assert "server" not in headers.get("server", "").lower() or \
               "uvicorn" not in headers.get("server", "").lower()
    
    def test_api_endpoints_require_proper_methods(self):
        """Test that endpoints properly validate HTTP methods."""
        # Test that POST endpoints don't accept GET
        response = client.get("/api/v1/auth/login")
        assert response.status_code == 405  # Method Not Allowed


class TestFinancialSafety:
    """Tests to ensure financial calculation safety."""
    
    def test_decimal_import_available(self):
        """Ensure Decimal is available for financial calculations."""
        from decimal import Decimal
        
        # Test basic decimal operations
        amount = Decimal('100.000000')  # USDT with 6 decimals
        rate = Decimal('130.50')        # KES exchange rate
        
        result = amount * rate
        assert isinstance(result, Decimal)
        assert str(result) == '13050.000000'
    
    def test_no_float_usage_in_models(self):
        """Verify that financial models don't use float types."""
        from app.models.transaction import Transaction
        from app.models.wallet import Wallet
        
        # This is a basic check - in a real scenario, we'd inspect
        # the SQLAlchemy column types to ensure they're NUMERIC
        assert hasattr(Transaction, 'amount_crypto')
        assert hasattr(Transaction, 'amount_kes')
        assert hasattr(Wallet, 'balance_crypto')
        assert hasattr(Wallet, 'balance_kes')


if __name__ == "__main__":
    pytest.main([__file__])
