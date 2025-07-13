#!/usr/bin/env python3
"""
WebAgent Development Setup Script

Quick setup script to configure WebAgent for development workflows.
"""

import os
import sys
from pathlib import Path


def create_env_template():
    """Create .env template with WebAgent configuration"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    env_template = """# WebAgent Development Configuration
# Copy this to .env and fill in your API keys

# Core WebAgent APIs (Required)
GOOGLE_SEARCH_KEY=your_serper_api_key_here
JINA_API_KEY=your_jina_api_key_here  
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Crypto APIs (At least one required)
COINMARKETCAP_API_KEY=your_coinmarketcap_key_here
COINGECKO_API_KEY=your_coingecko_key_here
BINANCE_API_KEY=your_binance_key_here

# WebAgent Performance Settings
WEBAGENT_ENABLE_CACHE=true
WEBAGENT_CACHE_TTL=3600
WEBAGENT_RATE_LIMITING=true
WEBAGENT_MAX_REQUESTS_PER_MINUTE=60

# Model Configuration (Optional - uses cloud by default)
MODEL_SERVER_HOST=127.0.0.1
MODEL_SERVER_PORT=6001
MAX_LLM_CALL_PER_RUN=40

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/qpesapay
TEST_DATABASE_URL=postgresql://user:password@localhost/qpesapay_test

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
"""
    
    with open(env_file, 'w') as f:
        f.write(env_template)
    
    print(f"📝 Created .env template: {env_file}")
    print("   Please fill in your API keys before using WebAgent")


def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "aiohttp",
        "pytest",
        "asyncio"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True


def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "examples/generated",
        "logs",
        "app/webagent/agents",
        "app/webagent/tools",
        "app/tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")


def check_test_files():
    """Check if test files exist"""
    print("🧪 Checking test files...")
    
    test_files = [
        "examples/tests/payment_tests.py",
        "app/tests/test_webagent.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"   ✅ {test_file}")
        else:
            print(f"   ❌ {test_file} (missing)")
    
    if not Path("examples/tests/payment_tests.py").exists():
        print("\n⚠️ payment_tests.py not found!")
        print("   This is the main file WebAgent will help you complete")
        return False
    
    return True


def show_usage_examples():
    """Show usage examples"""
    print("\n🚀 WebAgent Development Usage Examples:")
    print("=" * 50)
    
    print("\n1️⃣ Analyze Payment Tests:")
    print("   python scripts/webagent_dev_demo.py")
    
    print("\n2️⃣ Complete Payment Tests:")
    print("   python examples/webagent_payment_test_completion.py")
    
    print("\n3️⃣ Start Development Server:")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    print("\n4️⃣ Use API Endpoints:")
    print("   # Analyze tests")
    print("   curl -X POST 'http://localhost:8000/api/v1/webagent/dev/analyze' \\")
    print("        -H 'Authorization: Bearer <token>' \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"file_path\": \"examples/tests/payment_tests.py\"}'")
    
    print("\n   # Complete specific test")
    print("   curl -X POST 'http://localhost:8000/api/v1/webagent/dev/complete-test' \\")
    print("        -H 'Authorization: Bearer <token>' \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"file_path\": \"examples/tests/payment_tests.py\", \"function_name\": \"test_audit_trail_completeness\"}'")


def show_api_key_setup():
    """Show API key setup instructions"""
    print("\n🔑 API Key Setup Instructions:")
    print("=" * 40)
    
    print("\n1. Google Search (Serper):")
    print("   • Visit: https://serper.dev/")
    print("   • Sign up and get API key")
    print("   • Add to .env: GOOGLE_SEARCH_KEY=your_key")
    
    print("\n2. Jina API:")
    print("   • Visit: https://jina.ai/")
    print("   • Sign up and get API key")
    print("   • Add to .env: JINA_API_KEY=your_key")
    
    print("\n3. DashScope (Alibaba):")
    print("   • Visit: https://dashscope.aliyun.com/")
    print("   • Sign up and get API key")
    print("   • Add to .env: DASHSCOPE_API_KEY=your_key")
    
    print("\n4. Crypto APIs (Choose one):")
    print("   • CoinMarketCap: https://coinmarketcap.com/api/")
    print("   • CoinGecko: https://www.coingecko.com/en/api")
    print("   • Binance: https://binance-docs.github.io/apidocs/")


def main():
    """Run the setup process"""
    print("🤖 WebAgent Development Setup")
    print("Setting up AI-powered development workflows for Qpesapay")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Not in the backend directory!")
        print("   Please run this script from the backend directory")
        sys.exit(1)
    
    # Run setup steps
    success = True
    
    # 1. Check dependencies
    if not check_dependencies():
        success = False
    
    # 2. Create directories
    create_directories()
    
    # 3. Create .env template
    create_env_template()
    
    # 4. Check test files
    if not check_test_files():
        success = False
    
    # 5. Show results
    if success:
        print("\n🎉 WebAgent Development Setup Complete!")
        print("\nNext Steps:")
        print("1. 🔑 Configure API keys in .env file")
        print("2. 🧪 Run the demo: python scripts/webagent_dev_demo.py")
        print("3. 🛠️ Complete tests: python examples/webagent_payment_test_completion.py")
        print("4. 🚀 Start development server and use API endpoints")
        
        show_usage_examples()
        show_api_key_setup()
        
    else:
        print("\n⚠️ Setup completed with warnings")
        print("   Please address the issues above before using WebAgent")
    
    print("\n📚 Documentation:")
    print("   • WebAgent Integration: backend/docs/webagent_integration.md")
    print("   • Development Guide: backend/docs/WEBAGENT_README.md")
    print("   • API Reference: http://localhost:8000/docs (when server is running)")


if __name__ == "__main__":
    main()
