#!/usr/bin/env python3
"""
Emergency test runner for CI/CD
Runs tests with aggressive timeouts and bypasses to prevent hanging
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def setup_emergency_environment():
    """Setup emergency test environment"""
    # Critical environment variables
    env_vars = {
        "TESTING": "true",
        "CI": "true", 
        "LOG_LEVEL": "ERROR",
        "DATABASE_URL": "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db",
        "SECRET_KEY": "test-secret-key-for-testing-32-characters-long-secure",
        "ENCRYPTION_KEY": "test-encryption-key-32-characters-long-secure",
        "WEBHOOK_SECRET": "test-webhook-secret-32-characters-long",
        "DISABLE_RATE_LIMITING": "true",
        "DISABLE_EXTERNAL_CALLS": "true",
        "PYTHONPATH": str(Path.cwd()),
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Emergency environment configured")

def run_tests_with_timeout():
    """Run tests with aggressive timeout protection"""
    
    # Test command with multiple timeout layers
    cmd = [
        sys.executable, "-m", "pytest",
        "app/tests/",
        "-v",
        "--timeout=30",  # 30 second per-test timeout
        "--timeout-method=thread",
        "--tb=short",
        "--disable-warnings",
        "--maxfail=5",  # Stop after 5 failures
        "--durations=10",  # Show slowest tests
        "-x",  # Stop on first failure for faster feedback
    ]
    
    print(f"🚀 Running tests with command: {' '.join(cmd)}")
    
    # Set up process timeout (5 minutes total)
    timeout_seconds = 300
    
    try:
        # Run with timeout
        result = subprocess.run(
            cmd,
            timeout=timeout_seconds,
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        print("📊 Test Results:")
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print(f"❌ Tests failed with return code: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Tests timed out after {timeout_seconds} seconds")
        return False
    except Exception as e:
        print(f"💥 Error running tests: {e}")
        return False

def main():
    """Main emergency test runner"""
    print("🚨 EMERGENCY CI/CD TEST RUNNER")
    print("=" * 50)
    
    # Setup environment
    setup_emergency_environment()
    
    # Run tests
    success = run_tests_with_timeout()
    
    if success:
        print("\n✅ EMERGENCY TESTS COMPLETED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("\n❌ EMERGENCY TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
