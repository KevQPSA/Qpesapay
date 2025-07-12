#!/usr/bin/env python3
"""
Test script to verify Context7 MCP setup for Qpesapay project.
This script tests the Context7 installation and provides example usage.
"""

import subprocess
import sys
import json
from pathlib import Path

def test_context7_installation():
    """Test if Context7 MCP is properly installed."""
    print("🧪 Testing Context7 MCP Installation...")
    
    try:
        # Test Context7 help command
        result = subprocess.run(
            ["npx", "-y", "@upstash/context7-mcp@latest", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Context7 MCP is properly installed!")
            print(f"📋 Available options:\n{result.stdout}")
            return True
        else:
            print(f"❌ Context7 installation test failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Context7 installation test timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing Context7: {e}")
        return False

def check_configuration_files():
    """Check if configuration files are properly created."""
    print("\n🔧 Checking Configuration Files...")
    
    config_files = [
        ".augment/mcp-config.json",
        ".vscode/settings.json", 
        ".cursor/mcp.json"
    ]
    
    for config_file in config_files:
        path = Path(config_file)
        if path.exists():
            print(f"✅ {config_file} - Found")
            try:
                with open(path, 'r') as f:
                    json.load(f)
                print(f"   📋 Valid JSON configuration")
            except json.JSONDecodeError:
                print(f"   ❌ Invalid JSON in {config_file}")
        else:
            print(f"❌ {config_file} - Not found")

def show_qpesapay_specific_examples():
    """Show Context7 usage examples specific to Qpesapay project."""
    print("\n🎯 Context7 Usage Examples for Qpesapay:")
    
    examples = [
        {
            "title": "FastAPI Payment Endpoint",
            "query": "Create FastAPI endpoint for USDT to KES conversion with validation. use context7",
            "libraries": ["/fastapi/fastapi", "/pydantic/pydantic"]
        },
        {
            "title": "Async SQLAlchemy Models", 
            "query": "Implement async SQLAlchemy models for cryptocurrency transactions. use library /sqlalchemy/sqlalchemy",
            "libraries": ["/sqlalchemy/sqlalchemy"]
        },
        {
            "title": "JWT Authentication Middleware",
            "query": "Create FastAPI JWT authentication middleware with Redis caching. use context7",
            "libraries": ["/fastapi/fastapi", "/redis/redis-py", "/mpdavis/python-jose"]
        },
        {
            "title": "Pytest Async Testing",
            "query": "Write pytest fixtures for async FastAPI testing with database. use library /pytest-dev/pytest",
            "libraries": ["/pytest-dev/pytest", "/pytest-dev/pytest-asyncio"]
        },
        {
            "title": "HTTP Client for M-Pesa API",
            "query": "Create async HTTP client for M-Pesa Daraja API integration. use library /encode/httpx",
            "libraries": ["/encode/httpx"]
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   Query: {example['query']}")
        print(f"   Libraries: {', '.join(example['libraries'])}")

def main():
    """Main test function."""
    print("🚀 Context7 MCP Setup Verification for Qpesapay\n")
    
    # Test installation
    installation_ok = test_context7_installation()
    
    # Check configuration files
    check_configuration_files()
    
    # Show examples
    show_qpesapay_specific_examples()
    
    print("\n" + "="*60)
    if installation_ok:
        print("✅ Context7 MCP is ready for use!")
        print("\n📚 Next Steps:")
        print("1. Use Context7 in your AI assistant with 'use context7'")
        print("2. Try the example queries above")
        print("3. Add library-specific IDs for better results")
        print("4. Check the context7-setup-guide.md for more details")
    else:
        print("❌ Context7 MCP setup needs attention")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure Node.js is installed (v18+)")
        print("2. Check internet connection")
        print("3. Try running: npx -y @upstash/context7-mcp@latest --help")
    
    print("\n📖 Documentation: https://github.com/upstash/context7")

if __name__ == "__main__":
    main()
