"""
WebAgent Core Manager for Qpesapay Integration
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from contextlib import asynccontextmanager

from .config import WebAgentConfig, get_webagent_config, validate_api_keys
from .agents import FinancialSearchAgent, ComplianceAgent, MarketAnalysisAgent, DevelopmentAssistantAgent
from .tools import CryptoMarketTool, FiatRatesTool, ComplianceCheckTool, TransactionVerificationTool, DevelopmentAssistantTool

logger = logging.getLogger(__name__)


class WebAgentManager:
    """
    Central manager for WebAgent integration in Qpesapay
    
    Manages agent lifecycle, tool registration, and provides high-level API
    for financial information seeking and compliance monitoring.
    """
    
    def __init__(self, config: Optional[WebAgentConfig] = None):
        self.config = config or get_webagent_config()
        self._agents: Dict[str, Any] = {}
        self._tools: Dict[str, Any] = {}
        self._initialized = False
        
    async def initialize(self) -> bool:
        """Initialize WebAgent manager and validate configuration"""
        try:
            # Validate API keys
            validation_results = validate_api_keys()
            missing_keys = [key for key, valid in validation_results.items() if not valid]
            
            if missing_keys:
                logger.warning(f"Missing API keys: {missing_keys}")
                # Continue with limited functionality
            
            # Initialize tools
            await self._initialize_tools()
            
            # Initialize agents
            await self._initialize_agents()
            
            self._initialized = True
            logger.info("WebAgent manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize WebAgent manager: {e}")
            return False
    
    async def _initialize_tools(self):
        """Initialize financial and compliance tools"""
        try:
            # Initialize crypto market tool
            if self.config.crypto_apis.get("coinmarketcap"):
                self._tools["crypto_market"] = CryptoMarketTool(self.config)
                
            # Initialize fiat rates tool
            self._tools["fiat_rates"] = FiatRatesTool(self.config)
            
            # Initialize compliance check tool
            self._tools["compliance_check"] = ComplianceCheckTool(self.config)
            
            # Initialize transaction verification tool
            self._tools["transaction_verification"] = TransactionVerificationTool(self.config)

            # Initialize development assistant tool
            self._tools["dev_assistant"] = DevelopmentAssistantTool(self.config)

            logger.info(f"Initialized {len(self._tools)} WebAgent tools")
            
        except Exception as e:
            logger.error(f"Failed to initialize tools: {e}")
            raise
    
    async def _initialize_agents(self):
        """Initialize specialized financial agents"""
        try:
            # Get available tools
            tool_list = list(self._tools.values())
            
            # Initialize Financial Search Agent (WebDancer-based)
            self._agents["financial_search"] = FinancialSearchAgent(
                tools=tool_list,
                config=self.config
            )
            
            # Initialize Compliance Agent (WebSailor-based)
            self._agents["compliance"] = ComplianceAgent(
                tools=tool_list,
                config=self.config
            )
            
            # Initialize Market Analysis Agent (WebSailor-based)
            self._agents["market_analysis"] = MarketAnalysisAgent(
                tools=tool_list,
                config=self.config
            )

            # Initialize Development Assistant Agent (WebDancer-based)
            self._agents["dev_assistant"] = DevelopmentAssistantAgent(
                tools=tool_list,
                config=self.config
            )

            logger.info(f"Initialized {len(self._agents)} WebAgent agents")
            
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            raise
    
    async def search_financial_information(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for financial information using WebDancer agent
        
        Args:
            query: Search query
            context: Additional context for the search
            
        Returns:
            Search results with analysis
        """
        if not self._initialized:
            raise RuntimeError("WebAgent manager not initialized")
            
        agent = self._agents.get("financial_search")
        if not agent:
            raise RuntimeError("Financial search agent not available")
            
        try:
            result = await agent.search(query, context or {})
            return {
                "success": True,
                "query": query,
                "result": result,
                "agent": "financial_search"
            }
        except Exception as e:
            logger.error(f"Financial search failed: {e}")
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "agent": "financial_search"
            }
    
    async def analyze_market_conditions(
        self, 
        assets: List[str], 
        timeframe: str = "24h"
    ) -> Dict[str, Any]:
        """
        Analyze market conditions for specified assets
        
        Args:
            assets: List of asset symbols (e.g., ['BTC', 'ETH', 'KES'])
            timeframe: Analysis timeframe
            
        Returns:
            Market analysis results
        """
        if not self._initialized:
            raise RuntimeError("WebAgent manager not initialized")
            
        agent = self._agents.get("market_analysis")
        if not agent:
            raise RuntimeError("Market analysis agent not available")
            
        try:
            result = await agent.analyze_market(assets, timeframe)
            return {
                "success": True,
                "assets": assets,
                "timeframe": timeframe,
                "analysis": result,
                "agent": "market_analysis"
            }
        except Exception as e:
            logger.error(f"Market analysis failed: {e}")
            return {
                "success": False,
                "assets": assets,
                "error": str(e),
                "agent": "market_analysis"
            }
    
    async def check_compliance(
        self, 
        transaction_data: Dict[str, Any],
        check_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Check compliance for transaction or operation
        
        Args:
            transaction_data: Transaction details to check
            check_type: Type of compliance check
            
        Returns:
            Compliance check results
        """
        if not self._initialized:
            raise RuntimeError("WebAgent manager not initialized")
            
        agent = self._agents.get("compliance")
        if not agent:
            raise RuntimeError("Compliance agent not available")
            
        try:
            result = await agent.check_compliance(transaction_data, check_type)
            return {
                "success": True,
                "transaction_data": transaction_data,
                "check_type": check_type,
                "compliance_result": result,
                "agent": "compliance"
            }
        except Exception as e:
            logger.error(f"Compliance check failed: {e}")
            return {
                "success": False,
                "transaction_data": transaction_data,
                "error": str(e),
                "agent": "compliance"
            }

    async def analyze_development_tasks(
        self,
        file_path: str = "examples/tests/payment_tests.py",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze development tasks and provide completion suggestions

        Args:
            file_path: Path to file to analyze
            context: Additional context for analysis

        Returns:
            Development analysis with completion suggestions
        """
        if not self._initialized:
            raise RuntimeError("WebAgent manager not initialized")

        agent = self._agents.get("dev_assistant")
        if not agent:
            raise RuntimeError("Development assistant agent not available")

        try:
            result = await agent.analyze_and_complete_tests(file_path, context or {})
            return {
                "success": True,
                "file_path": file_path,
                "analysis": result,
                "agent": "dev_assistant"
            }
        except Exception as e:
            logger.error(f"Development analysis failed: {e}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e),
                "agent": "dev_assistant"
            }

    async def complete_test_function(
        self,
        file_path: str,
        function_name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Complete a specific test function

        Args:
            file_path: Path to test file
            function_name: Name of function to complete
            context: Additional context

        Returns:
            Function completion result
        """
        if not self._initialized:
            raise RuntimeError("WebAgent manager not initialized")

        agent = self._agents.get("dev_assistant")
        if not agent:
            raise RuntimeError("Development assistant agent not available")

        try:
            result = await agent.complete_specific_test(file_path, function_name, context or {})
            return {
                "success": True,
                "file_path": file_path,
                "function_name": function_name,
                "completion": result,
                "agent": "dev_assistant"
            }
        except Exception as e:
            logger.error(f"Test completion failed: {e}")
            return {
                "success": False,
                "file_path": file_path,
                "function_name": function_name,
                "error": str(e),
                "agent": "dev_assistant"
            }

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents and tools"""
        return {
            "initialized": self._initialized,
            "agents": {
                name: {"available": True, "type": type(agent).__name__}
                for name, agent in self._agents.items()
            },
            "tools": {
                name: {"available": True, "type": type(tool).__name__}
                for name, tool in self._tools.items()
            },
            "config": {
                "model_server_url": f"http://{self.config.model_server_host}:{self.config.model_server_port}",
                "api_keys_configured": validate_api_keys()
            }
        }
    
    async def shutdown(self):
        """Shutdown WebAgent manager and cleanup resources"""
        try:
            # Cleanup agents
            for agent in self._agents.values():
                if hasattr(agent, 'cleanup'):
                    await agent.cleanup()
            
            # Cleanup tools
            for tool in self._tools.values():
                if hasattr(tool, 'cleanup'):
                    await tool.cleanup()
            
            self._agents.clear()
            self._tools.clear()
            self._initialized = False
            
            logger.info("WebAgent manager shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during WebAgent manager shutdown: {e}")


# Global WebAgent manager instance
_webagent_manager: Optional[WebAgentManager] = None


async def get_webagent_manager() -> WebAgentManager:
    """Get or create global WebAgent manager instance"""
    global _webagent_manager
    
    if _webagent_manager is None:
        _webagent_manager = WebAgentManager()
        await _webagent_manager.initialize()
    
    return _webagent_manager


@asynccontextmanager
async def webagent_context():
    """Context manager for WebAgent operations"""
    manager = await get_webagent_manager()
    try:
        yield manager
    finally:
        # Manager stays alive for reuse
        pass
