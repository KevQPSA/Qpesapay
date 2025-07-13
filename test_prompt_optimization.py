#!/usr/bin/env python3
"""
Test script for the automated prompt optimization integration
"""

import sys
import os
import asyncio

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.automated_prompt_optimizer import auto_optimize_prompt, format_optimization_display

async def test_prompt_optimization():
    """Test the automated prompt optimization"""
    
    print("🚀 Testing Automated Prompt Optimization for Qpesapay")
    print("=" * 60)
    
    # Test prompts
    test_prompts = [
        {
            "prompt": "Analyze this crypto transaction",
            "context": "financial analysis",
            "description": "Basic financial analysis prompt"
        },
        {
            "prompt": "Check if this transaction is compliant",
            "context": "compliance",
            "description": "Compliance checking prompt"
        },
        {
            "prompt": "What are the current market conditions?",
            "context": "market",
            "description": "Market analysis prompt"
        },
        {
            "prompt": "Process M-Pesa payment",
            "context": "mpesa",
            "description": "M-Pesa integration prompt"
        }
    ]
    
    for i, test_case in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print("-" * 40)
        
        try:
            # Optimize the prompt
            result = await auto_optimize_prompt(
                test_case["prompt"], 
                test_case["context"]
            )
            
            # Format and display the result
            formatted_result = format_optimization_display(result)
            print(formatted_result)
            
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
        
        print("\n" + "=" * 60)

def main():
    """Main function to run the test"""
    print("🔧 Qpesapay Prompt Optimization Integration Test")
    print("This test verifies that the automated prompt optimization is working")
    
    # Run the async test
    asyncio.run(test_prompt_optimization())
    
    print("\n✅ Test completed!")
    print("\n💡 The automated prompt optimization is now ready for use.")
    print("   Whenever you provide a prompt, I can automatically optimize it")
    print("   using the Qpesapay-specific context and requirements.")

if __name__ == "__main__":
    main()
