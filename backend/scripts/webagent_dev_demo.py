#!/usr/bin/env python3
"""
WebAgent Development Assistant Demo

This script demonstrates how to use WebAgent for development workflows,
specifically for completing the payment tests in your Qpesapay project.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from app.webagent.core import get_webagent_manager


async def demo_payment_test_analysis():
    """Demonstrate WebAgent analysis of payment tests"""
    print("🚀 WebAgent Development Assistant Demo")
    print("=" * 50)
    
    try:
        # Initialize WebAgent manager
        print("📡 Initializing WebAgent manager...")
        manager = await get_webagent_manager()
        
        # Analyze payment tests
        print("\n🔍 Analyzing payment tests...")
        result = await manager.analyze_development_tasks(
            file_path="examples/tests/payment_tests.py",
            context={"analysis_type": "payment_specific"}
        )
        
        if result["success"]:
            analysis = result["analysis"]
            
            print(f"\n📊 Analysis Results:")
            print(f"   File: {analysis.get('file_analysis', {}).get('file_path', 'N/A')}")
            print(f"   Completion: {analysis.get('file_analysis', {}).get('completion_percentage', 0):.1f}%")
            print(f"   Incomplete functions: {analysis.get('file_analysis', {}).get('incomplete_functions', 0)}")
            
            # Show priority tasks
            priority_tasks = analysis.get("priority_tasks", [])
            if priority_tasks:
                print(f"\n🎯 Priority Tasks ({len(priority_tasks)}):")
                for i, task in enumerate(priority_tasks[:3], 1):
                    print(f"   {i}. {task['function_name']} (Priority: {task['priority']}, Effort: {task['estimated_effort']})")
            
            # Show recommendations
            recommendations = analysis.get("recommendations", {})
            best_practices = recommendations.get("best_practices", [])
            if best_practices:
                print(f"\n💡 Best Practices ({len(best_practices)}):")
                for practice in best_practices[:5]:
                    print(f"   • {practice}")
            
            security_improvements = recommendations.get("security_improvements", [])
            if security_improvements:
                print(f"\n🔒 Security Improvements ({len(security_improvements)}):")
                for improvement in security_improvements[:5]:
                    print(f"   • {improvement}")
            
            # Show next steps
            next_steps = recommendations.get("next_steps", [])
            if next_steps:
                print(f"\n📋 Next Steps:")
                for step in next_steps[:3]:
                    print(f"   • {step}")
        
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


async def demo_test_completion():
    """Demonstrate WebAgent test completion"""
    print("\n" + "=" * 50)
    print("🛠️ Test Completion Demo")
    print("=" * 50)
    
    try:
        manager = await get_webagent_manager()
        
        # Complete the audit trail test
        print("\n🔧 Completing 'test_audit_trail_completeness' function...")
        result = await manager.complete_test_function(
            file_path="examples/tests/payment_tests.py",
            function_name="test_audit_trail_completeness",
            context={"test_type": "audit_trail"}
        )
        
        if result["success"]:
            completion = result["completion"]
            implementation = completion.get("implementation", "")
            
            print("✅ Test completion generated!")
            print("\n📝 Implementation Preview:")
            print("-" * 40)
            # Show first few lines of implementation
            lines = implementation.strip().split('\n')
            for line in lines[:10]:
                print(f"   {line}")
            if len(lines) > 10:
                print(f"   ... ({len(lines) - 10} more lines)")
            print("-" * 40)
            
        else:
            print(f"❌ Test completion failed: {result.get('error', 'Unknown error')}")
        
        # Complete the rate limiting test
        print("\n🔧 Completing 'test_rate_limiting_compliance' function...")
        result = await manager.complete_test_function(
            file_path="examples/tests/payment_tests.py",
            function_name="test_rate_limiting_compliance",
            context={"test_type": "rate_limiting"}
        )
        
        if result["success"]:
            print("✅ Rate limiting test completion generated!")
        else:
            print(f"❌ Rate limiting test completion failed: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ Test completion demo failed: {e}")


async def demo_api_usage():
    """Demonstrate API usage for development workflows"""
    print("\n" + "=" * 50)
    print("📡 API Usage Demo")
    print("=" * 50)
    
    print("\n🌐 WebAgent Development API Endpoints:")
    print("   POST /api/v1/webagent/dev/analyze")
    print("   POST /api/v1/webagent/dev/complete-test")
    print("   GET  /api/v1/webagent/dev/payment-tests/analyze")
    
    print("\n📝 Example API Usage:")
    
    # Example 1: Analyze development tasks
    analyze_example = {
        "file_path": "examples/tests/payment_tests.py",
        "context": {
            "analysis_type": "payment_specific"
        }
    }
    
    print("\n1️⃣ Analyze Development Tasks:")
    print("   curl -X POST 'http://localhost:8000/api/v1/webagent/dev/analyze' \\")
    print("        -H 'Authorization: Bearer <token>' \\")
    print("        -H 'Content-Type: application/json' \\")
    print(f"        -d '{json.dumps(analyze_example, indent=2)}'")
    
    # Example 2: Complete test function
    complete_example = {
        "file_path": "examples/tests/payment_tests.py",
        "function_name": "test_audit_trail_completeness",
        "context": {
            "test_type": "audit_trail"
        }
    }
    
    print("\n2️⃣ Complete Test Function:")
    print("   curl -X POST 'http://localhost:8000/api/v1/webagent/dev/complete-test' \\")
    print("        -H 'Authorization: Bearer <token>' \\")
    print("        -H 'Content-Type: application/json' \\")
    print(f"        -d '{json.dumps(complete_example, indent=2)}'")
    
    # Example 3: Analyze payment tests
    print("\n3️⃣ Analyze Payment Tests:")
    print("   curl -X GET 'http://localhost:8000/api/v1/webagent/dev/payment-tests/analyze' \\")
    print("        -H 'Authorization: Bearer <token>'")


async def demo_integration_workflow():
    """Demonstrate complete development workflow integration"""
    print("\n" + "=" * 50)
    print("🔄 Development Workflow Integration")
    print("=" * 50)
    
    print("\n🎯 Complete Development Workflow:")
    print("   1. 🔍 Analyze test file for incomplete functions")
    print("   2. 📋 Get prioritized list of tasks")
    print("   3. 🛠️ Generate implementations for high-priority tests")
    print("   4. 🧪 Apply best practices and security patterns")
    print("   5. 📊 Verify test coverage and quality")
    
    print("\n💡 WebAgent Benefits for Development:")
    print("   ✅ Intelligent test completion with financial patterns")
    print("   ✅ Security-first implementation suggestions")
    print("   ✅ Best practices integration")
    print("   ✅ Multi-turn reasoning for complex scenarios")
    print("   ✅ Context-aware code generation")
    print("   ✅ Payment-specific testing patterns")
    
    print("\n🚀 Integration Points:")
    print("   • IDE Extensions (via API)")
    print("   • CI/CD Pipelines (automated test generation)")
    print("   • Code Review Tools (quality suggestions)")
    print("   • Development Dashboards (progress tracking)")
    print("   • Documentation Generation (from test patterns)")


async def main():
    """Run the complete WebAgent development demo"""
    print("🤖 WebAgent Development Assistant")
    print("Intelligent AI-powered development workflows for Qpesapay")
    print("=" * 60)
    
    # Run all demos
    await demo_payment_test_analysis()
    await demo_test_completion()
    await demo_api_usage()
    await demo_integration_workflow()
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("\nNext Steps:")
    print("1. 🔑 Configure API keys in .env file")
    print("2. 🚀 Start the FastAPI server")
    print("3. 📡 Use the WebAgent API endpoints")
    print("4. 🛠️ Integrate with your development workflow")
    print("5. 🧪 Complete your payment tests with AI assistance!")


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("examples/tests/payment_tests.py").exists():
        print("❌ Error: payment_tests.py not found!")
        print("   Please run this script from the backend directory")
        sys.exit(1)
    
    # Run the demo
    asyncio.run(main())
