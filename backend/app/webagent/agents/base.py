"""
Base Agent Classes for Qpesapay WebAgent Integration
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseFinancialAgent(ABC):
    """
    Base class for all financial agents in Qpesapay WebAgent integration
    
    Provides common functionality for financial information seeking,
    caching, rate limiting, and error handling.
    """
    
    def __init__(self, tools: List[Any], config: Any, name: str):
        self.tools = tools
        self.config = config
        self.name = name
        self.logger = logging.getLogger(f"webagent.{name}")
        self._cache: Dict[str, Any] = {}
        self._last_request_time: Optional[datetime] = None
        
    async def _rate_limit_check(self):
        """Check rate limiting before making requests"""
        if not self.config.enable_rate_limiting:
            return
            
        if self._last_request_time:
            time_since_last = (datetime.now() - self._last_request_time).total_seconds()
            min_interval = 60.0 / self.config.max_requests_per_minute
            
            if time_since_last < min_interval:
                wait_time = min_interval - time_since_last
                self.logger.info(f"Rate limiting: waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
        
        self._last_request_time = datetime.now()
    
    def _get_cache_key(self, query: str, context: Dict[str, Any]) -> str:
        """Generate cache key for query and context"""
        import hashlib
        import json
        
        cache_data = {
            "query": query,
            "context": context,
            "agent": self.name
        }
        
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available and not expired"""
        if not self.config.enable_cache:
            return None
            
        cached_item = self._cache.get(cache_key)
        if not cached_item:
            return None
            
        # Check if cache is expired
        cache_age = (datetime.now() - cached_item["timestamp"]).total_seconds()
        if cache_age > self.config.cache_ttl:
            del self._cache[cache_key]
            return None
            
        self.logger.info(f"Cache hit for key: {cache_key[:8]}...")
        return cached_item["result"]
    
    def _set_cached_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache result with timestamp"""
        if not self.config.enable_cache:
            return
            
        self._cache[cache_key] = {
            "result": result,
            "timestamp": datetime.now()
        }
        
        # Simple cache cleanup - remove oldest entries if cache is too large
        if len(self._cache) > 1000:
            oldest_key = min(self._cache.keys(), 
                           key=lambda k: self._cache[k]["timestamp"])
            del self._cache[oldest_key]
    
    def _format_financial_context(self, context: Dict[str, Any]) -> str:
        """Format context for financial operations"""
        formatted_parts = []
        
        if context.get("user_id"):
            formatted_parts.append(f"User ID: {context['user_id']}")
            
        if context.get("transaction_type"):
            formatted_parts.append(f"Transaction Type: {context['transaction_type']}")
            
        if context.get("amount"):
            formatted_parts.append(f"Amount: {context['amount']}")
            
        if context.get("currency"):
            formatted_parts.append(f"Currency: {context['currency']}")
            
        if context.get("region"):
            formatted_parts.append(f"Region: {context['region']}")
        else:
            formatted_parts.append("Region: Kenya")  # Default for Qpesapay
            
        if context.get("compliance_level"):
            formatted_parts.append(f"Compliance Level: {context['compliance_level']}")
            
        return "\n".join(formatted_parts)
    
    def _extract_financial_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract financial entities from text"""
        import re
        
        entities = {
            "currencies": [],
            "amounts": [],
            "institutions": [],
            "regulations": []
        }
        
        # Currency patterns
        currency_patterns = [
            r'\b(USD|EUR|GBP|KES|BTC|ETH|USDT)\b',
            r'\b(Bitcoin|Ethereum|Tether|Dollar|Euro|Pound|Shilling)\b'
        ]
        
        for pattern in currency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["currencies"].extend(matches)
        
        # Amount patterns
        amount_patterns = [
            r'\$[\d,]+\.?\d*',
            r'KES\s*[\d,]+\.?\d*',
            r'[\d,]+\.?\d*\s*(USD|EUR|GBP|KES|BTC|ETH)'
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["amounts"].extend(matches)
        
        # Remove duplicates and clean up
        for key in entities:
            entities[key] = list(set(entities[key]))
            
        return entities
    
    @abstractmethod
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a query - must be implemented by subclasses"""
        pass
    
    async def cleanup(self):
        """Cleanup agent resources"""
        self._cache.clear()
        self.logger.info(f"Agent {self.name} cleaned up")


class WebDancerBasedAgent(BaseFinancialAgent):
    """
    Base class for agents using WebDancer (multi-turn reasoning)
    
    Suitable for complex financial analysis requiring multiple steps
    and iterative reasoning.
    """
    
    def __init__(self, tools: List[Any], config: Any, name: str):
        super().__init__(tools, config, name)
        self.max_turns = 10  # Maximum reasoning turns
        
    async def _multi_turn_reasoning(
        self, 
        initial_query: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform multi-turn reasoning for complex queries
        
        This simulates WebDancer's ReAct framework for financial analysis
        """
        reasoning_history = []
        current_query = initial_query
        
        for turn in range(self.max_turns):
            self.logger.info(f"Reasoning turn {turn + 1}: {current_query[:100]}...")
            
            # Simulate reasoning step
            reasoning_step = {
                "turn": turn + 1,
                "query": current_query,
                "timestamp": datetime.now().isoformat()
            }
            
            # Check if we need more information
            if self._needs_more_information(current_query, reasoning_history):
                # Use tools to gather more information
                tool_results = await self._use_tools(current_query, context)
                reasoning_step["tool_results"] = tool_results
                
                # Generate next query based on results
                next_query = self._generate_next_query(tool_results, context)
                if next_query:
                    current_query = next_query
                    reasoning_step["next_query"] = next_query
                else:
                    reasoning_step["conclusion"] = "Sufficient information gathered"
                    reasoning_history.append(reasoning_step)
                    break
            else:
                reasoning_step["conclusion"] = "Query resolved"
                reasoning_history.append(reasoning_step)
                break
                
            reasoning_history.append(reasoning_step)
        
        return {
            "reasoning_history": reasoning_history,
            "total_turns": len(reasoning_history),
            "final_query": current_query
        }
    
    def _needs_more_information(self, query: str, history: List[Dict]) -> bool:
        """Determine if more information is needed"""
        # Simple heuristic - can be enhanced with ML
        keywords_needing_research = [
            "current", "latest", "recent", "today", "now",
            "compare", "analysis", "trend", "forecast"
        ]
        
        return any(keyword in query.lower() for keyword in keywords_needing_research)
    
    async def _use_tools(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Use available tools to gather information"""
        tool_results = {}
        
        for tool in self.tools:
            try:
                if hasattr(tool, 'is_relevant') and tool.is_relevant(query):
                    result = await tool.execute(query, context)
                    tool_results[tool.name] = result
            except Exception as e:
                self.logger.error(f"Tool {tool.name} failed: {e}")
                tool_results[tool.name] = {"error": str(e)}
        
        return tool_results
    
    def _generate_next_query(self, tool_results: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """Generate next query based on tool results"""
        # Simple query generation - can be enhanced with LLM
        if not tool_results:
            return None
            
        # Look for incomplete or error results
        for tool_name, result in tool_results.items():
            if result.get("error") or result.get("incomplete"):
                return f"Get more detailed information about {tool_name} results"
        
        return None


class WebSailorBasedAgent(BaseFinancialAgent):
    """
    Base class for agents using WebSailor (extended thinking)
    
    Suitable for complex regulatory compliance and deep market analysis
    requiring extended reasoning capabilities.
    """
    
    def __init__(self, tools: List[Any], config: Any, name: str):
        super().__init__(tools, config, name)
        self.thinking_depth = 5  # Depth of extended thinking
        
    async def _extended_thinking(
        self, 
        query: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform extended thinking for complex analysis
        
        This simulates WebSailor's extended reasoning capabilities
        """
        thinking_layers = []
        
        for depth in range(self.thinking_depth):
            layer = {
                "depth": depth + 1,
                "focus": self._get_thinking_focus(depth, query, context),
                "timestamp": datetime.now().isoformat()
            }
            
            # Perform analysis at this depth
            analysis = await self._analyze_at_depth(depth, query, context, thinking_layers)
            layer["analysis"] = analysis
            
            thinking_layers.append(layer)
            
            # Check if we can conclude
            if analysis.get("conclusive", False):
                break
        
        return {
            "thinking_layers": thinking_layers,
            "total_depth": len(thinking_layers),
            "final_analysis": thinking_layers[-1]["analysis"] if thinking_layers else {}
        }
    
    def _get_thinking_focus(self, depth: int, query: str, context: Dict[str, Any]) -> str:
        """Get focus area for thinking at specific depth"""
        focus_areas = [
            "Initial problem understanding",
            "Context and constraints analysis", 
            "Risk and compliance considerations",
            "Market and regulatory factors",
            "Implementation and recommendations"
        ]
        
        return focus_areas[min(depth, len(focus_areas) - 1)]
    
    async def _analyze_at_depth(
        self, 
        depth: int, 
        query: str, 
        context: Dict[str, Any],
        previous_layers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze query at specific thinking depth"""
        analysis = {
            "depth": depth,
            "considerations": [],
            "findings": [],
            "conclusive": False
        }
        
        # Depth-specific analysis
        if depth == 0:  # Initial understanding
            analysis["considerations"] = [
                "Query interpretation",
                "Required information identification",
                "Initial risk assessment"
            ]
        elif depth == 1:  # Context analysis
            analysis["considerations"] = [
                "Regulatory environment",
                "Market conditions", 
                "User context and constraints"
            ]
        elif depth >= 2:  # Deep analysis
            analysis["considerations"] = [
                "Compliance implications",
                "Risk mitigation strategies",
                "Implementation recommendations"
            ]
            analysis["conclusive"] = True
        
        return analysis
