#!/usr/bin/env python3
"""
Test script to verify Alembic setup and psycopg2 installation.
This script tests the Alembic configuration without requiring a running database.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import psycopg2
        print("✓ psycopg2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import psycopg2: {e}")
        return False
    
    try:
        import alembic
        print("✓ alembic imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import alembic: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✓ sqlalchemy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import sqlalchemy: {e}")
        return False
    
    return True

def test_env_loading():
    """Test that environment variables can be loaded."""
    print("\nTesting environment loading...")
    
    # Load environment variables
    from dotenv import load_dotenv
    env_file = backend_dir / ".env"
    
    if env_file.exists():
        load_dotenv(env_file)
        print("✓ .env file loaded")
        
        # Check some key variables
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            print(f"✓ DATABASE_URL found: {database_url[:50]}...")
        else:
            print("✗ DATABASE_URL not found")
            return False
    else:
        print("✗ .env file not found")
        return False
    
    return True

def test_alembic_config():
    """Test that Alembic configuration can be loaded."""
    print("\nTesting Alembic configuration...")
    
    try:
        # Set testing environment to bypass database connection
        os.environ['TESTING'] = 'true'
        
        # Import after setting environment
        from alembic.config import Config
        from alembic import command
        
        # Load Alembic config
        alembic_cfg = Config(str(backend_dir / "alembic.ini"))
        print("✓ Alembic configuration loaded")
        
        # Test that we can access the script directory
        from alembic.script import ScriptDirectory
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        print("✓ Alembic script directory accessible")
        
        # Check for migrations
        revisions = list(script_dir.walk_revisions())
        print(f"✓ Found {len(revisions)} migration(s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Alembic configuration test failed: {e}")
        return False

def test_app_config():
    """Test that app configuration can be loaded in testing mode."""
    print("\nTesting app configuration...")
    
    try:
        # Ensure testing mode is set
        os.environ['TESTING'] = 'true'
        
        # Import app config
        from app.config import settings
        print("✓ App configuration loaded successfully")
        
        # Test database URL transformation
        original_url = settings.DATABASE_URL
        transformed_url = original_url.replace("postgresql+asyncpg", "postgresql")
        print(f"✓ Database URL transformation: {transformed_url[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ App configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Alembic Setup Test ===\n")
    
    tests = [
        test_imports,
        test_env_loading,
        test_alembic_config,
        test_app_config,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Alembic setup is working correctly.")
        print("\nTo run migrations:")
        print("1. Ensure PostgreSQL is running")
        print("2. Run: alembic upgrade head")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
