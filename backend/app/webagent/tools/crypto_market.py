"""
Crypto Market Tool - Integration with cryptocurrency market data APIs
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CryptoMarketTool:
    """
    Tool for accessing cryptocurrency market data
    
    Integrates with multiple crypto APIs:
    - CoinMarketCap
    - CoinGecko
    - Binance
    """
    
    def __init__(self, config: Any):
        self.config = config
        self.name = "crypto_market"
        self.apis = config.crypto_apis
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for cryptocurrency"""
        try:
            # Try CoinMarketCap first
            if self.apis.get("coinmarketcap"):
                return await self._get_price_coinmarketcap(symbol)
            
            # Fallback to CoinGecko
            elif self.apis.get("coingecko"):
                return await self._get_price_coingecko(symbol)
            
            # Fallback to Binance
            elif self.apis.get("binance"):
                return await self._get_price_binance(symbol)
            
            else:
                return {"error": "No crypto API configured"}
                
        except Exception as e:
            logger.error(f"Failed to get price for {symbol}: {e}")
            return {"error": str(e)}
    
    async def _get_price_coinmarketcap(self, symbol: str) -> Dict[str, Any]:
        """Get price from CoinMarketCap API"""
        session = await self._get_session()
        
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {
            "X-CMC_PRO_API_KEY": self.apis["coinmarketcap"],
            "Accept": "application/json"
        }
        params = {"symbol": symbol, "convert": "USD,KES"}
        
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                if symbol in data.get("data", {}):
                    crypto_data = data["data"][symbol]
                    quote_usd = crypto_data["quote"]["USD"]
                    quote_kes = crypto_data["quote"].get("KES", {})
                    
                    return {
                        "symbol": symbol,
                        "name": crypto_data["name"],
                        "price_usd": quote_usd["price"],
                        "price_kes": quote_kes.get("price", 0),
                        "change_24h": quote_usd["percent_change_24h"],
                        "volume_24h": quote_usd["volume_24h"],
                        "market_cap": quote_usd["market_cap"],
                        "last_updated": quote_usd["last_updated"],
                        "source": "coinmarketcap"
                    }
                else:
                    return {"error": f"Symbol {symbol} not found"}
            else:
                return {"error": f"API request failed: {response.status}"}
    
    async def _get_price_coingecko(self, symbol: str) -> Dict[str, Any]:
        """Get price from CoinGecko API"""
        session = await self._get_session()
        
        # Convert symbol to CoinGecko ID
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum", 
            "USDT": "tether",
            "LTC": "litecoin",
            "XRP": "ripple"
        }
        
        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd,kes",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        
        headers = {}
        if self.apis.get("coingecko"):
            headers["x-cg-demo-api-key"] = self.apis["coingecko"]
        
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                if coin_id in data:
                    coin_data = data[coin_id]
                    
                    return {
                        "symbol": symbol.upper(),
                        "name": coin_id.title(),
                        "price_usd": coin_data.get("usd", 0),
                        "price_kes": coin_data.get("kes", 0),
                        "change_24h": coin_data.get("usd_24h_change", 0),
                        "volume_24h": coin_data.get("usd_24h_vol", 0),
                        "market_cap": coin_data.get("usd_market_cap", 0),
                        "last_updated": datetime.now().isoformat(),
                        "source": "coingecko"
                    }
                else:
                    return {"error": f"Coin {coin_id} not found"}
            else:
                return {"error": f"API request failed: {response.status}"}
    
    async def _get_price_binance(self, symbol: str) -> Dict[str, Any]:
        """Get price from Binance API"""
        session = await self._get_session()
        
        # Binance uses trading pairs
        trading_pair = f"{symbol}USDT"
        
        url = "https://api.binance.com/api/v3/ticker/24hr"
        params = {"symbol": trading_pair}
        
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                return {
                    "symbol": symbol,
                    "name": symbol,
                    "price_usd": float(data["lastPrice"]),
                    "price_kes": 0,  # Would need USD to KES conversion
                    "change_24h": float(data["priceChangePercent"]),
                    "volume_24h": float(data["volume"]),
                    "market_cap": 0,  # Not available from this endpoint
                    "last_updated": datetime.now().isoformat(),
                    "source": "binance"
                }
            else:
                return {"error": f"API request failed: {response.status}"}
    
    async def get_historical_data(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Get historical price data"""
        try:
            if self.apis.get("coingecko"):
                return await self._get_historical_coingecko(symbol, timeframe)
            else:
                return {"error": "No API configured for historical data"}
                
        except Exception as e:
            logger.error(f"Failed to get historical data for {symbol}: {e}")
            return {"error": str(e)}
    
    async def _get_historical_coingecko(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Get historical data from CoinGecko"""
        session = await self._get_session()
        
        # Convert symbol to CoinGecko ID
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "USDT": "tether"
        }
        
        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        
        # Convert timeframe to days
        days_map = {
            "1h": 1,
            "4h": 1, 
            "1d": 7,
            "1w": 30,
            "1m": 365
        }
        
        days = days_map.get(timeframe, 7)
        
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily" if days > 1 else "hourly"
        }
        
        headers = {}
        if self.apis.get("coingecko"):
            headers["x-cg-demo-api-key"] = self.apis["coingecko"]
        
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                prices = [price[1] for price in data.get("prices", [])]
                volumes = [vol[1] for vol in data.get("total_volumes", [])]
                market_caps = [mc[1] for mc in data.get("market_caps", [])]
                
                return {
                    "symbol": symbol.upper(),
                    "timeframe": timeframe,
                    "historical_prices": prices,
                    "historical_volumes": volumes,
                    "historical_market_caps": market_caps,
                    "current_price": prices[-1] if prices else 0,
                    "price_change_24h": ((prices[-1] - prices[0]) / prices[0] * 100) if len(prices) > 1 else 0,
                    "volume_24h": volumes[-1] if volumes else 0,
                    "market_cap": market_caps[-1] if market_caps else 0,
                    "source": "coingecko"
                }
            else:
                return {"error": f"API request failed: {response.status}"}
    
    async def get_market_overview(self) -> Dict[str, Any]:
        """Get overall crypto market overview"""
        try:
            if self.apis.get("coingecko"):
                return await self._get_market_overview_coingecko()
            else:
                return {"error": "No API configured for market overview"}
                
        except Exception as e:
            logger.error(f"Failed to get market overview: {e}")
            return {"error": str(e)}
    
    async def _get_market_overview_coingecko(self) -> Dict[str, Any]:
        """Get market overview from CoinGecko"""
        session = await self._get_session()
        
        url = "https://api.coingecko.com/api/v3/global"
        
        headers = {}
        if self.apis.get("coingecko"):
            headers["x-cg-demo-api-key"] = self.apis["coingecko"]
        
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                global_data = data.get("data", {})
                
                return {
                    "total_market_cap_usd": global_data.get("total_market_cap", {}).get("usd", 0),
                    "total_volume_24h_usd": global_data.get("total_volume", {}).get("usd", 0),
                    "bitcoin_dominance": global_data.get("market_cap_percentage", {}).get("btc", 0),
                    "ethereum_dominance": global_data.get("market_cap_percentage", {}).get("eth", 0),
                    "active_cryptocurrencies": global_data.get("active_cryptocurrencies", 0),
                    "markets": global_data.get("markets", 0),
                    "market_cap_change_24h": global_data.get("market_cap_change_percentage_24h_usd", 0),
                    "updated_at": global_data.get("updated_at", 0),
                    "source": "coingecko"
                }
            else:
                return {"error": f"API request failed: {response.status}"}
    
    def is_relevant(self, query: str) -> bool:
        """Check if this tool is relevant for the query"""
        crypto_keywords = [
            "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
            "usdt", "tether", "price", "market", "trading"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in crypto_keywords)
    
    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool based on query"""
        # Extract crypto symbols from query
        symbols = self._extract_symbols(query)
        
        if not symbols:
            symbols = ["BTC", "ETH", "USDT"]  # Default symbols
        
        results = {}
        
        # Get current prices
        for symbol in symbols:
            price_data = await self.get_price(symbol)
            results[symbol] = price_data
        
        # Get market overview if requested
        if "overview" in query.lower() or "market" in query.lower():
            overview = await self.get_market_overview()
            results["market_overview"] = overview
        
        return {
            "tool": self.name,
            "query": query,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_symbols(self, query: str) -> List[str]:
        """Extract crypto symbols from query"""
        import re
        
        # Common crypto symbols
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
    
    async def search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for crypto market information"""
        return await self.execute(query, context)
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session and not self.session.closed:
            await self.session.close()
