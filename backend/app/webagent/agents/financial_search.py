"""
Financial Search Agent - WebDancer-based agent for complex financial information seeking
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base import WebDancerBasedAgent


class FinancialSearchAgent(WebDancerBasedAgent):
    """
    Financial Search Agent using WebDancer's multi-turn reasoning
    
    Specialized for:
    - Crypto market analysis and price discovery
    - Fiat currency rate analysis
    - Financial news and trend analysis
    - Cross-market arbitrage opportunities
    - Payment method availability research
    """
    
    def __init__(self, tools: List[Any], config: Any):
        super().__init__(tools, config, "financial_search")
        self.search_domains = [
            "cryptocurrency_markets",
            "fiat_currency_rates", 
            "financial_news",
            "regulatory_updates",
            "payment_methods",
            "market_trends"
        ]
    
    async def search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main search method for financial information
        
        Args:
            query: Search query (e.g., "Current BTC to KES exchange rate")
            context: Additional context (user_id, transaction_type, etc.)
            
        Returns:
            Comprehensive search results with analysis
        """
        await self._rate_limit_check()
        
        # Check cache first
        cache_key = self._get_cache_key(query, context)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        try:
            # Classify query type
            query_type = self._classify_financial_query(query)
            
            # Perform multi-turn reasoning
            reasoning_result = await self._multi_turn_reasoning(query, context)
            
            # Execute specialized search based on query type
            search_result = await self._execute_specialized_search(
                query, query_type, context, reasoning_result
            )
            
            # Analyze and synthesize results
            final_result = await self._synthesize_search_results(
                query, search_result, reasoning_result, context
            )
            
            # Cache result
            self._set_cached_result(cache_key, final_result)
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"Financial search failed: {e}")
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _classify_financial_query(self, query: str) -> str:
        """Classify the type of financial query"""
        query_lower = query.lower()
        
        # Price/rate queries
        if any(word in query_lower for word in ["price", "rate", "exchange", "convert"]):
            if any(crypto in query_lower for crypto in ["btc", "eth", "usdt", "bitcoin", "ethereum"]):
                return "crypto_price_query"
            elif any(fiat in query_lower for fiat in ["kes", "usd", "eur", "shilling", "dollar"]):
                return "fiat_rate_query"
            else:
                return "general_price_query"
        
        # Market analysis queries
        elif any(word in query_lower for word in ["trend", "analysis", "forecast", "prediction"]):
            return "market_analysis_query"
        
        # News and updates
        elif any(word in query_lower for word in ["news", "update", "announcement", "regulation"]):
            return "news_query"
        
        # Payment method queries
        elif any(word in query_lower for word in ["mpesa", "payment", "method", "transfer"]):
            return "payment_method_query"
        
        # Compliance queries
        elif any(word in query_lower for word in ["compliance", "regulation", "legal", "kyc", "aml"]):
            return "compliance_query"
        
        else:
            return "general_financial_query"
    
    async def _execute_specialized_search(
        self, 
        query: str, 
        query_type: str, 
        context: Dict[str, Any],
        reasoning_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute specialized search based on query type"""
        
        search_results = {
            "query_type": query_type,
            "primary_results": {},
            "supporting_results": {},
            "tool_outputs": {}
        }
        
        if query_type == "crypto_price_query":
            search_results = await self._search_crypto_prices(query, context)
            
        elif query_type == "fiat_rate_query":
            search_results = await self._search_fiat_rates(query, context)
            
        elif query_type == "market_analysis_query":
            search_results = await self._search_market_analysis(query, context)
            
        elif query_type == "news_query":
            search_results = await self._search_financial_news(query, context)
            
        elif query_type == "payment_method_query":
            search_results = await self._search_payment_methods(query, context)
            
        elif query_type == "compliance_query":
            search_results = await self._search_compliance_info(query, context)
            
        else:
            search_results = await self._search_general_financial(query, context)
        
        return search_results
    
    async def _search_crypto_prices(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for cryptocurrency prices and market data"""
        results = {"query_type": "crypto_price_query", "data": {}}
        
        # Extract crypto symbols from query
        crypto_symbols = self._extract_crypto_symbols(query)
        
        # Use crypto market tool
        crypto_tool = next((tool for tool in self.tools if tool.name == "crypto_market"), None)
        if crypto_tool:
            try:
                for symbol in crypto_symbols:
                    price_data = await crypto_tool.get_price(symbol)
                    results["data"][symbol] = price_data
            except Exception as e:
                results["error"] = f"Crypto price lookup failed: {e}"
        
        return results
    
    async def _search_fiat_rates(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for fiat currency exchange rates"""
        results = {"query_type": "fiat_rate_query", "data": {}}
        
        # Extract currency pairs from query
        currency_pairs = self._extract_currency_pairs(query)
        
        # Use fiat rates tool
        fiat_tool = next((tool for tool in self.tools if tool.name == "fiat_rates"), None)
        if fiat_tool:
            try:
                for pair in currency_pairs:
                    rate_data = await fiat_tool.get_rate(pair["from"], pair["to"])
                    results["data"][f"{pair['from']}_to_{pair['to']}"] = rate_data
            except Exception as e:
                results["error"] = f"Fiat rate lookup failed: {e}"
        
        return results
    
    async def _search_market_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for market analysis and trends"""
        results = {"query_type": "market_analysis_query", "data": {}}
        
        # This would integrate with market analysis tools
        # For now, return placeholder structure
        results["data"] = {
            "trend_analysis": "Market analysis would be performed here",
            "key_indicators": [],
            "recommendations": []
        }
        
        return results
    
    async def _search_financial_news(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for financial news and updates"""
        results = {"query_type": "news_query", "data": {}}
        
        # This would integrate with news APIs
        results["data"] = {
            "recent_news": [],
            "regulatory_updates": [],
            "market_sentiment": "neutral"
        }
        
        return results
    
    async def _search_payment_methods(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for payment method information"""
        results = {"query_type": "payment_method_query", "data": {}}
        
        # Kenya-specific payment methods
        results["data"] = {
            "available_methods": ["M-Pesa", "Bank Transfer", "Crypto Wallet"],
            "recommended_method": "M-Pesa",
            "fees": {},
            "processing_times": {}
        }
        
        return results
    
    async def _search_compliance_info(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for compliance and regulatory information"""
        results = {"query_type": "compliance_query", "data": {}}
        
        # Use compliance tool
        compliance_tool = next((tool for tool in self.tools if tool.name == "compliance_check"), None)
        if compliance_tool:
            try:
                compliance_data = await compliance_tool.check_regulations(query, context)
                results["data"] = compliance_data
            except Exception as e:
                results["error"] = f"Compliance check failed: {e}"
        
        return results
    
    async def _search_general_financial(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """General financial information search"""
        results = {"query_type": "general_financial_query", "data": {}}
        
        # Use multiple tools for comprehensive search
        for tool in self.tools:
            try:
                if hasattr(tool, 'search'):
                    tool_result = await tool.search(query, context)
                    results["data"][tool.name] = tool_result
            except Exception as e:
                self.logger.warning(f"Tool {tool.name} search failed: {e}")
        
        return results
    
    async def _synthesize_search_results(
        self, 
        query: str, 
        search_result: Dict[str, Any],
        reasoning_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize and analyze search results"""
        
        synthesis = {
            "success": True,
            "query": query,
            "query_type": search_result.get("query_type", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "context": self._format_financial_context(context),
            "reasoning_summary": {
                "total_turns": reasoning_result.get("total_turns", 0),
                "key_insights": self._extract_key_insights(reasoning_result)
            },
            "search_results": search_result,
            "recommendations": self._generate_recommendations(search_result, context),
            "confidence_score": self._calculate_confidence_score(search_result),
            "next_actions": self._suggest_next_actions(search_result, context)
        }
        
        return synthesis
    
    def _extract_crypto_symbols(self, query: str) -> List[str]:
        """Extract cryptocurrency symbols from query"""
        import re
        
        crypto_patterns = [
            r'\b(BTC|ETH|USDT|LTC|XRP|ADA|DOT|LINK|UNI|AAVE)\b',
            r'\b(Bitcoin|Ethereum|Tether|Litecoin|Ripple)\b'
        ]
        
        symbols = []
        for pattern in crypto_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            symbols.extend(matches)
        
        # Convert to standard symbols
        symbol_map = {
            "Bitcoin": "BTC",
            "Ethereum": "ETH", 
            "Tether": "USDT",
            "Litecoin": "LTC",
            "Ripple": "XRP"
        }
        
        standardized = []
        for symbol in symbols:
            standardized.append(symbol_map.get(symbol, symbol.upper()))
        
        return list(set(standardized))
    
    def _extract_currency_pairs(self, query: str) -> List[Dict[str, str]]:
        """Extract currency pairs from query"""
        import re
        
        # Look for patterns like "USD to KES", "BTC/USD", etc.
        pair_patterns = [
            r'(\w{3})\s+to\s+(\w{3})',
            r'(\w{3})/(\w{3})',
            r'(\w{3})-(\w{3})'
        ]
        
        pairs = []
        for pattern in pair_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                pairs.append({"from": match[0].upper(), "to": match[1].upper()})
        
        return pairs
    
    def _extract_key_insights(self, reasoning_result: Dict[str, Any]) -> List[str]:
        """Extract key insights from reasoning process"""
        insights = []
        
        reasoning_history = reasoning_result.get("reasoning_history", [])
        for step in reasoning_history:
            if step.get("conclusion"):
                insights.append(step["conclusion"])
        
        return insights
    
    def _generate_recommendations(self, search_result: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on search results"""
        recommendations = []
        
        query_type = search_result.get("query_type", "")
        
        if query_type == "crypto_price_query":
            recommendations.extend([
                "Consider market volatility when making transactions",
                "Check multiple exchanges for best rates",
                "Monitor price trends before large transactions"
            ])
        elif query_type == "fiat_rate_query":
            recommendations.extend([
                "Compare rates across different providers",
                "Consider timing for better exchange rates",
                "Factor in transaction fees"
            ])
        
        return recommendations
    
    def _calculate_confidence_score(self, search_result: Dict[str, Any]) -> float:
        """Calculate confidence score for search results"""
        # Simple scoring based on data availability
        data = search_result.get("data", {})
        
        if search_result.get("error"):
            return 0.2
        elif not data:
            return 0.3
        elif len(data) == 1:
            return 0.7
        else:
            return 0.9
    
    def _suggest_next_actions(self, search_result: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Suggest next actions based on search results"""
        actions = []
        
        query_type = search_result.get("query_type", "")
        
        if query_type == "crypto_price_query":
            actions.extend([
                "Set up price alerts for significant changes",
                "Review transaction limits and fees",
                "Consider market timing for transactions"
            ])
        elif query_type == "compliance_query":
            actions.extend([
                "Review compliance requirements",
                "Update KYC documentation if needed",
                "Monitor regulatory changes"
            ])
        
        return actions
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of abstract method from base class"""
        return await self.search(query, context)
