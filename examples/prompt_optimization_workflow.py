#!/usr/bin/env python3
"""
Practical example of using Prompt Optimizer during Qpesapay development.
This script demonstrates the complete workflow from prompt optimization to integration.
"""

import asyncio
import json
import requests
from typing import Dict, Any, List
from pathlib import Path

class QpesapayPromptOptimizer:
    """
    Integration class for using Prompt Optimizer during Qpesapay development.
    This class provides methods to optimize prompts and integrate them into your workflow.
    """
    
    def __init__(self, optimizer_url: str = "http://localhost:8081"):
        self.optimizer_url = optimizer_url
        self.project_root = Path(__file__).parent.parent
        self.prompt_library = self.project_root / "backend" / "prompts"
    
    def load_current_webagent_prompts(self) -> Dict[str, str]:
        """Load current prompts from WebAgent code for optimization"""
        
        # These are examples of current prompts that could be optimized
        current_prompts = {
            "financial_search": "Analyze this crypto transaction",
            
            "compliance_check": "Check if this transaction is compliant",
            
            "market_analysis": "What are the current market conditions?",
            
            "mpesa_integration": "Process M-Pesa transaction",
            
            "transaction_verification": "Verify this transaction is valid",
            
            "risk_assessment": "Assess the risk level of this transaction",
            
            "fraud_detection": "Check if this transaction shows signs of fraud",
            
            "regulatory_compliance": "Ensure this follows CBK regulations"
        }
        
        return current_prompts
    
    def optimize_prompt_manually(self, prompt_name: str, original_prompt: str) -> str:
        """
        Manual optimization workflow - demonstrates how to use the web interface.
        This method provides step-by-step instructions for manual optimization.
        """
        
        print(f"\n🎯 Optimizing prompt: {prompt_name}")
        print(f"📝 Original prompt: {original_prompt}")
        print("\n📋 Manual Optimization Steps:")
        print("1. Open Prompt Optimizer web interface: http://localhost:8081")
        print("2. Paste the original prompt in the input field")
        print("3. Add context: 'Kenya crypto-fiat payment processor, CBK compliance required'")
        print("4. Click 'Optimize' button")
        print("5. Review the optimized prompt")
        print("6. Use the comparison feature to test both prompts")
        print("7. Copy the optimized prompt for integration")
        print("\n⏳ Waiting for manual optimization...")
        
        # In a real scenario, you would manually optimize and then return the result
        # For this example, we'll return a pre-optimized version
        optimized_prompts = {
            "financial_search": """As a Kenya-focused crypto-fiat payment specialist, analyze this transaction considering:
- CBK regulatory requirements and compliance standards
- M-Pesa integration protocols and security measures
- USDT-KES conversion rates and market conditions
- KYC/AML compliance factors and risk assessment
- Transaction security patterns and fraud detection

Transaction data: {transaction_data}

Provide analysis in the following format:
1. Compliance Status: [Compliant/Non-Compliant/Requires Review]
2. Risk Level: [Low/Medium/High]
3. Regulatory Notes: [Specific CBK/CMA considerations]
4. Recommendations: [Action items or approvals needed]""",
            
            "compliance_check": """Perform comprehensive regulatory compliance analysis for Kenya financial services:

1. CBK Guidelines Verification:
   - Anti-Money Laundering (AML) requirements
   - Know Your Customer (KYC) standards
   - Foreign Exchange regulations
   - Digital payment service provider rules

2. CMA Requirements Check:
   - Securities and investment regulations
   - Capital markets compliance
   - Investor protection measures

3. Data Protection Compliance:
   - Kenya Data Protection Act compliance
   - Customer data handling protocols
   - Cross-border data transfer regulations

4. Transaction Risk Assessment:
   - Suspicious activity patterns
   - High-risk jurisdiction involvement
   - Transaction amount thresholds
   - Frequency and velocity analysis

Data to analyze: {compliance_data}

Provide detailed compliance report with specific regulatory references."""
        }
        
        return optimized_prompts.get(prompt_name, original_prompt)
    
    def save_optimized_prompt(self, prompt_name: str, original: str, optimized: str, metadata: Dict[str, Any]):
        """Save optimized prompt to the prompt library"""
        
        prompt_data = {
            "name": prompt_name.replace("_", " ").title(),
            "category": "webagent",
            "description": f"Optimized prompt for {prompt_name}",
            "original": original,
            "optimized": optimized,
            "context": "Used by Qpesapay WebAgent for financial operations",
            "optimization_date": metadata.get("date", "2024-01-15"),
            "models_tested": metadata.get("models", ["gpt-4", "gemini-1.5-pro"]),
            "performance_notes": metadata.get("notes", "Optimized for Kenya financial regulations"),
            "usage_instructions": f"Use this prompt in backend/app/webagent/agents.py for {prompt_name} operations"
        }
        
        # Ensure prompt library directory exists
        self.prompt_library.mkdir(exist_ok=True)
        
        # Save to JSON file
        prompt_file = self.prompt_library / f"{prompt_name}.json"
        with open(prompt_file, "w") as f:
            json.dump(prompt_data, f, indent=2)
        
        print(f"✅ Saved optimized prompt to: {prompt_file}")
    
    def generate_integration_code(self, prompt_name: str, optimized_prompt: str) -> str:
        """Generate Python code for integrating the optimized prompt"""
        
        class_name = "".join(word.capitalize() for word in prompt_name.split("_"))
        
        integration_code = f'''
# Integration code for {prompt_name}
# Add this to backend/app/webagent/agents.py

class {class_name}Agent:
    """Optimized agent for {prompt_name} operations"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.prompt_template = """{optimized_prompt}"""
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process {prompt_name} request with optimized prompt"""
        
        # Format the prompt with actual data
        formatted_prompt = self.prompt_template.format(**data)
        
        # Generate response using LLM
        response = await self.llm.generate(formatted_prompt)
        
        # Parse and structure the response
        return self.parse_response(response)
    
    def parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured data"""
        # Implement parsing logic based on the expected format
        return {{"raw_response": response, "parsed": True}}

# Usage example:
# agent = {class_name}Agent(llm_client)
# result = await agent.process({{"transaction_data": "...", "compliance_data": "..."}})
'''
        
        return integration_code
    
    def run_optimization_workflow(self):
        """Run the complete optimization workflow"""
        
        print("🚀 Starting Qpesapay Prompt Optimization Workflow")
        print("=" * 60)
        
        # Load current prompts
        current_prompts = self.load_current_webagent_prompts()
        
        print(f"\n📋 Found {len(current_prompts)} prompts to optimize:")
        for name in current_prompts.keys():
            print(f"   - {name}")
        
        # Optimize each prompt
        optimized_results = {}
        
        for prompt_name, original_prompt in current_prompts.items():
            print(f"\n{'='*40}")
            
            # Optimize the prompt (manual process)
            optimized_prompt = self.optimize_prompt_manually(prompt_name, original_prompt)
            
            # Save the optimized prompt
            metadata = {
                "date": "2024-01-15",
                "models": ["gpt-4", "gemini-1.5-pro"],
                "notes": f"Optimized for Kenya financial regulations and {prompt_name} use case"
            }
            
            self.save_optimized_prompt(prompt_name, original_prompt, optimized_prompt, metadata)
            
            # Generate integration code
            integration_code = self.generate_integration_code(prompt_name, optimized_prompt)
            
            # Save integration code
            code_file = self.project_root / "examples" / f"{prompt_name}_integration.py"
            with open(code_file, "w") as f:
                f.write(integration_code)
            
            print(f"✅ Generated integration code: {code_file}")
            
            optimized_results[prompt_name] = {
                "original": original_prompt,
                "optimized": optimized_prompt,
                "improvement_notes": f"Enhanced for Kenya market and {prompt_name} specifics"
            }
        
        # Generate summary report
        self.generate_optimization_report(optimized_results)
        
        print("\n🎉 Optimization workflow completed!")
        print("\n📋 Next Steps:")
        print("1. Review optimized prompts in backend/prompts/")
        print("2. Test the prompts using the web interface comparison feature")
        print("3. Integrate the optimized prompts into your WebAgent code")
        print("4. Run tests to validate improvements")
        print("5. Monitor performance in production")
    
    def generate_optimization_report(self, results: Dict[str, Dict[str, str]]):
        """Generate a summary report of optimization results"""
        
        report = {
            "optimization_summary": {
                "total_prompts_optimized": len(results),
                "optimization_date": "2024-01-15",
                "focus_areas": [
                    "Kenya financial regulations (CBK/CMA)",
                    "M-Pesa integration specifics",
                    "Crypto-fiat conversion accuracy",
                    "KYC/AML compliance enhancement",
                    "Risk assessment improvements"
                ]
            },
            "prompts": results,
            "integration_instructions": {
                "1": "Review each optimized prompt in backend/prompts/",
                "2": "Test prompts using Prompt Optimizer comparison feature",
                "3": "Update WebAgent code with optimized prompts",
                "4": "Run comprehensive tests to validate improvements",
                "5": "Monitor performance metrics in development and production"
            }
        }
        
        report_file = self.project_root / "docs" / "prompt_optimization_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Optimization report saved: {report_file}")

def main():
    """Main function to run the optimization workflow"""
    
    print("🔧 Qpesapay Prompt Optimization Workflow")
    print("This script demonstrates how to use Prompt Optimizer during development")
    print("\n⚠️  Prerequisites:")
    print("1. Prompt Optimizer should be running at http://localhost:8081")
    print("2. Run: ./scripts/start_prompt_optimizer.sh")
    print("3. Configure API keys in the web interface")
    
    # Check if Prompt Optimizer is running
    try:
        response = requests.get("http://localhost:8081", timeout=5)
        if response.status_code == 200:
            print("✅ Prompt Optimizer is running")
        else:
            print("❌ Prompt Optimizer is not accessible")
            return
    except requests.exceptions.RequestException:
        print("❌ Prompt Optimizer is not running. Please start it first:")
        print("   ./scripts/start_prompt_optimizer.sh")
        return
    
    # Run the optimization workflow
    optimizer = QpesapayPromptOptimizer()
    optimizer.run_optimization_workflow()

if __name__ == "__main__":
    main()
