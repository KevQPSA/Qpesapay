"""
Tests for WebAgent Integration
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from typing import Dict, Any

from app.webagent.core import WebAgentManager, get_webagent_manager
from app.webagent.config import WebAgentConfig
from app.webagent.agents import FinancialSearchAgent, ComplianceAgent, MarketAnalysisAgent
from app.webagent.tools import CryptoMarketTool


class TestWebAgentConfig:
    """Test WebAgent configuration"""
    
    def test_config_initialization(self):
        """Test configuration initialization with environment variables"""
        config = WebAgentConfig(
            google_search_key="test_google_key",
            jina_api_key="test_jina_key",
            dashscope_api_key="test_dashscope_key"
        )
        
        assert config.google_search_key == "test_google_key"
        assert config.jina_api_key == "test_jina_key"
        assert config.dashscope_api_key == "test_dashscope_key"
        assert config.max_llm_calls_per_run == 40
        assert config.enable_cache is True
    
    def test_config_validation(self):
        """Test configuration validation"""
        from app.webagent.config import validate_api_keys
        
        with patch.dict('os.environ', {
            'GOOGLE_SEARCH_KEY': 'test_key',
            'JINA_API_KEY': 'test_key',
            'DASHSCOPE_API_KEY': 'test_key'
        }):
            validation_results = validate_api_keys()
            
            assert validation_results["google_search"] is True
            assert validation_results["jina_api"] is True
            assert validation_results["dashscope"] is True


class TestWebAgentManager:
    """Test WebAgent Manager"""
    
    @pytest.fixture
    async def manager(self):
        """Create WebAgent manager for testing"""
        config = WebAgentConfig(
            google_search_key="test_google_key",
            jina_api_key="test_jina_key",
            dashscope_api_key="test_dashscope_key"
        )
        
        manager = WebAgentManager(config)
        
        # Mock tools and agents for testing
        manager._tools = {
            "crypto_market": Mock(spec=CryptoMarketTool),
            "fiat_rates": Mock(),
            "compliance_check": Mock(),
            "transaction_verification": Mock()
        }
        
        manager._agents = {
            "financial_search": Mock(spec=FinancialSearchAgent),
            "compliance": Mock(spec=ComplianceAgent),
            "market_analysis": Mock(spec=MarketAnalysisAgent)
        }
        
        manager._initialized = True
        
        return manager
    
    @pytest.mark.asyncio
    async def test_manager_initialization(self):
        """Test WebAgent manager initialization"""
        config = WebAgentConfig(
            google_search_key="test_google_key",
            jina_api_key="test_jina_key",
            dashscope_api_key="test_dashscope_key"
        )
        
        manager = WebAgentManager(config)
        
        # Mock the initialization methods
        with patch.object(manager, '_initialize_tools', new_callable=AsyncMock) as mock_init_tools, \
             patch.object(manager, '_initialize_agents', new_callable=AsyncMock) as mock_init_agents:
            
            result = await manager.initialize()
            
            assert result is True
            assert manager._initialized is True
            mock_init_tools.assert_called_once()
            mock_init_agents.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_financial_search(self, manager):
        """Test financial information search"""
        # Mock the financial search agent
        mock_agent = manager._agents["financial_search"]
        mock_agent.search = AsyncMock(return_value={
            "success": True,
            "query": "BTC price",
            "result": {"price": 45000, "currency": "USD"}
        })
        
        result = await manager.search_financial_information(
            query="What's the current BTC price?",
            context={"user_id": "test_user"}
        )
        
        assert result["success"] is True
        assert result["agent"] == "financial_search"
        assert "result" in result
        mock_agent.search.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_market_analysis(self, manager):
        """Test market analysis"""
        mock_agent = manager._agents["market_analysis"]
        mock_agent.analyze_market = AsyncMock(return_value={
            "success": True,
            "analysis": {"trend": "bullish", "confidence": 0.8}
        })
        
        result = await manager.analyze_market_conditions(
            assets=["BTC", "ETH"],
            timeframe="24h"
        )
        
        assert result["success"] is True
        assert result["agent"] == "market_analysis"
        assert "analysis" in result
        mock_agent.analyze_market.assert_called_once_with(["BTC", "ETH"], "24h")
    
    @pytest.mark.asyncio
    async def test_compliance_check(self, manager):
        """Test compliance checking"""
        mock_agent = manager._agents["compliance"]
        mock_agent.check_compliance = AsyncMock(return_value={
            "success": True,
            "compliance_result": {"passed": True, "risk_level": "LOW"}
        })
        
        transaction_data = {
            "user_id": "test_user",
            "amount": 50000,
            "currency": "KES"
        }
        
        result = await manager.check_compliance(
            transaction_data=transaction_data,
            check_type="comprehensive"
        )
        
        assert result["success"] is True
        assert result["agent"] == "compliance"
        assert "compliance_result" in result
        mock_agent.check_compliance.assert_called_once()
    
    def test_agent_status(self, manager):
        """Test getting agent status"""
        status = manager.get_agent_status()
        
        assert status["initialized"] is True
        assert "agents" in status
        assert "tools" in status
        assert "config" in status
        
        assert len(status["agents"]) == 3
        assert len(status["tools"]) == 4


class TestFinancialSearchAgent:
    """Test Financial Search Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create financial search agent for testing"""
        config = Mock()
        config.enable_cache = True
        config.cache_ttl = 3600
        config.enable_rate_limiting = False
        
        tools = [Mock(), Mock()]
        agent = FinancialSearchAgent(tools, config)
        
        return agent
    
    @pytest.mark.asyncio
    async def test_crypto_price_query(self, agent):
        """Test cryptocurrency price query"""
        query = "What's the current BTC price?"
        context = {"user_id": "test_user"}
        
        # Mock the multi-turn reasoning and search execution
        with patch.object(agent, '_multi_turn_reasoning', new_callable=AsyncMock) as mock_reasoning, \
             patch.object(agent, '_execute_specialized_search', new_callable=AsyncMock) as mock_search, \
             patch.object(agent, '_synthesize_search_results', new_callable=AsyncMock) as mock_synthesize:
            
            mock_reasoning.return_value = {"total_turns": 2}
            mock_search.return_value = {"query_type": "crypto_price_query", "data": {"BTC": {"price": 45000}}}
            mock_synthesize.return_value = {
                "success": True,
                "query": query,
                "query_type": "crypto_price_query",
                "search_results": {"data": {"BTC": {"price": 45000}}},
                "confidence_score": 0.9
            }
            
            result = await agent.search(query, context)
            
            assert result["success"] is True
            assert result["query_type"] == "crypto_price_query"
            assert result["confidence_score"] == 0.9
            
            mock_reasoning.assert_called_once()
            mock_search.assert_called_once()
            mock_synthesize.assert_called_once()
    
    def test_query_classification(self, agent):
        """Test financial query classification"""
        test_cases = [
            ("What's the BTC price?", "crypto_price_query"),
            ("USD to KES exchange rate", "fiat_rate_query"),
            ("Market trend analysis for ETH", "market_analysis_query"),
            ("Latest crypto news", "news_query"),
            ("M-Pesa payment methods", "payment_method_query"),
            ("KYC compliance requirements", "compliance_query"),
            ("General financial question", "general_financial_query")
        ]
        
        for query, expected_type in test_cases:
            result = agent._classify_financial_query(query)
            assert result == expected_type
    
    def test_crypto_symbol_extraction(self, agent):
        """Test cryptocurrency symbol extraction"""
        test_cases = [
            ("BTC price today", ["BTC"]),
            ("Bitcoin and Ethereum rates", ["BTC", "ETH"]),
            ("USDT, LTC, and XRP analysis", ["USDT", "LTC", "XRP"]),
            ("No crypto symbols here", [])
        ]
        
        for query, expected_symbols in test_cases:
            result = agent._extract_crypto_symbols(query)
            assert set(result) == set(expected_symbols)


class TestComplianceAgent:
    """Test Compliance Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create compliance agent for testing"""
        config = Mock()
        config.enable_cache = True
        config.cache_ttl = 3600
        config.enable_rate_limiting = False
        
        tools = [Mock(), Mock()]
        agent = ComplianceAgent(tools, config)
        
        return agent
    
    @pytest.mark.asyncio
    async def test_kyc_compliance_check(self, agent):
        """Test KYC compliance checking"""
        transaction_data = {
            "user_id": "test_user",
            "amount": 50000,
            "user_documents": ["national_id", "proof_of_address"]
        }
        
        result = await agent._check_kyc_compliance(transaction_data)
        
        assert result["passed"] is True
        assert "national_id" in result["requirements_met"]
        assert "proof_of_address" in result["requirements_met"]
        assert len(result["missing_requirements"]) == 0
    
    @pytest.mark.asyncio
    async def test_kyc_compliance_failure(self, agent):
        """Test KYC compliance failure"""
        transaction_data = {
            "user_id": "test_user",
            "amount": 50000,
            "user_documents": ["national_id"]  # Missing proof_of_address
        }
        
        result = await agent._check_kyc_compliance(transaction_data)
        
        assert result["passed"] is False
        assert "proof_of_address" in result["missing_requirements"]
        assert "Missing proof_of_address" in result["issues"]
    
    @pytest.mark.asyncio
    async def test_transaction_limits_check(self, agent):
        """Test transaction limits checking"""
        transaction_data = {
            "amount": 30000,
            "user_tier": "basic",
            "daily_usage": 10000,
            "monthly_usage": 100000
        }
        
        result = await agent._check_transaction_limits(transaction_data)
        
        assert result["passed"] is True
        assert "daily_limit" in result["limits_checked"]
        assert "monthly_limit" in result["limits_checked"]
        assert len(result["violations"]) == 0
    
    @pytest.mark.asyncio
    async def test_transaction_limits_violation(self, agent):
        """Test transaction limits violation"""
        transaction_data = {
            "amount": 60000,  # Exceeds basic daily limit of 50000
            "user_tier": "basic",
            "daily_usage": 0,
            "monthly_usage": 0
        }
        
        result = await agent._check_transaction_limits(transaction_data)
        
        assert result["passed"] is False
        assert len(result["violations"]) > 0
        assert "Daily limit exceeded" in result["violations"][0]


class TestCryptoMarketTool:
    """Test Crypto Market Tool"""
    
    @pytest.fixture
    def tool(self):
        """Create crypto market tool for testing"""
        config = Mock()
        config.crypto_apis = {
            "coinmarketcap": "test_cmc_key",
            "coingecko": "test_cg_key",
            "binance": "test_binance_key"
        }
        
        tool = CryptoMarketTool(config)
        return tool
    
    @pytest.mark.asyncio
    async def test_get_price_success(self, tool):
        """Test successful price retrieval"""
        with patch.object(tool, '_get_price_coinmarketcap', new_callable=AsyncMock) as mock_cmc:
            mock_cmc.return_value = {
                "symbol": "BTC",
                "name": "Bitcoin",
                "price_usd": 45000,
                "price_kes": 5850000,
                "change_24h": 2.5,
                "source": "coinmarketcap"
            }
            
            result = await tool.get_price("BTC")
            
            assert result["symbol"] == "BTC"
            assert result["price_usd"] == 45000
            assert result["source"] == "coinmarketcap"
            mock_cmc.assert_called_once_with("BTC")
    
    @pytest.mark.asyncio
    async def test_get_price_error(self, tool):
        """Test price retrieval error handling"""
        with patch.object(tool, '_get_price_coinmarketcap', new_callable=AsyncMock) as mock_cmc:
            mock_cmc.side_effect = Exception("API error")
            
            result = await tool.get_price("BTC")
            
            assert "error" in result
            assert "API error" in result["error"]
    
    def test_is_relevant(self, tool):
        """Test query relevance checking"""
        relevant_queries = [
            "BTC price",
            "Bitcoin market data",
            "cryptocurrency rates",
            "ETH trading volume"
        ]
        
        irrelevant_queries = [
            "Weather forecast",
            "Restaurant recommendations",
            "Movie reviews"
        ]
        
        for query in relevant_queries:
            assert tool.is_relevant(query) is True
        
        for query in irrelevant_queries:
            assert tool.is_relevant(query) is False
    
    def test_extract_symbols(self, tool):
        """Test symbol extraction from queries"""
        test_cases = [
            ("BTC and ETH prices", ["BTC", "ETH"]),
            ("Bitcoin to Ethereum exchange", ["BTC", "ETH"]),
            ("USDT market analysis", ["USDT"]),
            ("No symbols here", [])
        ]
        
        for query, expected_symbols in test_cases:
            result = tool._extract_symbols(query)
            assert set(result) == set(expected_symbols)


class TestWebAgentAPI:
    """Test WebAgent API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from fastapi.testclient import TestClient
        from app.main import app
        
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self):
        """Create authentication headers for testing"""
        # This would create valid JWT token for testing
        return {"Authorization": "Bearer test_token"}
    
    def test_webagent_status_endpoint(self, client):
        """Test WebAgent status endpoint"""
        with patch('app.api.v1.webagent.get_webagent_manager', new_callable=AsyncMock) as mock_manager:
            mock_manager.return_value.__aenter__.return_value.get_agent_status.return_value = {
                "initialized": True,
                "agents": {"financial_search": {"available": True}},
                "tools": {"crypto_market": {"available": True}},
                "config": {"model_server_url": "http://localhost:6001"}
            }
            
            response = client.get("/api/v1/webagent/status")
            
            assert response.status_code == 200
            data = response.json()
            assert data["initialized"] is True
            assert "agents" in data
            assert "tools" in data
    
    def test_financial_search_endpoint(self, client, auth_headers):
        """Test financial search endpoint"""
        request_data = {
            "query": "What's the current BTC price?",
            "context": {"transaction_type": "crypto_purchase"}
        }
        
        with patch('app.api.v1.webagent.get_current_user') as mock_user, \
             patch('app.api.v1.webagent.get_webagent_manager', new_callable=AsyncMock) as mock_manager:
            
            mock_user.return_value = Mock(id=1)
            mock_manager.return_value.__aenter__.return_value.search_financial_information = AsyncMock(
                return_value={"success": True, "result": {"price": 45000}}
            )
            
            response = client.post(
                "/api/v1/webagent/search/financial",
                json=request_data,
                headers=auth_headers
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["agent_used"] == "financial_search"


# Integration Tests
class TestWebAgentIntegration:
    """Integration tests for WebAgent system"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_financial_search(self):
        """Test end-to-end financial search flow"""
        # This would test the complete flow from API request to response
        # including agent initialization, tool usage, and result synthesis
        pass
    
    @pytest.mark.asyncio
    async def test_end_to_end_compliance_check(self):
        """Test end-to-end compliance checking flow"""
        # This would test the complete compliance checking process
        # including KYC verification, risk assessment, and reporting
        pass
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling of concurrent WebAgent requests"""
        # This would test the system's ability to handle multiple
        # simultaneous requests without conflicts
        pass


# Performance Tests
class TestWebAgentPerformance:
    """Performance tests for WebAgent system"""
    
    @pytest.mark.asyncio
    async def test_response_time_financial_search(self):
        """Test response time for financial search"""
        # This would measure and assert response times
        # for different types of financial queries
        pass
    
    @pytest.mark.asyncio
    async def test_cache_performance(self):
        """Test caching performance and hit rates"""
        # This would test the effectiveness of the caching system
        # and measure cache hit rates for repeated queries
        pass
    
    @pytest.mark.asyncio
    async def test_rate_limiting_behavior(self):
        """Test rate limiting behavior under load"""
        # This would test the rate limiting system's behavior
        # when request limits are approached or exceeded
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
