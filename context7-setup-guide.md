# Context7 MCP Setup Guide for Qpesapay

## ✅ Installation Complete

Context7 MCP has been successfully installed and configured for your Qpesapay project!

## 🎯 Relevant Libraries for Your Project

Based on your `requirements.txt`, here are the most useful Context7 library IDs:

### Core Framework & API
- **FastAPI**: `/fastapi/fastapi` - Your main web framework
- **Uvicorn**: `/encode/uvicorn` - Your ASGI server  
- **Pydantic**: `/pydantic/pydantic` - Data validation and settings

### Database & ORM
- **SQLAlchemy**: `/sqlalchemy/sqlalchemy` - Your ORM
- **Alembic**: `/sqlalchemy/alembic` - Database migrations
- **AsyncPG**: `/magicstack/asyncpg` - PostgreSQL async driver

### Authentication & Security
- **Python-JOSE**: `/mpdavis/python-jose` - JWT handling
- **Passlib**: `/hynek/passlib` - Password hashing
- **Cryptography**: `/pyca/cryptography` - Encryption utilities

### HTTP & Async
- **HTTPX**: `/encode/httpx` - HTTP client for external APIs
- **AioHTTP**: `/aio-libs/aiohttp` - Alternative async HTTP

### Caching & Background Tasks
- **Redis**: `/redis/redis-py` - Caching and sessions
- **Celery**: `/celery/celery` - Background task processing

### Testing
- **Pytest**: `/pytest-dev/pytest` - Testing framework
- **Pytest-AsyncIO**: `/pytest-dev/pytest-asyncio` - Async testing

## 🚀 How to Use Context7

### Method 1: Natural Language with "use context7"
```
Create FastAPI middleware for JWT authentication with Redis caching. use context7
```

### Method 2: Specify Library ID Directly
```
Implement async SQLAlchemy models for payment transactions. use library /sqlalchemy/sqlalchemy for patterns
```

### Method 3: Multiple Libraries
```
Create FastAPI endpoint with Pydantic validation and async database operations. use context7 for /fastapi/fastapi and /pydantic/pydantic
```

## 🔧 Configuration Files Created

1. **`.augment/mcp-config.json`** - Augment Code MCP configuration
2. **`context7-setup-guide.md`** - This guide

## 🧪 Test Context7 Installation

Run this command to test:
```bash
npx -y @upstash/context7-mcp@latest --help
```

## 💡 Pro Tips

1. **Add a Rule**: Create a rule in Augment to auto-invoke Context7:
   ```
   When the user requests code examples, setup or configuration steps, or library/API documentation, use context7
   ```

2. **Use Specific Library IDs**: If you know the exact library, use the ID format:
   ```
   /fastapi/fastapi
   /sqlalchemy/sqlalchemy
   /pytest-dev/pytest
   ```

3. **Focus on Topics**: Add specific topics for better results:
   ```
   Create FastAPI authentication middleware. use context7 topic: middleware
   ```

## 🎯 Most Critical for Your Current Build

Given your CI/CD is running tests, these would be most immediately useful:

1. **FastAPI** (`/fastapi/fastapi`) - Core framework patterns
2. **Pytest** (`/pytest-dev/pytest`) - Testing best practices  
3. **SQLAlchemy** (`/sqlalchemy/sqlalchemy`) - Database patterns
4. **Pydantic** (`/pydantic/pydantic`) - Validation patterns

## 🔍 Example Queries for Your Project

### Payment Processing
```
Create FastAPI endpoint for USDT to KES conversion with M-Pesa integration. use context7
```

### Database Operations
```
Implement async SQLAlchemy models for cryptocurrency transactions with proper relationships. use library /sqlalchemy/sqlalchemy
```

### Authentication
```
Set up JWT authentication middleware with Redis session storage in FastAPI. use context7
```

### Testing
```
Write pytest fixtures for async FastAPI testing with database transactions. use library /pytest-dev/pytest
```

## ✅ Next Steps

1. **Test Context7** with a simple query in your AI assistant
2. **Add specific rules** for automatic Context7 invocation
3. **Use library-specific IDs** for better documentation quality
4. **Focus on your current development needs** (testing, payment processing, etc.)

Your Context7 MCP setup is ready to provide up-to-date documentation for all your Qpesapay development needs! 🚀
