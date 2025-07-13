"""
Automated Prompt Optimizer Client for Qpesapay Development
This service provides automated prompt optimization capabilities.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
import aiohttp
from pathlib import Path

logger = logging.getLogger(__name__)

class PromptOptimizerClient:
    """
    Automated client for the Prompt Optimizer service.
    Provides programmatic access to prompt optimization capabilities.
    """
    
    def __init__(self, base_url: str = "http://localhost:18181"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.qpesapay_context = {
            "domain": "financial_services",
            "market": "kenya",
            "regulations": ["CBK", "CMA", "Kenya_Data_Protection_Act"],
            "integrations": ["mpesa", "daraja_api", "usdt", "bitcoin"],
            "compliance_requirements": [
                "KYC/AML verification",
                "Transaction monitoring",
                "Regulatory reporting",
                "Cross-border compliance"
            ]
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def health_check(self) -> bool:
        """Check if the Prompt Optimizer service is running"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(f"{self.base_url}/") as response:
                return response.status == 200
        except Exception as e:
            logger.warning(f"Prompt Optimizer health check failed: {e}")
            return False
    
    def _build_optimization_context(self, category: str = "general") -> str:
        """Build context string for Qpesapay-specific optimization"""
        
        context_templates = {
            "financial_analysis": """
            Context: Kenya crypto-fiat payment processor specializing in USDT-KES conversions
            Requirements: CBK regulatory compliance, M-Pesa integration, real-time transaction analysis
            Focus: Financial accuracy, risk assessment, compliance verification
            """,
            
            "compliance_check": """
            Context: Kenya financial services compliance verification system
            Requirements: CBK and CMA regulatory adherence, KYC/AML procedures, data protection
            Focus: Regulatory compliance, audit trails, risk management
            """,
            
            "market_analysis": """
            Context: Kenya crypto-fiat market analysis for payment processing
            Requirements: Real-time market data, exchange rate analysis, trend prediction
            Focus: Market conditions, volatility assessment, arbitrage opportunities
            """,
            
            "mpesa_integration": """
            Context: M-Pesa Daraja API integration for crypto-fiat payments
            Requirements: Safaricom API compliance, transaction security, error handling
            Focus: Payment processing, transaction validation, integration reliability
            """,
            
            "general": """
            Context: Kenya-focused crypto-fiat payment processor (Qpesapay)
            Requirements: CBK/CMA compliance, M-Pesa integration, USDT-KES operations
            Focus: Financial accuracy, regulatory compliance, user security
            """
        }
        
        return context_templates.get(category, context_templates["general"]).strip()
    
    async def optimize_prompt(
        self, 
        original_prompt: str, 
        category: str = "general",
        model: str = "gpt-4",
        custom_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize a prompt using the Prompt Optimizer service
        
        Args:
            original_prompt: The original prompt to optimize
            category: Category for context (financial_analysis, compliance_check, etc.)
            model: AI model to use for optimization
            custom_context: Custom context override
            
        Returns:
            Dictionary containing optimization results
        """
        
        if not await self.health_check():
            raise ConnectionError("Prompt Optimizer service is not available")
        
        # Build context for optimization
        context = custom_context or self._build_optimization_context(category)
        
        # Simulate the optimization process
        # In a real implementation, this would call the actual API
        optimized_prompt = await self._simulate_optimization(
            original_prompt, context, category
        )
        
        return {
            "original_prompt": original_prompt,
            "optimized_prompt": optimized_prompt,
            "category": category,
            "context_used": context,
            "model": model,
            "improvement_notes": self._generate_improvement_notes(category),
            "qpesapay_specific": True
        }
    
    async def _simulate_optimization(
        self, 
        original_prompt: str, 
        context: str, 
        category: str
    ) -> str:
        """
        Simulate prompt optimization with Qpesapay-specific improvements
        This would be replaced with actual API calls in production
        """
        
        # Qpesapay-specific optimization templates
        optimization_templates = {
            "financial_analysis": f"""As a Kenya-focused crypto-fiat payment specialist, {original_prompt.lower()}

Consider the following in your analysis:
- CBK regulatory requirements and compliance standards
- M-Pesa integration protocols and security measures
- USDT-KES conversion rates and market conditions
- KYC/AML compliance factors and risk assessment
- Transaction security patterns and fraud detection
- Cross-border payment regulations and reporting requirements

Provide analysis in the following structured format:
1. Compliance Status: [Compliant/Non-Compliant/Requires Review]
2. Risk Level: [Low/Medium/High]
3. Regulatory Notes: [Specific CBK/CMA considerations]
4. Market Impact: [Exchange rate and volatility factors]
5. Recommendations: [Action items or approvals needed]

Data to analyze: {{input_data}}""",

            "compliance_check": f"""Perform comprehensive regulatory compliance analysis for Kenya financial services regarding: {original_prompt.lower()}

Verification Framework:
1. CBK Guidelines Compliance:
   - Anti-Money Laundering (AML) requirements
   - Know Your Customer (KYC) standards
   - Foreign Exchange regulations
   - Digital payment service provider rules

2. CMA Requirements Assessment:
   - Securities and investment regulations
   - Capital markets compliance
   - Investor protection measures

3. Data Protection Compliance:
   - Kenya Data Protection Act adherence
   - Customer data handling protocols
   - Cross-border data transfer regulations

4. Transaction Risk Evaluation:
   - Suspicious activity pattern detection
   - High-risk jurisdiction involvement
   - Transaction amount threshold analysis
   - Frequency and velocity assessment

Compliance data: {{compliance_data}}

Provide detailed compliance report with specific regulatory references and actionable recommendations.""",

            "market_analysis": f"""Analyze crypto-fiat market conditions for Kenya with focus on: {original_prompt.lower()}

Comprehensive Market Assessment:
1. Exchange Rate Analysis:
   - USDT/KES current rates and historical trends
   - Bitcoin/KES market movements and volatility
   - Cross-platform rate comparisons
   - Arbitrage opportunity identification

2. M-Pesa Ecosystem Integration:
   - Transaction volume patterns and seasonal trends
   - Peak usage times and capacity analysis
   - Integration success rates and performance metrics
   - User adoption and behavior patterns

3. Regulatory Environment Impact:
   - Recent CBK policy changes and implications
   - CMA regulatory updates and market effects
   - Government cryptocurrency stance evolution
   - Banking sector collaboration trends

4. Economic Indicators Correlation:
   - Kenya Shilling stability and inflation impact
   - Cross-border remittance flow analysis
   - Mobile money ecosystem health assessment
   - Competitive landscape and market positioning

Market data: {{market_data}}

Provide actionable insights for strategic decision-making with specific recommendations for Qpesapay operations.""",

            "mpesa_integration": f"""Process M-Pesa integration request following Safaricom Daraja API best practices for: {original_prompt.lower()}

Integration Protocol:
1. Transaction Validation Framework:
   - Phone number format validation (254XXXXXXXXX)
   - Amount limits and business rule enforcement
   - Account balance verification and availability
   - Duplicate transaction prevention mechanisms

2. API Integration Standards:
   - OAuth token management and automatic refresh
   - STK Push request formatting and validation
   - Callback URL handling and security verification
   - Comprehensive error code interpretation and handling

3. Compliance and Security Requirements:
   - Transaction logging for comprehensive audit trails
   - Customer notification protocols and timing
   - Dispute resolution procedures and escalation
   - Regulatory reporting requirements (CBK compliance)

4. Performance and Reliability Optimization:
   - Response time monitoring and alerting
   - Intelligent retry logic for failed transactions
   - Load balancing and traffic distribution
   - Caching strategies for frequent operations

Transaction details: {{mpesa_data}}

Ensure all processing adheres to Safaricom guidelines, CBK regulations, and Qpesapay security standards."""
        }
        
        # Get the appropriate template or create a general optimization
        if category in optimization_templates:
            return optimization_templates[category]
        else:
            # General optimization for other categories
            return f"""As a Kenya-focused crypto-fiat payment specialist, {original_prompt.lower()}

Context: Qpesapay payment processor specializing in USDT-KES conversions with M-Pesa integration

Key Considerations:
- CBK and CMA regulatory compliance requirements
- M-Pesa Daraja API integration standards
- Real-time crypto-fiat conversion accuracy
- KYC/AML verification and risk assessment
- Transaction security and fraud prevention
- Cross-border payment regulations

Input data: {{input_data}}

Provide detailed analysis with specific recommendations for Qpesapay operations."""
    
    def _generate_improvement_notes(self, category: str) -> List[str]:
        """Generate improvement notes for the optimization"""
        
        base_improvements = [
            "Added Kenya market-specific context",
            "Included CBK and CMA regulatory requirements",
            "Enhanced with M-Pesa integration considerations",
            "Structured output format for consistency",
            "Added specific compliance checkpoints"
        ]
        
        category_specific = {
            "financial_analysis": [
                "Added USDT-KES conversion rate considerations",
                "Included fraud detection patterns",
                "Enhanced risk assessment framework"
            ],
            "compliance_check": [
                "Comprehensive regulatory framework coverage",
                "Specific Kenya Data Protection Act requirements",
                "Enhanced audit trail specifications"
            ],
            "market_analysis": [
                "Real-time market data integration",
                "Cross-platform arbitrage analysis",
                "Economic indicator correlation"
            ],
            "mpesa_integration": [
                "Safaricom API best practices",
                "Enhanced error handling protocols",
                "Performance optimization strategies"
            ]
        }
        
        return base_improvements + category_specific.get(category, [])
    
    async def batch_optimize_prompts(
        self, 
        prompts: Dict[str, Dict[str, str]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Optimize multiple prompts in batch
        
        Args:
            prompts: Dict with format {prompt_id: {"prompt": str, "category": str}}
            
        Returns:
            Dict with optimization results for each prompt
        """
        
        results = {}
        
        for prompt_id, prompt_data in prompts.items():
            try:
                result = await self.optimize_prompt(
                    prompt_data["prompt"],
                    prompt_data.get("category", "general")
                )
                results[prompt_id] = result
                
                # Add a small delay to avoid overwhelming the service
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to optimize prompt {prompt_id}: {e}")
                results[prompt_id] = {
                    "error": str(e),
                    "original_prompt": prompt_data["prompt"]
                }
        
        return results
    
    async def save_optimization_result(
        self, 
        result: Dict[str, Any], 
        prompt_name: str
    ) -> Path:
        """Save optimization result to the prompt library"""
        
        from pathlib import Path
        import json
        from datetime import datetime
        
        # Create prompt library directory
        prompt_lib_dir = Path(__file__).parent.parent.parent / "prompts"
        prompt_lib_dir.mkdir(exist_ok=True)
        
        # Prepare the data for saving
        prompt_data = {
            "name": prompt_name.replace("_", " ").title(),
            "category": result.get("category", "general"),
            "description": f"Optimized prompt for {prompt_name}",
            "original": result["original_prompt"],
            "optimized": result["optimized_prompt"],
            "context": result.get("context_used", ""),
            "optimization_date": datetime.now().isoformat(),
            "model": result.get("model", "gpt-4"),
            "improvement_notes": result.get("improvement_notes", []),
            "qpesapay_specific": result.get("qpesapay_specific", True),
            "usage_instructions": f"Use this optimized prompt in WebAgent for {prompt_name} operations"
        }
        
        # Save to JSON file
        prompt_file = prompt_lib_dir / f"{prompt_name}.json"
        with open(prompt_file, "w", encoding="utf-8") as f:
            json.dump(prompt_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved optimized prompt to: {prompt_file}")
        return prompt_file


# Convenience function for quick optimization
async def optimize_prompt_for_qpesapay(
    prompt: str, 
    category: str = "general"
) -> Dict[str, Any]:
    """
    Quick function to optimize a prompt for Qpesapay use cases
    
    Usage:
        result = await optimize_prompt_for_qpesapay(
            "Analyze this crypto transaction", 
            "financial_analysis"
        )
    """
    
    async with PromptOptimizerClient() as client:
        return await client.optimize_prompt(prompt, category)
