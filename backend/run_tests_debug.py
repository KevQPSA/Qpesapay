#!/usr/bin/env python3
"""
Debug test runner for Qpesapay backend.
Helps identify which tests are causing timeouts in CI/CD.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_test_group(test_path, timeout=120):
    """Run a specific test group with timeout."""
    print(f"\n{'='*60}")
    print(f"Running: {test_path}")
    print(f"Timeout: {timeout}s")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_path, 
            "-v", 
            "--tb=short",
            "--timeout=60",
            "--timeout-method=thread",
            "--disable-warnings"
        ], 
        timeout=timeout,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ PASSED in {duration:.2f}s")
        print(f"Exit code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        return True, duration
        
    except subprocess.TimeoutExpired:
        print(f"❌ TIMEOUT after {timeout}s")
        return False, timeout
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, 0

def main():
    """Run tests in groups to identify timeout issues."""
    
    # Set environment variables
    os.environ['TESTING'] = 'true'
    os.environ['CI'] = 'true'
    os.environ['DISABLE_EXTERNAL_CALLS'] = 'true'
    
    test_groups = [
        ("Basic Tests", "app/tests/test_initialization.py"),
        ("Security Tests (Core)", "app/tests/test_security.py"),
        ("API Security Tests", "app/tests/test_api_security.py::TestAuthenticationSecurity"),
        ("Webhook Security", "app/tests/test_api_security.py::TestWebhookSecurity"),
        ("Payment Security", "app/tests/test_api_security.py::TestPaymentSecurity"),
        ("General API Security", "app/tests/test_api_security.py::TestGeneralAPISecurity"),
        ("Rate Limiting", "app/tests/test_api_security.py::TestRateLimiting"),
        ("New Security Tests", "app/tests/test_api_security.py::TestAPIDocumentation"),
        ("CORS Tests", "app/tests/test_api_security.py::TestCORSPolicy"),
        ("JWT Tests", "app/tests/test_api_security.py::TestJWTTokenSecurity"),
        ("Authorization Tests", "app/tests/test_api_security.py::TestAuthorizationSecurity"),
    ]
    
    print("🧪 Qpesapay Test Debug Runner")
    print("="*60)
    
    results = []
    total_time = 0
    
    for name, test_path in test_groups:
        success, duration = run_test_group(test_path, timeout=120)
        results.append((name, success, duration))
        total_time += duration
        
        if not success:
            print(f"\n⚠️  {name} failed or timed out!")
            print("Consider investigating this test group.")
    
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for name, success, duration in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name:<30} {duration:>6.2f}s")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {len(results)} groups")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f}s")
    
    if failed == 0:
        print("\n🎉 All test groups passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test groups failed or timed out")
        return 1

if __name__ == "__main__":
    sys.exit(main())
