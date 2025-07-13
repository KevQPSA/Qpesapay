"""
Market Analysis Agent - WebSailor-based agent for deep market analysis and forecasting
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from .base import WebSailorBasedAgent


class MarketAnalysisAgent(WebSailorBasedAgent):
    """
    Market Analysis Agent using WebSailor's extended thinking capabilities
    
    Specialized for:
    - Crypto market trend analysis
    - Fiat currency forecasting
    - Cross-market arbitrage opportunities
    - Market sentiment analysis
    - Price prediction and recommendations
    """
    
    def __init__(self, tools: List[Any], config: Any):
        super().__init__(tools, config, "market_analysis")
        self.analysis_timeframes = ["1h", "4h", "1d", "1w", "1m"]
        self.supported_assets = ["BTC", "ETH", "USDT", "KES", "USD", "EUR"]
        
    async def analyze_market(
        self, 
        assets: List[str], 
        timeframe: str = "24h"
    ) -> Dict[str, Any]:
        """
        Main market analysis method
        
        Args:
            assets: List of asset symbols to analyze
            timeframe: Analysis timeframe (1h, 4h, 1d, 1w, 1m)
            
        Returns:
            Comprehensive market analysis
        """
        await self._rate_limit_check()
        
        # Check cache first
        cache_key = self._get_cache_key(str(assets), {"timeframe": timeframe})
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        try:
            # Perform extended thinking analysis
            thinking_result = await self._extended_thinking(
                f"Market analysis for {assets} over {timeframe}", 
                {"assets": assets, "timeframe": timeframe}
            )
            
            # Execute market analysis
            analysis_result = await self._execute_market_analysis(
                assets, timeframe, thinking_result
            )
            
            # Generate predictions and recommendations
            predictions = await self._generate_market_predictions(
                assets, analysis_result, timeframe
            )
            
            # Create comprehensive report
            final_result = await self._generate_market_report(
                assets, analysis_result, predictions, thinking_result, timeframe
            )
            
            # Cache result
            self._set_cached_result(cache_key, final_result)
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"Market analysis failed: {e}")
            return {
                "success": False,
                "assets": assets,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_market_analysis(
        self, 
        assets: List[str], 
        timeframe: str,
        thinking_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute comprehensive market analysis"""
        
        analysis_result = {
            "timeframe": timeframe,
            "assets_analyzed": assets,
            "market_data": {},
            "technical_analysis": {},
            "sentiment_analysis": {},
            "correlation_analysis": {}
        }
        
        # Gather market data for each asset
        for asset in assets:
            try:
                market_data = await self._get_market_data(asset, timeframe)
                analysis_result["market_data"][asset] = market_data
                
                # Technical analysis
                technical = await self._perform_technical_analysis(asset, market_data)
                analysis_result["technical_analysis"][asset] = technical
                
                # Sentiment analysis
                sentiment = await self._analyze_market_sentiment(asset)
                analysis_result["sentiment_analysis"][asset] = sentiment
                
            except Exception as e:
                self.logger.error(f"Analysis failed for {asset}: {e}")
                analysis_result["market_data"][asset] = {"error": str(e)}
        
        # Cross-asset correlation analysis
        if len(assets) > 1:
            correlation = await self._analyze_correlations(assets, analysis_result["market_data"])
            analysis_result["correlation_analysis"] = correlation
        
        return analysis_result
    
    async def _get_market_data(self, asset: str, timeframe: str) -> Dict[str, Any]:
        """Get market data for specific asset"""
        # Use crypto market tool for crypto assets
        if asset in ["BTC", "ETH", "USDT"]:
            crypto_tool = next((tool for tool in self.tools if tool.name == "crypto_market"), None)
            if crypto_tool:
                return await crypto_tool.get_historical_data(asset, timeframe)
        
        # Use fiat rates tool for fiat currencies
        elif asset in ["KES", "USD", "EUR"]:
            fiat_tool = next((tool for tool in self.tools if tool.name == "fiat_rates"), None)
            if fiat_tool:
                return await fiat_tool.get_historical_rates(asset, timeframe)
        
        # Default market data structure
        return {
            "asset": asset,
            "current_price": 0.0,
            "price_change_24h": 0.0,
            "volume_24h": 0.0,
            "market_cap": 0.0,
            "historical_prices": [],
            "error": "Market data not available"
        }
    
    async def _perform_technical_analysis(self, asset: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform technical analysis on market data"""
        technical_analysis = {
            "asset": asset,
            "indicators": {},
            "signals": [],
            "trend": "neutral",
            "support_levels": [],
            "resistance_levels": []
        }
        
        historical_prices = market_data.get("historical_prices", [])
        if not historical_prices:
            return technical_analysis
        
        # Calculate technical indicators
        try:
            # Moving averages
            ma_20 = self._calculate_moving_average(historical_prices, 20)
            ma_50 = self._calculate_moving_average(historical_prices, 50)
            
            technical_analysis["indicators"]["ma_20"] = ma_20
            technical_analysis["indicators"]["ma_50"] = ma_50
            
            # RSI
            rsi = self._calculate_rsi(historical_prices)
            technical_analysis["indicators"]["rsi"] = rsi
            
            # Generate signals
            current_price = market_data.get("current_price", 0)
            
            if current_price > ma_20 > ma_50:
                technical_analysis["trend"] = "bullish"
                technical_analysis["signals"].append("Golden cross pattern")
            elif current_price < ma_20 < ma_50:
                technical_analysis["trend"] = "bearish"
                technical_analysis["signals"].append("Death cross pattern")
            
            if rsi > 70:
                technical_analysis["signals"].append("Overbought condition")
            elif rsi < 30:
                technical_analysis["signals"].append("Oversold condition")
            
            # Support and resistance levels
            technical_analysis["support_levels"] = self._find_support_levels(historical_prices)
            technical_analysis["resistance_levels"] = self._find_resistance_levels(historical_prices)
            
        except Exception as e:
            technical_analysis["error"] = f"Technical analysis failed: {e}"
        
        return technical_analysis
    
    async def _analyze_market_sentiment(self, asset: str) -> Dict[str, Any]:
        """Analyze market sentiment for asset"""
        sentiment_analysis = {
            "asset": asset,
            "overall_sentiment": "neutral",
            "sentiment_score": 0.0,
            "news_sentiment": "neutral",
            "social_sentiment": "neutral",
            "fear_greed_index": 50
        }
        
        # This would integrate with sentiment analysis APIs
        # For now, return mock data
        import random
        
        sentiment_score = random.uniform(-1, 1)
        sentiment_analysis["sentiment_score"] = sentiment_score
        
        if sentiment_score > 0.3:
            sentiment_analysis["overall_sentiment"] = "bullish"
        elif sentiment_score < -0.3:
            sentiment_analysis["overall_sentiment"] = "bearish"
        
        return sentiment_analysis
    
    async def _analyze_correlations(self, assets: List[str], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze correlations between assets"""
        correlation_analysis = {
            "assets": assets,
            "correlation_matrix": {},
            "strongest_correlations": [],
            "arbitrage_opportunities": []
        }
        
        # Calculate correlation matrix
        for asset1 in assets:
            correlation_analysis["correlation_matrix"][asset1] = {}
            for asset2 in assets:
                if asset1 != asset2:
                    correlation = self._calculate_correlation(
                        market_data.get(asset1, {}),
                        market_data.get(asset2, {})
                    )
                    correlation_analysis["correlation_matrix"][asset1][asset2] = correlation
        
        # Find arbitrage opportunities
        arbitrage_ops = await self._find_arbitrage_opportunities(assets, market_data)
        correlation_analysis["arbitrage_opportunities"] = arbitrage_ops
        
        return correlation_analysis
    
    async def _generate_market_predictions(
        self, 
        assets: List[str], 
        analysis_result: Dict[str, Any],
        timeframe: str
    ) -> Dict[str, Any]:
        """Generate market predictions based on analysis"""
        predictions = {
            "timeframe": timeframe,
            "predictions": {},
            "confidence_levels": {},
            "risk_assessments": {}
        }
        
        for asset in assets:
            try:
                # Get technical analysis for asset
                technical = analysis_result.get("technical_analysis", {}).get(asset, {})
                sentiment = analysis_result.get("sentiment_analysis", {}).get(asset, {})
                
                # Generate prediction
                prediction = await self._predict_price_movement(asset, technical, sentiment)
                predictions["predictions"][asset] = prediction
                
                # Calculate confidence
                confidence = self._calculate_prediction_confidence(technical, sentiment)
                predictions["confidence_levels"][asset] = confidence
                
                # Risk assessment
                risk = self._assess_prediction_risk(asset, technical, sentiment)
                predictions["risk_assessments"][asset] = risk
                
            except Exception as e:
                predictions["predictions"][asset] = {"error": str(e)}
        
        return predictions
    
    async def _predict_price_movement(
        self, 
        asset: str, 
        technical: Dict[str, Any], 
        sentiment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Predict price movement for asset"""
        prediction = {
            "asset": asset,
            "direction": "neutral",
            "magnitude": "low",
            "target_price": None,
            "probability": 0.5,
            "factors": []
        }
        
        # Analyze technical factors
        trend = technical.get("trend", "neutral")
        rsi = technical.get("indicators", {}).get("rsi", 50)
        
        # Analyze sentiment factors
        sentiment_score = sentiment.get("sentiment_score", 0)
        
        # Combine factors for prediction
        bullish_factors = 0
        bearish_factors = 0
        
        if trend == "bullish":
            bullish_factors += 1
            prediction["factors"].append("Bullish technical trend")
        elif trend == "bearish":
            bearish_factors += 1
            prediction["factors"].append("Bearish technical trend")
        
        if sentiment_score > 0.3:
            bullish_factors += 1
            prediction["factors"].append("Positive market sentiment")
        elif sentiment_score < -0.3:
            bearish_factors += 1
            prediction["factors"].append("Negative market sentiment")
        
        if rsi < 30:
            bullish_factors += 1
            prediction["factors"].append("Oversold condition")
        elif rsi > 70:
            bearish_factors += 1
            prediction["factors"].append("Overbought condition")
        
        # Determine prediction
        if bullish_factors > bearish_factors:
            prediction["direction"] = "bullish"
            prediction["probability"] = 0.6 + (bullish_factors - bearish_factors) * 0.1
        elif bearish_factors > bullish_factors:
            prediction["direction"] = "bearish"
            prediction["probability"] = 0.6 + (bearish_factors - bullish_factors) * 0.1
        
        return prediction
    
    def _calculate_moving_average(self, prices: List[float], period: int) -> float:
        """Calculate moving average"""
        if len(prices) < period:
            return 0.0
        return sum(prices[-period:]) / period
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _find_support_levels(self, prices: List[float]) -> List[float]:
        """Find support levels in price data"""
        # Simple implementation - find local minima
        support_levels = []
        
        for i in range(1, len(prices) - 1):
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                support_levels.append(prices[i])
        
        return sorted(list(set(support_levels)))[:3]  # Top 3 support levels
    
    def _find_resistance_levels(self, prices: List[float]) -> List[float]:
        """Find resistance levels in price data"""
        # Simple implementation - find local maxima
        resistance_levels = []
        
        for i in range(1, len(prices) - 1):
            if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                resistance_levels.append(prices[i])
        
        return sorted(list(set(resistance_levels)), reverse=True)[:3]  # Top 3 resistance levels
    
    def _calculate_correlation(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> float:
        """Calculate correlation between two assets"""
        # Simple correlation calculation
        prices1 = data1.get("historical_prices", [])
        prices2 = data2.get("historical_prices", [])
        
        if len(prices1) != len(prices2) or len(prices1) < 2:
            return 0.0
        
        # Calculate correlation coefficient
        import statistics
        
        try:
            correlation = statistics.correlation(prices1, prices2)
            return correlation
        except:
            return 0.0
    
    async def _find_arbitrage_opportunities(
        self, 
        assets: List[str], 
        market_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Find arbitrage opportunities between assets"""
        opportunities = []
        
        # Look for price discrepancies
        for i, asset1 in enumerate(assets):
            for asset2 in assets[i+1:]:
                data1 = market_data.get(asset1, {})
                data2 = market_data.get(asset2, {})
                
                price1 = data1.get("current_price", 0)
                price2 = data2.get("current_price", 0)
                
                if price1 > 0 and price2 > 0:
                    # Calculate potential arbitrage
                    price_diff = abs(price1 - price2) / max(price1, price2)
                    
                    if price_diff > 0.02:  # 2% threshold
                        opportunities.append({
                            "asset_pair": f"{asset1}/{asset2}",
                            "price_difference": price_diff,
                            "potential_profit": price_diff * 100,
                            "recommendation": f"Buy {asset1 if price1 < price2 else asset2}, sell {asset2 if price1 < price2 else asset1}"
                        })
        
        return opportunities
    
    def _calculate_prediction_confidence(
        self, 
        technical: Dict[str, Any], 
        sentiment: Dict[str, Any]
    ) -> float:
        """Calculate confidence level for predictions"""
        confidence = 0.5  # Base confidence
        
        # Technical analysis confidence
        if technical.get("trend") != "neutral":
            confidence += 0.2
        
        if len(technical.get("signals", [])) > 0:
            confidence += 0.1
        
        # Sentiment analysis confidence
        sentiment_score = abs(sentiment.get("sentiment_score", 0))
        confidence += sentiment_score * 0.2
        
        return min(confidence, 1.0)
    
    def _assess_prediction_risk(
        self, 
        asset: str, 
        technical: Dict[str, Any], 
        sentiment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess risk for prediction"""
        risk_assessment = {
            "overall_risk": "medium",
            "risk_factors": [],
            "risk_score": 0.5
        }
        
        # Volatility risk
        if asset in ["BTC", "ETH"]:
            risk_assessment["risk_factors"].append("High volatility asset")
            risk_assessment["risk_score"] += 0.2
        
        # Technical risk
        rsi = technical.get("indicators", {}).get("rsi", 50)
        if rsi > 70 or rsi < 30:
            risk_assessment["risk_factors"].append("Extreme RSI levels")
            risk_assessment["risk_score"] += 0.1
        
        # Sentiment risk
        sentiment_score = abs(sentiment.get("sentiment_score", 0))
        if sentiment_score > 0.8:
            risk_assessment["risk_factors"].append("Extreme sentiment levels")
            risk_assessment["risk_score"] += 0.1
        
        # Determine overall risk
        if risk_assessment["risk_score"] < 0.3:
            risk_assessment["overall_risk"] = "low"
        elif risk_assessment["risk_score"] > 0.7:
            risk_assessment["overall_risk"] = "high"
        
        return risk_assessment
    
    async def _generate_market_report(
        self,
        assets: List[str],
        analysis_result: Dict[str, Any],
        predictions: Dict[str, Any],
        thinking_result: Dict[str, Any],
        timeframe: str
    ) -> Dict[str, Any]:
        """Generate comprehensive market analysis report"""
        
        report = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "analysis_summary": {
                "assets": assets,
                "timeframe": timeframe,
                "analysis_depth": thinking_result.get("total_depth", 0)
            },
            "market_overview": self._create_market_overview(analysis_result),
            "detailed_analysis": analysis_result,
            "predictions": predictions,
            "recommendations": self._generate_market_recommendations(analysis_result, predictions),
            "risk_warnings": self._generate_risk_warnings(analysis_result, predictions),
            "next_actions": self._suggest_market_actions(predictions)
        }
        
        return report
    
    def _create_market_overview(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Create market overview summary"""
        overview = {
            "market_sentiment": "neutral",
            "dominant_trends": [],
            "key_opportunities": [],
            "major_risks": []
        }
        
        # Analyze overall sentiment
        sentiment_data = analysis_result.get("sentiment_analysis", {})
        bullish_count = sum(1 for s in sentiment_data.values() 
                          if s.get("overall_sentiment") == "bullish")
        bearish_count = sum(1 for s in sentiment_data.values() 
                          if s.get("overall_sentiment") == "bearish")
        
        if bullish_count > bearish_count:
            overview["market_sentiment"] = "bullish"
        elif bearish_count > bullish_count:
            overview["market_sentiment"] = "bearish"
        
        return overview
    
    def _generate_market_recommendations(
        self, 
        analysis_result: Dict[str, Any], 
        predictions: Dict[str, Any]
    ) -> List[str]:
        """Generate market recommendations"""
        recommendations = []
        
        # Analyze predictions for recommendations
        prediction_data = predictions.get("predictions", {})
        
        for asset, prediction in prediction_data.items():
            direction = prediction.get("direction", "neutral")
            confidence = predictions.get("confidence_levels", {}).get(asset, 0.5)
            
            if direction == "bullish" and confidence > 0.7:
                recommendations.append(f"Consider buying {asset} - strong bullish signals")
            elif direction == "bearish" and confidence > 0.7:
                recommendations.append(f"Consider selling {asset} - strong bearish signals")
        
        # Arbitrage opportunities
        arbitrage_ops = analysis_result.get("correlation_analysis", {}).get("arbitrage_opportunities", [])
        for op in arbitrage_ops[:2]:  # Top 2 opportunities
            recommendations.append(f"Arbitrage opportunity: {op['recommendation']}")
        
        return recommendations
    
    def _generate_risk_warnings(
        self, 
        analysis_result: Dict[str, Any], 
        predictions: Dict[str, Any]
    ) -> List[str]:
        """Generate risk warnings"""
        warnings = []
        
        # Check for high-risk predictions
        risk_assessments = predictions.get("risk_assessments", {})
        for asset, risk in risk_assessments.items():
            if risk.get("overall_risk") == "high":
                warnings.append(f"High risk detected for {asset}: {', '.join(risk.get('risk_factors', []))}")
        
        return warnings
    
    def _suggest_market_actions(self, predictions: Dict[str, Any]) -> List[str]:
        """Suggest next actions based on market analysis"""
        actions = []
        
        # General actions
        actions.extend([
            "Monitor market conditions closely",
            "Set up price alerts for significant movements",
            "Review and adjust risk management strategies"
        ])
        
        # Specific actions based on predictions
        high_confidence_predictions = [
            asset for asset, confidence in predictions.get("confidence_levels", {}).items()
            if confidence > 0.8
        ]
        
        if high_confidence_predictions:
            actions.append(f"Focus on high-confidence predictions: {', '.join(high_confidence_predictions)}")
        
        return actions
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of abstract method from base class"""
        # Extract assets and timeframe from context
        assets = context.get("assets", ["BTC", "ETH", "KES"])
        timeframe = context.get("timeframe", "24h")
        
        return await self.analyze_market(assets, timeframe)
