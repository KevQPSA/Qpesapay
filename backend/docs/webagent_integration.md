# WebAgent Integration for Qpesapay

## Overview

This document describes the integration of Alibaba's WebAgent technology into the Qpesapay platform, providing autonomous information seeking and advanced reasoning capabilities for financial operations.

## Architecture

### Core Components

1. **WebAgent Manager** (`app/webagent/core.py`)
   - Central orchestrator for all WebAgent operations
   - Manages agent lifecycle and tool registration
   - Provides high-level API for financial operations

2. **Specialized Agents**
   - **FinancialSearchAgent**: WebDancer-based multi-turn reasoning for complex financial queries
   - **ComplianceAgent**: WebSailor-based extended thinking for regulatory compliance
   - **MarketAnalysisAgent**: WebSailor-based deep market analysis and forecasting

3. **Financial Tools**
   - **CryptoMarketTool**: Real-time cryptocurrency market data
   - **FiatRatesTool**: Fiat currency exchange rates
   - **ComplianceCheckTool**: Regulatory compliance verification
   - **TransactionVerificationTool**: Transaction validation and monitoring

## Key Features

### 🎯 Financial Information Seeking
- **Multi-turn reasoning** for complex financial queries
- **Real-time market data** integration
- **Cross-market analysis** and arbitrage detection
- **Personalized results** based on user context

### 🛡️ Compliance & Risk Management
- **KYC/AML compliance** checking with extended thinking
- **Regulatory requirement** analysis for Kenya market
- **Risk assessment** and scoring
- **Transaction monitoring** and flagging

### 📊 Market Analysis & Forecasting
- **Technical analysis** with multiple indicators
- **Sentiment analysis** from multiple sources
- **Price prediction** with confidence scoring
- **Correlation analysis** between assets

## API Endpoints

### Financial Search
```http
POST /api/v1/webagent/search/financial
```
Search for financial information using WebDancer's multi-turn reasoning.

**Request:**
```json
{
  "query": "Current BTC to KES exchange rate and market trend",
  "context": {
    "transaction_type": "crypto_to_fiat",
    "amount": 50000
  }
}
```

### Market Analysis
```http
POST /api/v1/webagent/analyze/market
```
Analyze market conditions using WebSailor's extended thinking.

**Request:**
```json
{
  "assets": ["BTC", "ETH", "KES"],
  "timeframe": "24h",
  "analysis_type": "comprehensive"
}
```

### Compliance Check
```http
POST /api/v1/webagent/check/compliance
```
Check compliance using WebSailor's regulatory analysis.

**Request:**
```json
{
  "transaction_data": {
    "amount": 100000,
    "currency": "KES",
    "transaction_type": "crypto_to_fiat"
  },
  "check_type": "comprehensive"
}
```

## Configuration

### Required API Keys

1. **Google Search API** (via Serper)
   ```bash
   GOOGLE_SEARCH_KEY=your_serper_api_key
   ```

2. **Jina API** (for content processing)
   ```bash
   JINA_API_KEY=your_jina_api_key
   ```

3. **DashScope API** (for model inference)
   ```bash
   DASHSCOPE_API_KEY=your_dashscope_api_key
   ```

4. **Crypto APIs** (at least one required)
   ```bash
   COINMARKETCAP_API_KEY=your_coinmarketcap_key
   COINGECKO_API_KEY=your_coingecko_key
   BINANCE_API_KEY=your_binance_key
   ```

### Model Configuration

```bash
# Model paths (optional - uses cloud inference by default)
WEBDANCER_MODEL_PATH=/path/to/webdancer/model
WEBSAILOR_MODEL_PATH=/path/to/websailor/model

# Model server configuration
MODEL_SERVER_HOST=127.0.0.1
MODEL_SERVER_PORT=6001
```

### Runtime Configuration

```bash
# Performance settings
MAX_LLM_CALL_PER_RUN=40
MAX_TOKEN_LENGTH=31744
MAX_MULTIQUERY_NUM=3

# Feature flags
WEBAGENT_ENABLE_CACHE=true
WEBAGENT_CACHE_TTL=3600
WEBAGENT_RATE_LIMITING=true
WEBAGENT_MAX_REQUESTS_PER_MINUTE=60
```

## Usage Examples

### 1. Financial Information Search

```python
from app.webagent.core import get_webagent_manager

async def search_crypto_rates():
    manager = await get_webagent_manager()
    
    result = await manager.search_financial_information(
        query="What's the current BTC to KES rate and is it a good time to buy?",
        context={
            "user_id": "user123",
            "transaction_type": "crypto_purchase",
            "amount": 50000
        }
    )
    
    return result
```

### 2. Market Analysis

```python
async def analyze_crypto_market():
    manager = await get_webagent_manager()
    
    result = await manager.analyze_market_conditions(
        assets=["BTC", "ETH", "USDT"],
        timeframe="24h"
    )
    
    return result
```

### 3. Compliance Checking

```python
async def check_transaction_compliance():
    manager = await get_webagent_manager()
    
    result = await manager.check_compliance(
        transaction_data={
            "user_id": "user123",
            "amount": 100000,
            "currency": "KES",
            "transaction_type": "crypto_to_fiat",
            "country": "KE"
        },
        check_type="comprehensive"
    )
    
    return result
```

## Financial Use Cases

### 1. Crypto-Fiat Exchange Optimization
- **Real-time rate comparison** across multiple exchanges
- **Market timing recommendations** based on trend analysis
- **Arbitrage opportunity detection** between platforms

### 2. Regulatory Compliance Automation
- **Automated KYC/AML checks** for all transactions
- **Risk scoring** based on transaction patterns
- **Regulatory update monitoring** for Kenya financial laws

### 3. Market Intelligence
- **Crypto market sentiment** analysis from multiple sources
- **Price prediction** with confidence intervals
- **Cross-asset correlation** analysis for portfolio optimization

### 4. Customer Support Enhancement
- **Autonomous query resolution** for complex financial questions
- **Personalized recommendations** based on user history
- **Multi-language support** for Kenyan market

## Performance & Monitoring

### Caching Strategy
- **Query-level caching** with configurable TTL
- **Result deduplication** to reduce API calls
- **Cache invalidation** based on market volatility

### Rate Limiting
- **Per-user rate limiting** to prevent abuse
- **API quota management** across multiple services
- **Graceful degradation** when limits are reached

### Monitoring Metrics
- **Response times** for each agent type
- **Success rates** for different query types
- **API usage** and cost tracking
- **Cache hit rates** and performance

## Security Considerations

### API Key Management
- **Environment-based configuration** for all API keys
- **Rotation support** for long-term security
- **Access logging** for audit trails

### Data Privacy
- **User context isolation** between requests
- **PII scrubbing** in logs and caches
- **Compliance** with Kenya data protection laws

### Rate Limiting & Abuse Prevention
- **Per-user quotas** to prevent system abuse
- **Anomaly detection** for unusual usage patterns
- **Circuit breakers** for external API failures

## Deployment

### Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env`
3. Initialize WebAgent manager: `await get_webagent_manager()`

### Production Deployment
1. **Model server deployment** (optional for local inference)
2. **API key configuration** in secure environment
3. **Monitoring setup** for performance tracking
4. **Backup strategies** for cache and configuration

## Troubleshooting

### Common Issues

1. **API Key Validation Failures**
   - Check `/api/v1/webagent/config/validate` endpoint
   - Verify API key permissions and quotas

2. **Model Server Connection Issues**
   - Verify MODEL_SERVER_HOST and MODEL_SERVER_PORT
   - Check model server logs for errors

3. **Rate Limiting Errors**
   - Adjust WEBAGENT_MAX_REQUESTS_PER_MINUTE
   - Implement exponential backoff in client code

### Performance Optimization

1. **Enable caching** for frequently accessed data
2. **Optimize query patterns** to reduce API calls
3. **Use batch operations** where possible
4. **Monitor and tune** rate limiting parameters

## Future Enhancements

### Planned Features
- **WebSocket support** for real-time market updates
- **Advanced ML models** for better predictions
- **Multi-language support** for Swahili and other local languages
- **Integration with more** crypto exchanges and data sources

### Scalability Improvements
- **Horizontal scaling** of agent instances
- **Load balancing** across multiple model servers
- **Distributed caching** for better performance
- **Microservice architecture** for independent scaling
