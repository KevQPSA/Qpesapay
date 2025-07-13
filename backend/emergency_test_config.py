"""
Emergency test configuration for CI/CD
This module provides emergency overrides to prevent test hanging
"""

import os
import sys
from unittest.mock import patch, MagicMock

def setup_emergency_test_environment():
    """
    Setup emergency test environment to prevent hanging
    """
    # Set critical environment variables
    os.environ["TESTING"] = "true"
    os.environ["CI"] = "true"
    os.environ["LOG_LEVEL"] = "ERROR"
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
    
    # Disable problematic components
    os.environ["DISABLE_RATE_LIMITING"] = "true"
    os.environ["DISABLE_EXTERNAL_CALLS"] = "true"
    os.environ["DISABLE_BACKGROUND_TASKS"] = "true"
    
    print("Emergency test environment configured")

def mock_external_dependencies():
    """
    Mock external dependencies that might cause hanging
    """
    # Mock Redis connections
    mock_redis = MagicMock()
    mock_redis.ping.return_value = True
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    
    # Mock external API calls
    mock_httpx = MagicMock()
    mock_httpx.get.return_value.status_code = 200
    mock_httpx.post.return_value.status_code = 200
    
    # Apply mocks
    sys.modules['redis'] = mock_redis
    sys.modules['httpx'] = mock_httpx
    
    print("External dependencies mocked")

def apply_emergency_patches():
    """
    Apply emergency patches to prevent hanging
    """
    # Patch slow operations
    time_patch = patch('time.sleep', return_value=None)
    asyncio_patch = patch('asyncio.sleep', return_value=None)
    time_patch.start()
    asyncio_patch.start()
    print("Emergency patches applied")

if __name__ == "__main__":
    setup_emergency_test_environment()
    mock_external_dependencies()
    apply_emergency_patches()
