"""
Automated Prompt Optimization Service for Real-time Use
This service automatically optimizes prompts when requested by the AI assistant.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from .prompt_optimizer_client import PromptOptimizerClient

logger = logging.getLogger(__name__)

class AutomatedPromptOptimizer:
    """
    Service that automatically optimizes prompts in real-time.
    Used by the AI assistant to enhance prompts during conversations.
    """
    
    def __init__(self):
        self.client = PromptOptimizerClient()
        self._cache = {}  # Simple cache for optimization results
    
    async def auto_optimize(
        self, 
        prompt: str, 
        context_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Automatically optimize a prompt with intelligent category detection
        
        Args:
            prompt: The prompt to optimize
            context_hint: Optional hint about the prompt's purpose
            
        Returns:
            Optimization result with original and optimized prompts
        """
        
        # Check cache first
        cache_key = f"{prompt}:{context_hint}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Detect category from prompt content
        category = self._detect_category(prompt, context_hint)
        
        try:
            async with self.client as optimizer:
                result = await optimizer.optimize_prompt(prompt, category)
                
                # Cache the result
                self._cache[cache_key] = result
                
                # Add auto-optimization metadata
                result["auto_optimized"] = True
                result["detected_category"] = category
                result["optimization_confidence"] = self._calculate_confidence(prompt, category)
                
                return result
                
        except Exception as e:
            logger.error(f"Auto-optimization failed: {e}")
            # Return original prompt if optimization fails
            return {
                "original_prompt": prompt,
                "optimized_prompt": prompt,
                "category": category,
                "auto_optimized": False,
                "error": str(e),
                "optimization_confidence": 0.0
            }
    
    def _detect_category(self, prompt: str, context_hint: Optional[str] = None) -> str:
        """
        Intelligently detect the category of a prompt based on content and context
        """
        
        prompt_lower = prompt.lower()
        hint_lower = (context_hint or "").lower()
        
        # Financial analysis keywords
        financial_keywords = [
            "transaction", "crypto", "bitcoin", "usdt", "payment", "transfer",
            "analyze", "financial", "money", "currency", "exchange", "rate",
            "balance", "wallet", "blockchain", "conversion"
        ]
        
        # Compliance keywords
        compliance_keywords = [
            "compliance", "regulatory", "cbk", "cma", "kyc", "aml", "verify",
            "regulation", "legal", "audit", "risk", "suspicious", "report",
            "data protection", "gdpr", "privacy"
        ]
        
        # Market analysis keywords
        market_keywords = [
            "market", "trend", "price", "volatility", "analysis", "forecast",
            "prediction", "conditions", "sentiment", "volume", "liquidity",
            "arbitrage", "opportunity"
        ]
        
        # M-Pesa integration keywords
        mpesa_keywords = [
            "mpesa", "m-pesa", "daraja", "safaricom", "stk", "push", "callback",
            "integration", "api", "mobile", "phone", "254", "kenya"
        ]
        
        # Count keyword matches
        categories = {
            "financial_analysis": sum(1 for kw in financial_keywords if kw in prompt_lower or kw in hint_lower),
            "compliance_check": sum(1 for kw in compliance_keywords if kw in prompt_lower or kw in hint_lower),
            "market_analysis": sum(1 for kw in market_keywords if kw in prompt_lower or kw in hint_lower),
            "mpesa_integration": sum(1 for kw in mpesa_keywords if kw in prompt_lower or kw in hint_lower)
        }
        
        # Return category with highest score, default to general
        best_category = max(categories.items(), key=lambda x: x[1])
        return best_category[0] if best_category[1] > 0 else "general"
    
    def _calculate_confidence(self, prompt: str, category: str) -> float:
        """
        Calculate confidence score for the optimization
        """
        
        # Base confidence factors
        length_factor = min(len(prompt) / 100, 1.0)  # Longer prompts get higher confidence
        category_factor = 0.9 if category != "general" else 0.6  # Specific categories get higher confidence
        
        # Keyword density factor
        prompt_lower = prompt.lower()
        qpesapay_keywords = ["kenya", "crypto", "fiat", "payment", "usdt", "mpesa", "cbk", "cma"]
        keyword_matches = sum(1 for kw in qpesapay_keywords if kw in prompt_lower)
        keyword_factor = min(keyword_matches / 3, 1.0)  # Up to 3 keywords for full score
        
        # Calculate overall confidence
        confidence = (length_factor * 0.3 + category_factor * 0.4 + keyword_factor * 0.3)
        return round(confidence, 2)
    
    def format_optimization_result(self, result: Dict[str, Any]) -> str:
        """
        Format optimization result for display to the user
        """
        
        if not result.get("auto_optimized", False):
            return f"**Original Prompt:** {result['original_prompt']}\n\n*Note: Optimization failed - {result.get('error', 'Unknown error')}*"
        
        confidence = result.get("optimization_confidence", 0.0)
        category = result.get("detected_category", "general")
        
        formatted = f"""## 🚀 **Automated Prompt Optimization Result**

**📝 Original Prompt:**
```
{result['original_prompt']}
```

**✨ Optimized Prompt:**
```
{result['optimized_prompt']}
```

**📊 Optimization Details:**
- **Category Detected:** {category.replace('_', ' ').title()}
- **Confidence Score:** {confidence:.0%}
- **Qpesapay-Specific:** ✅ Yes

**🎯 Key Improvements:**
"""
        
        # Add improvement notes
        improvements = result.get("improvement_notes", [])
        for improvement in improvements[:5]:  # Show top 5 improvements
            formatted += f"- {improvement}\n"
        
        formatted += f"\n**💡 Usage:** This optimized prompt is specifically tailored for Qpesapay's Kenya crypto-fiat payment processing needs with CBK/CMA compliance considerations."
        
        return formatted


# Global instance for easy access
_auto_optimizer = AutomatedPromptOptimizer()

async def auto_optimize_prompt(prompt: str, context_hint: Optional[str] = None) -> Dict[str, Any]:
    """
    Global function to automatically optimize prompts
    
    Usage:
        result = await auto_optimize_prompt("Analyze this transaction", "financial")
    """
    return await _auto_optimizer.auto_optimize(prompt, context_hint)

def format_optimization_display(result: Dict[str, Any]) -> str:
    """
    Global function to format optimization results for display
    """
    return _auto_optimizer.format_optimization_result(result)

# Synchronous wrapper for immediate use
def optimize_prompt_sync(prompt: str, context_hint: Optional[str] = None) -> Dict[str, Any]:
    """
    Synchronous wrapper for prompt optimization
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a new task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, auto_optimize_prompt(prompt, context_hint))
                return future.result(timeout=30)
        else:
            # If no loop is running, use asyncio.run
            return asyncio.run(auto_optimize_prompt(prompt, context_hint))
    except Exception as e:
        logger.error(f"Synchronous optimization failed: {e}")
        return {
            "original_prompt": prompt,
            "optimized_prompt": prompt,
            "auto_optimized": False,
            "error": str(e),
            "optimization_confidence": 0.0
        }
