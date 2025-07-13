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
    Mock external dependencies that might cause hanging.
    Uses proper patching instead of sys.modules manipulation.
    """
    # Mock Redis connections using proper patching
    redis_patch = patch('redis.Redis')
    mock_redis_class = redis_patch.start()
    mock_redis_instance = MagicMock()
    mock_redis_instance.ping.return_value = True
    mock_redis_instance.get.return_value = None
    mock_redis_instance.set.return_value = True
    mock_redis_class.return_value = mock_redis_instance

    # Mock httpx using proper patching
    httpx_patch = patch('httpx.AsyncClient')
    mock_httpx_class = httpx_patch.start()
    mock_httpx_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_httpx_instance.get.return_value = mock_response
    mock_httpx_instance.post.return_value = mock_response
    mock_httpx_class.return_value = mock_httpx_instance

    # Store patches for cleanup
    _active_patches.extend([redis_patch, httpx_patch])

    print("External dependencies mocked")

# Global patch storage to maintain patch lifecycle
_active_patches = []

def apply_emergency_patches():
    """
    Apply emergency patches to prevent hanging.
    Returns patch objects so caller can manage their lifecycle.
    """
    # Patch slow operations globally
    time_patch = patch('time.sleep', return_value=None)
    asyncio_patch = patch('asyncio.sleep', return_value=None)

    # Start patches and store references
    time_patch.start()
    asyncio_patch.start()

    # Store patches globally for cleanup
    _active_patches.extend([time_patch, asyncio_patch])

    print("Emergency patches applied")
    return _active_patches

def cleanup_emergency_patches():
    """
    Clean up all active patches.
    """
    for patch_obj in _active_patches:
        try:
            patch_obj.stop()
        except Exception as e:
            print(f"Error stopping patch: {e}")

    _active_patches.clear()
    print("Emergency patches cleaned up")

if __name__ == "__main__":
    setup_emergency_test_environment()
    mock_external_dependencies()
    apply_emergency_patches()
