"""
WebAgent API Endpoints for Qpesapay
"""

import asyncio
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime

from app.webagent.core import get_webagent_manager, webagent_context
from app.webagent.config import get_webagent_config, validate_api_keys
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/webagent", tags=["webagent"])


# Request/Response Models
class FinancialSearchRequest(BaseModel):
    query: str = Field(..., description="Financial search query")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    user_id: Optional[str] = Field(None, description="User ID for personalized results")


class MarketAnalysisRequest(BaseModel):
    assets: List[str] = Field(..., description="List of assets to analyze")
    timeframe: str = Field("24h", description="Analysis timeframe")
    analysis_type: str = Field("comprehensive", description="Type of analysis")


class ComplianceCheckRequest(BaseModel):
    transaction_data: Dict[str, Any] = Field(..., description="Transaction data to check")
    check_type: str = Field("comprehensive", description="Type of compliance check")
    user_id: Optional[str] = Field(None, description="User ID")


class DevelopmentAnalysisRequest(BaseModel):
    file_path: str = Field("examples/tests/payment_tests.py", description="Path to file to analyze")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class TestCompletionRequest(BaseModel):
    file_path: str = Field(..., description="Path to test file")
    function_name: str = Field(..., description="Name of function to complete")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")


class WebAgentResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str
    agent_used: Optional[str] = None


class WebAgentStatusResponse(BaseModel):
    initialized: bool
    agents: Dict[str, Any]
    tools: Dict[str, Any]
    config: Dict[str, Any]


# API Endpoints
@router.get("/status", response_model=WebAgentStatusResponse)
async def get_webagent_status():
    """Get WebAgent system status"""
    try:
        async with webagent_context() as manager:
            status = manager.get_agent_status()
            return WebAgentStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get WebAgent status: {e}")


@router.post("/search/financial", response_model=WebAgentResponse)
async def search_financial_information(
    request: FinancialSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Search for financial information using WebDancer agent
    
    This endpoint provides autonomous financial information seeking with:
    - Multi-turn reasoning for complex queries
    - Real-time market data integration
    - Personalized results based on user context
    """
    try:
        # Add user context
        context = request.context.copy()
        context["user_id"] = str(current_user.id)
        context["user_tier"] = getattr(current_user, 'tier', 'basic')
        
        async with webagent_context() as manager:
            result = await manager.search_financial_information(
                query=request.query,
                context=context
            )
            
            return WebAgentResponse(
                success=result["success"],
                data=result if result["success"] else None,
                error=result.get("error") if not result["success"] else None,
                timestamp=datetime.now().isoformat(),
                agent_used="financial_search"
            )
            
    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="financial_search"
        )


@router.post("/analyze/market", response_model=WebAgentResponse)
async def analyze_market_conditions(
    request: MarketAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze market conditions using WebSailor agent
    
    This endpoint provides deep market analysis with:
    - Extended thinking for complex market dynamics
    - Technical and sentiment analysis
    - Price predictions and recommendations
    """
    try:
        async with webagent_context() as manager:
            result = await manager.analyze_market_conditions(
                assets=request.assets,
                timeframe=request.timeframe
            )
            
            return WebAgentResponse(
                success=result["success"],
                data=result if result["success"] else None,
                error=result.get("error") if not result["success"] else None,
                timestamp=datetime.now().isoformat(),
                agent_used="market_analysis"
            )
            
    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="market_analysis"
        )


@router.post("/check/compliance", response_model=WebAgentResponse)
async def check_compliance(
    request: ComplianceCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Check compliance using WebSailor agent
    
    This endpoint provides comprehensive compliance checking with:
    - Extended thinking for regulatory analysis
    - KYC/AML compliance verification
    - Risk assessment and scoring
    """
    try:
        # Add user context to transaction data
        transaction_data = request.transaction_data.copy()
        transaction_data["user_id"] = str(current_user.id)
        transaction_data["user_tier"] = getattr(current_user, 'tier', 'basic')
        
        async with webagent_context() as manager:
            result = await manager.check_compliance(
                transaction_data=transaction_data,
                check_type=request.check_type
            )
            
            return WebAgentResponse(
                success=result["success"],
                data=result if result["success"] else None,
                error=result.get("error") if not result["success"] else None,
                timestamp=datetime.now().isoformat(),
                agent_used="compliance"
            )
            
    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="compliance"
        )


@router.get("/crypto/price/{symbol}")
async def get_crypto_price(
    symbol: str,
    current_user: User = Depends(get_current_user)
):
    """Get current cryptocurrency price"""
    try:
        async with webagent_context() as manager:
            # Use crypto market tool directly
            crypto_tool = manager._tools.get("crypto_market")
            if not crypto_tool:
                raise HTTPException(status_code=503, detail="Crypto market tool not available")
            
            price_data = await crypto_tool.get_price(symbol.upper())
            
            return WebAgentResponse(
                success="error" not in price_data,
                data=price_data if "error" not in price_data else None,
                error=price_data.get("error"),
                timestamp=datetime.now().isoformat(),
                agent_used="crypto_market_tool"
            )
            
    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="crypto_market_tool"
        )


@router.get("/market/overview")
async def get_market_overview(
    current_user: User = Depends(get_current_user)
):
    """Get overall crypto market overview"""
    try:
        async with webagent_context() as manager:
            crypto_tool = manager._tools.get("crypto_market")
            if not crypto_tool:
                raise HTTPException(status_code=503, detail="Crypto market tool not available")
            
            overview_data = await crypto_tool.get_market_overview()
            
            return WebAgentResponse(
                success="error" not in overview_data,
                data=overview_data if "error" not in overview_data else None,
                error=overview_data.get("error"),
                timestamp=datetime.now().isoformat(),
                agent_used="crypto_market_tool"
            )
            
    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="crypto_market_tool"
        )


@router.post("/dev/analyze", response_model=WebAgentResponse)
async def analyze_development_tasks(
    request: DevelopmentAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze development tasks and provide completion suggestions

    This endpoint provides intelligent development assistance with:
    - Test completion analysis and suggestions
    - Code quality assessment
    - Implementation templates
    - Best practices recommendations
    """
    try:
        async with webagent_context() as manager:
            result = await manager.analyze_development_tasks(
                file_path=request.file_path,
                context=request.context
            )

            return WebAgentResponse(
                success=result["success"],
                data=result if result["success"] else None,
                error=result.get("error") if not result["success"] else None,
                timestamp=datetime.now().isoformat(),
                agent_used="dev_assistant"
            )

    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="dev_assistant"
        )


@router.post("/dev/complete-test", response_model=WebAgentResponse)
async def complete_test_function(
    request: TestCompletionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Complete a specific test function with intelligent implementation

    This endpoint provides:
    - Intelligent test implementation generation
    - Best practices integration
    - Security and validation patterns
    - Financial testing patterns for payment systems
    """
    try:
        async with webagent_context() as manager:
            result = await manager.complete_test_function(
                file_path=request.file_path,
                function_name=request.function_name,
                context=request.context
            )

            return WebAgentResponse(
                success=result["success"],
                data=result if result["success"] else None,
                error=result.get("error") if not result["success"] else None,
                timestamp=datetime.now().isoformat(),
                agent_used="dev_assistant"
            )

    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="dev_assistant"
        )


@router.get("/dev/payment-tests/analyze")
async def analyze_payment_tests(
    current_user: User = Depends(get_current_user)
):
    """
    Analyze payment tests specifically for completion suggestions

    This endpoint provides specialized analysis for financial testing:
    - Payment-specific test patterns
    - Security validation requirements
    - Decimal precision testing
    - Idempotency testing patterns
    """
    try:
        async with webagent_context() as manager:
            result = await manager.analyze_development_tasks(
                file_path="examples/tests/payment_tests.py",
                context={"analysis_type": "payment_specific"}
            )

            return WebAgentResponse(
                success=result["success"],
                data=result if result["success"] else None,
                error=result.get("error") if not result["success"] else None,
                timestamp=datetime.now().isoformat(),
                agent_used="dev_assistant"
            )

    except Exception as e:
        return WebAgentResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat(),
            agent_used="dev_assistant"
        )


# Utility endpoints
@router.get("/config/validate")
async def validate_webagent_config(
    current_user: User = Depends(get_current_user)
):
    """Validate WebAgent configuration and API keys"""
    try:
        validation_results = validate_api_keys()
        config = get_webagent_config()
        
        return {
            "api_keys_validation": validation_results,
            "configuration": {
                "model_server_url": f"http://{config.model_server_host}:{config.model_server_port}",
                "max_llm_calls": config.max_llm_calls_per_run,
                "cache_enabled": config.enable_cache,
                "rate_limiting_enabled": config.enable_rate_limiting
            },
            "recommendations": _generate_config_recommendations(validation_results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration validation failed: {e}")


def _generate_config_recommendations(validation_results: Dict[str, bool]) -> List[str]:
    """Generate configuration recommendations"""
    recommendations = []
    
    if not validation_results.get("google_search"):
        recommendations.append("Configure GOOGLE_SEARCH_KEY for web search capabilities")
    
    if not validation_results.get("jina_api"):
        recommendations.append("Configure JINA_API_KEY for content processing")
    
    if not validation_results.get("dashscope"):
        recommendations.append("Configure DASHSCOPE_API_KEY for model inference")
    
    if not validation_results.get("crypto_apis"):
        recommendations.append("Configure at least one crypto API (CoinMarketCap, CoinGecko, or Binance)")
    
    if not recommendations:
        recommendations.append("All API keys are properly configured")
    
    return recommendations


# Background task endpoints
@router.post("/tasks/market-monitoring")
async def start_market_monitoring(
    assets: List[str],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Start background market monitoring task"""
    try:
        background_tasks.add_task(_monitor_market_conditions, assets, str(current_user.id))
        
        return {
            "success": True,
            "message": f"Market monitoring started for {len(assets)} assets",
            "assets": assets,
            "user_id": str(current_user.id)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start market monitoring: {e}")


async def _monitor_market_conditions(assets: List[str], user_id: str):
    """Background task for market monitoring"""
    try:
        async with webagent_context() as manager:
            while True:
                # Analyze market conditions
                result = await manager.analyze_market_conditions(assets, "1h")
                
                # Check for significant changes or alerts
                if result["success"]:
                    analysis = result.get("analysis", {})
                    # Here you would implement alert logic
                    # For example, send notifications for significant price changes
                    pass
                
                # Wait before next analysis
                await asyncio.sleep(3600)  # 1 hour
                
    except Exception as e:
        # Log error and stop monitoring
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Market monitoring failed for user {user_id}: {e}")


# WebSocket endpoint for real-time updates (placeholder)
@router.websocket("/ws/market-updates")
async def websocket_market_updates(websocket):
    """WebSocket endpoint for real-time market updates"""
    # This would implement real-time market data streaming
    # using WebAgent tools for continuous market monitoring
    pass
