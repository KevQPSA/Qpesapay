"""
Security test configuration and fixtures.
Provides specialized configuration for security tests to work properly in CI/CD.
"""

import os
import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database import SessionLocal, wait_for_db_ready


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Setup test database and wait for it to be ready."""
    # Wait for database to be ready (important for CI/CD)
    db_ready = await wait_for_db_ready(max_retries=30, retry_delay=1.0)
    if not db_ready:
        pytest.fail("Database not ready for testing")
    
    yield
    
    # Cleanup after all tests
    # Note: In CI/CD, the database container is destroyed anyway


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for tests."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture
def security_test_client():
    """Provide a test client specifically configured for security tests."""
    # Ensure rate limiting is enabled for security tests
    original_disable_rate_limiting = os.environ.get('DISABLE_RATE_LIMITING')
    
    # Temporarily enable rate limiting for security tests
    if 'DISABLE_RATE_LIMITING' in os.environ:
        del os.environ['DISABLE_RATE_LIMITING']
    
    try:
        # Create a fresh app instance for security tests
        from app.main import create_app
        security_app = create_app()
        client = TestClient(security_app)
        yield client
    finally:
        # Restore original setting
        if original_disable_rate_limiting is not None:
            os.environ['DISABLE_RATE_LIMITING'] = original_disable_rate_limiting


@pytest.fixture
def isolated_test_env():
    """Provide an isolated test environment for security tests."""
    # Store original environment
    original_env = {}
    test_env_vars = [
        'DISABLE_RATE_LIMITING',
        'DISABLE_EXTERNAL_CALLS',
        'TESTING',
        'CI'
    ]
    
    for var in test_env_vars:
        if var in os.environ:
            original_env[var] = os.environ[var]
    
    # Set security test environment
    os.environ['TESTING'] = 'true'
    # Don't disable rate limiting for security tests
    if 'DISABLE_RATE_LIMITING' in os.environ:
        del os.environ['DISABLE_RATE_LIMITING']
    
    yield
    
    # Restore original environment
    for var in test_env_vars:
        if var in os.environ:
            del os.environ[var]
        if var in original_env:
            os.environ[var] = original_env[var]


@pytest.fixture
def rate_limit_reset():
    """Reset rate limiting state between tests."""
    # This fixture can be used to reset rate limiting state
    # if needed between security tests
    yield
    # Rate limiting state reset would go here if needed
