# Qpesapay Codebase Analysis

## Project Overview

**Qpesapay** is a web-first crypto-fiat payment processor specifically designed for the Kenya market. It enables seamless conversion between cryptocurrency (USDT) and Kenyan Shillings through M-Pesa integration, providing a secure and efficient payment gateway for businesses and individuals.

## Architecture Overview

### Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM (async)
- **Caching**: Redis
- **Authentication**: JWT with bcrypt
- **Payments**: M-Pesa Daraja API
- **Blockchain**: Ethereum, Tron, Bitcoin
- **Infrastructure**: Docker, Nginx
- **Testing**: Pytest with async support
- **CI/CD**: GitHub Actions

### Architectural Patterns
The codebase follows **Sandi Metz principles** for clean object-oriented design:
- **Single Responsibility Principle**: Small, focused classes and services
- **Dependency Injection**: Container-based dependency management
- **Command/Query Separation**: Separate command and query handlers
- **Domain-Driven Design**: Clear separation of domain logic
- **Service Layer Pattern**: Business logic encapsulated in services

## Directory Structure

```
backend/app/
├── api/v1/                    # API endpoints (FastAPI routers)
│   ├── endpoints/             # Individual endpoint modules
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── payments.py       # Payment processing endpoints
│   │   ├── webhooks.py       # Webhook handlers (M-Pesa)
│   │   ├── users.py          # User management
│   │   └── merchants.py      # Merchant management
│   └── api.py                # Router aggregation
├── core/                      # Core application components
│   ├── security.py           # JWT, password hashing, authentication
│   ├── security_audit.py     # Security enforcement and auditing
│   ├── middleware.py         # Request/response middleware
│   ├── exceptions.py         # Custom exception handling
│   ├── error_handlers.py     # Error response handling
│   ├── logging.py            # Structured logging setup
│   └── validation.py         # Input validation utilities
├── models/                    # SQLAlchemy database models
│   ├── user.py               # User model with KYC support
│   ├── wallet.py             # Cryptocurrency wallet management
│   ├── transaction.py        # Transaction records
│   ├── merchant.py           # Merchant account management
│   └── settlement.py         # Settlement processing
├── schemas/                   # Pydantic request/response models
│   ├── user.py               # User-related schemas
│   ├── wallet.py             # Wallet schemas
│   ├── transaction.py        # Transaction schemas
│   ├── merchant.py           # Merchant schemas
│   ├── settlement.py         # Settlement schemas
│   └── mpesa.py              # M-Pesa specific schemas
├── services/                  # Business logic services
│   ├── payment/              # Payment processing services
│   │   ├── validator.py      # Payment validation
│   │   ├── fee_estimator.py  # Fee calculation
│   │   ├── transaction_creator.py # Transaction creation
│   │   └── orchestrator.py   # Payment orchestration
│   ├── mpesa_service.py      # M-Pesa integration
│   └── blockchain_service.py # Blockchain interactions
├── domain/                    # Domain layer (DDD)
│   ├── value_objects.py      # Money, Address, PhoneNumber, etc.
│   └── entities.py           # PaymentRequest, TransactionRecord
├── commands/                  # Command pattern implementation
│   └── payment_commands.py   # Payment command handlers
├── queries/                   # Query pattern implementation
│   └── payment_queries.py    # Payment query handlers
├── middleware/                # Custom middleware
│   └── security_headers.py   # Security headers middleware
├── security/                  # Security-specific modules
│   └── dependency_scanner.py # Vulnerability scanning
├── tests/                     # Comprehensive test suite
│   ├── test_security.py      # Security feature tests
│   ├── test_api_security.py  # API security integration tests
│   ├── test_domain.py        # Domain logic tests
│   ├── test_payment_services.py # Payment service tests
│   ├── test_health.py        # Health check tests
│   └── conftest.py           # Test configuration
├── container.py              # Dependency injection container
├── config.py                 # Application configuration
├── database.py               # Database connection management
└── main.py                   # FastAPI application entry point
```

## Key Features & Components

### 1. Authentication & Security
- **JWT-based authentication** with access and refresh tokens
- **Password strength validation** with configurable policies
- **Account lockout mechanism** after failed login attempts
- **Token blacklisting** for secure logout
- **Rate limiting** on authentication endpoints
- **Security audit logging** for suspicious activities
- **OWASP-compliant security headers**
- **Input validation and sanitization**

### 2. Payment Processing
- **Multi-currency support**: USDT (Ethereum/Tron), Bitcoin, KES
- **M-Pesa integration** via Daraja API for KES transactions
- **Blockchain transaction handling** for crypto payments
- **Fee estimation** with static and dynamic providers
- **Payment validation** with amount limits and security checks
- **Transaction status tracking** with confirmation monitoring

### 3. User Management
- **KYC (Know Your Customer) support** with verification levels
- **Personal and merchant accounts**
- **Profile management** with secure data handling
- **Phone number validation** for Kenya (+254 format)
- **Email verification** workflows

### 4. Wallet Management
- **Multi-currency wallet support**
- **Secure private key handling** (encrypted storage)
- **Balance tracking** across different cryptocurrencies
- **Transaction history** with detailed records
- **Address generation** for receiving payments

### 5. Merchant Features
- **Business account management**
- **API key generation** for merchant integrations
- **Webhook configuration** for payment notifications
- **Settlement scheduling** (daily, weekly, monthly)
- **Transaction reporting** and analytics

## Database Models

### Core Models
1. **User**: Authentication, KYC, profile management
2. **Wallet**: Cryptocurrency wallet management
3. **Transaction**: Payment records and status tracking
4. **Merchant**: Business account and settings
5. **Settlement**: Batch payment processing

### Key Relationships
- Users can have multiple wallets (one per currency/network)
- Transactions link users, wallets, and payment methods
- Merchants extend user accounts with business features
- Settlements group multiple transactions for processing

## Security Implementation

### Authentication Flow
1. User registration with password strength validation
2. Email/phone verification
3. JWT token generation (access + refresh)
4. Token validation on protected endpoints
5. Automatic token refresh mechanism
6. Secure logout with token blacklisting

### Security Features
- **Password hashing** with bcrypt
- **Rate limiting** on sensitive endpoints
- **CSRF protection** via security headers
- **SQL injection prevention** through ORM
- **XSS protection** with input sanitization
- **Security audit logging** for compliance
- **Webhook signature validation** for M-Pesa callbacks

## Testing Strategy

### Test Coverage
- **Unit tests** for individual components
- **Integration tests** for API endpoints
- **Security tests** for authentication and validation
- **Domain tests** for business logic
- **Service tests** for payment processing

### Test Configuration
- Isolated test environment with test database
- Mock external services (M-Pesa, blockchain)
- Comprehensive test fixtures and factories
- Async test support with pytest-asyncio

## CI/CD Pipeline

### GitHub Actions Workflow
1. **Environment setup** with Python 3.11
2. **Service dependencies** (PostgreSQL, Redis)
3. **Dependency installation** with pip-tools
4. **Database migrations** with Alembic
5. **Test execution** with coverage reporting
6. **Security scanning** (planned)
7. **Coverage upload** to Codecov

## Configuration Management

### Environment Variables
- **Security keys** (SECRET_KEY, ENCRYPTION_KEY, WEBHOOK_SECRET)
- **Database configuration** (PostgreSQL connection)
- **External API keys** (M-Pesa, blockchain providers)
- **Rate limiting settings**
- **CORS configuration**
- **Logging levels**

### Production Considerations
- Secure secret management
- Environment-specific configurations
- Production-ready logging
- Performance monitoring setup
- Database connection pooling

## External Integrations

### M-Pesa Daraja API
- STK Push for payment initiation
- Callback handling for payment confirmation
- Transaction status tracking
- Error handling and retry logic

### Blockchain Networks
- **Ethereum**: USDT (ERC-20) transactions
- **Tron**: USDT (TRC-20) transactions  
- **Bitcoin**: Native BTC transactions
- Gas fee estimation and optimization
- Transaction confirmation monitoring

## Development Workflow

### Code Quality
- **Sandi Metz principles** for clean architecture
- **Type hints** throughout the codebase
- **Comprehensive documentation** in docstrings
- **Consistent code formatting** (implied)
- **Error handling** with custom exceptions

### Deployment
- **Docker containerization** ready
- **Database migrations** with Alembic
- **Environment configuration** management
- **Health check endpoints** for monitoring
- **Graceful startup/shutdown** handling

## Future Enhancements

### Planned Features
- Frontend application development
- Additional cryptocurrency support
- Advanced analytics and reporting
- Mobile application APIs
- Enhanced KYC verification
- Automated compliance reporting

### Technical Improvements
- Background task processing with Celery
- Caching optimization with Redis
- Performance monitoring integration
- Advanced security scanning
- Load balancing configuration
- Microservices architecture migration

## Conclusion

Qpesapay represents a well-architected, security-focused payment processing platform specifically designed for the Kenyan market. The codebase demonstrates strong adherence to software engineering best practices, comprehensive security measures, and a clear separation of concerns that makes it maintainable and scalable for future growth.
