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
    """
    Provides a new asyncio event loop for the entire pytest session.
    
    Yields:
        loop: The created asyncio event loop, available for all tests in the session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """
    Waits for the test database to become ready before running tests, failing the session if the database is unavailable.
    
    This fixture ensures that tests only proceed when the database is accessible, which is critical for CI/CD environments. No explicit cleanup is performed, as database teardown is handled externally.
    """
    # Wait for database to be ready (important for CI/CD)
    db_ready = await wait_for_db_ready(max_retries=30, retry_delay=1.0)
    if not db_ready:
        pytest.fail("Database not ready for testing")
    
    yield
    
    # Cleanup after all tests
    # Note: In CI/CD, the database container is destroyed anyway


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an asynchronous SQLAlchemy database session for use in tests.
    
    Ensures that any changes made during the test are rolled back and the session is properly closed after the test completes.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture
def security_test_client():
    """
    Yield a FastAPI TestClient with rate limiting explicitly enabled for security tests.
    
    Temporarily removes the `DISABLE_RATE_LIMITING` environment variable to ensure rate limiting is active during tests, then restores its original state after the test completes.
    """
    # Ensure rate limiting is enabled for security tests
    original_disable_rate_limiting = os.environ.get('DISABLE_RATE_LIMITING')

    # Temporarily enable rate limiting for security tests
    if 'DISABLE_RATE_LIMITING' in os.environ:
        del os.environ['DISABLE_RATE_LIMITING']

    try:
        # Use the existing app instance for security tests
        client = TestClient(app)
        yield client
    finally:
        # Restore original setting
        if original_disable_rate_limiting is not None:
            os.environ['DISABLE_RATE_LIMITING'] = original_disable_rate_limiting


@pytest.fixture
def isolated_test_env():
    """
    Sets up and restores environment variables to ensure an isolated environment for security tests.
    
    Temporarily modifies environment variables related to rate limiting, external calls, testing, and CI to enforce a controlled test environment. Restores the original environment variable states after the test completes.
    """
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
    """
    Fixture placeholder for resetting rate limiting state between security tests.
    
    Currently, this fixture does not perform any actions but is intended for future use if rate limiting state needs to be reset between tests.
    """
    # This fixture can be used to reset rate limiting state
    # if needed between security tests
    yield
    # Rate limiting state reset would go here if needed
