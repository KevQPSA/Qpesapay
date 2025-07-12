# backend/app/tests/test_initialization.py
import pytest
from fastapi.testclient import TestClient
from app.main import app, api_router
from app.config import settings

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Qpeasa"}

def test_config_loads():
    """Test if configuration loads properly."""
    assert settings is not None
    assert settings.PROJECT_NAME == "Qpeasa"
    assert settings.API_V1_STR == "/api/v1"

@pytest.mark.asyncio
async def test_schemas_import():
    """Test if schemas can be imported without errors."""
    try:
        from app.schemas.user import UserCreate
        from app.schemas.wallet import WalletCreate
        from app.schemas.transaction import TransactionCreate
        from app.schemas.merchant import MerchantCreate
        from app.schemas.settlement import SettlementCreate
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import schemas: {e}")

@pytest.mark.asyncio
async def test_models_import():
    """Test if models can be imported without errors."""
    try:
        from app.models.user import User
        from app.models.wallet import Wallet
        from app.models.transaction import Transaction
        from app.models.merchant import Merchant
        from app.models.settlement import Settlement
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import models: {e}")

def test_api_routers_are_registered():
    """Test if API routes are properly configured."""
    included_router_prefixes = [router.prefix for router in api_router.routes]
    
    expected_prefixes = [
        "/auth",
        "/payments",
        "/webhooks"
    ]
    
    for prefix in expected_prefixes:
        assert prefix in included_router_prefixes
