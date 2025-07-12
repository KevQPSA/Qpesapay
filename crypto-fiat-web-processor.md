name: "Web-First Crypto-Fiat Payment Processor - Kenya Market"
description: |

## Purpose

Build a comprehensive web-first dual-account payment ecosystem for Kenya that enables merchants to accept USDT payments with automatic KES settlement, and personal users to manage crypto wallets with M-Pesa integration. Focus on responsive web interfaces that work seamlessly on mobile browsers.

## Core Principles

1. **Web-First Architecture**: Responsive web applications that work on all devices
2. **Financial Security**: Bank-grade security with proper encryption and compliance
3. **Kenya Market Focus**: M-Pesa integration and local payment preferences
4. **Progressive Enhancement**: Start with core web functionality, mobile apps later
5. **Regulatory Compliance**: CBK, CMA guidelines and KYC/AML requirements

---

## Goal

Build a production-ready web-based crypto-fiat payment processor that serves both merchants and personal users in Kenya, with automatic USDT-to-KES conversion, M-Pesa settlement, and comprehensive compliance features.

## Why

- **Market Opportunity**: Bridge crypto adoption gap in Kenya's mobile-first economy
- **Merchant Value**: Enable businesses to accept crypto with fiat settlement
- **Personal Banking**: Provide crypto wallets with utility bill payment capabilities
- **Regulatory Approach**: Compliant financial services for emerging crypto market
- **Web-First Strategy**: Faster time-to-market with universal accessibility

## What

Web-based dual-account payment ecosystem with:

### Customer Web Portal (Responsive)
- USDT wallet management with mobile-optimized interface
- Buy USDT with M-Pesa, convert back to KES
- Pay utility bills (KPLC, Water, DSTV) directly from crypto
- P2P transfers and international remittances
- Progressive Web App (PWA) capabilities

### Merchant Dashboard (Next.js)
- Accept USDT payments with QR codes
- Automatic daily/weekly KES settlements to M-Pesa/Bank
- Sales analytics and tax reporting
- E-commerce API integration
- Multi-tier verification system

### Admin Panel (React)
- System monitoring and compliance oversight
- User management and KYC approval workflows
- Transaction monitoring and AML alerts
- Financial reporting and audit trails

### Success Criteria

- [ ] Responsive web interfaces work perfectly on mobile browsers
- [ ] USDT payments process with \u003c60 second confirmation
- [ ] M-Pesa settlements execute automatically within 2 hours
- [ ] Support 1000+ concurrent users with \u003c200ms response times
- [ ] 99.9% uptime with comprehensive monitoring
- [ ] Full CBK/CMA regulatory compliance
- [ ] Complete audit trail for all financial transactions
- [ ] Mobile-responsive design scores 95+ on Lighthouse

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Include these in your context window

# Kenya Payment Systems
- url: https://developer.safaricom.co.ke/
  why: M-Pesa Daraja API documentation for B2C payments and webhooks
  critical: STK Push implementation and callback handling

- url: https://developer.pesapal.com/
  why: Alternative payment processing for bank settlements
  section: API authentication and payment processing

# Blockchain & Crypto
- url: https://web3py.readthedocs.io/en/stable/
  why: Ethereum USDT transaction processing
  critical: Contract interaction and transaction monitoring

- url: https://tronpy.readthedocs.io/en/stable/
  why: Tron USDT transaction processing
  section: Wallet management and transaction signing

# Exchange Rate API for Real-Time USD/KES
- url: https://api.exchangerate-api.com/
  why: Real-time USD/KES exchange rate data
  critical: Rate caching and fallback strategies

- url: https://tether.to/
  why: USDT contract specifications and network details
  critical: Contract addresses and decimal handling

# Web Development Stack
- url: https://fastapi.tiangolo.com/
  why: API backend patterns and security implementation
  section: Authentication, dependency injection, async patterns

- url: https://nextjs.org/docs
  why: Full-stack React framework for frontend applications
  critical: Server-side rendering and API routes

- url: https://tailwindcss.com/docs
  why: Responsive design system for mobile-first interfaces

# Security & Compliance
- url: https://owasp.org/www-project-top-ten/
  why: Security best practices for financial applications

- file: examples/payment_gateway/payment_processor.py
  why: Secure USDT payment processing patterns with validation
  
- file: examples/wallet/secure_wallet.py
  why: HD wallet implementation with proper encryption
  
- file: examples/settlement/mpesa_settlement.py
  why: M-Pesa integration patterns and webhook handling

- file: examples/security/encryption_patterns.py
  why: Financial-grade encryption and data protection

- file: examples/testing/financial_testing_patterns.py
  why: Comprehensive testing patterns for financial systems

- file: .env.example
  why: Complete environment configuration template

- file: CLAUDE.md
  why: Project coding standards and security requirements
```

### Current Codebase Tree

```bash
context/
├── examples/                     # Existing patterns and implementations
│   ├── payment_gateway/
│   │   └── payment_processor.py  # USDT payment processing
│   ├── wallet/
│   │   └── secure_wallet.py      # HD wallet with encryption
│   ├── settlement/
│   │   └── mpesa_settlement.py   # M-Pesa integration
│   ├── security/
│   │   └── encryption_patterns.py
│   ├── testing/
│   │   └── financial_testing_patterns.py
│   └── README.md
├── PRPs/
│   └── templates/
├── .env.example                  # Complete configuration
├── CLAUDE.md                     # Development guidelines
├── INITIAL.md                    # Feature requirements
└── requirements.txt              # Dependencies
```

### Desired Codebase Tree (Web-First Implementation)

```bash
crypto-fiat-web/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app initialization
│   │   ├── config.py            # Pydantic settings
│   │   ├── database.py          # PostgreSQL connection
│   │   ├── redis_client.py      # Redis connection
│   │   │
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User accounts
│   │   │   ├── wallet.py        # Wallet management
│   │   │   ├── transaction.py   # Transaction records
│   │   │   └── merchant.py      # Merchant accounts
│   │   │
│   │   ├── schemas/             # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── payment.py       # Payment schemas
│   │   │   ├── wallet.py        # Wallet schemas
│   │   │   └── auth.py          # Authentication schemas
│   │   │
│   │   ├── api/                 # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── payments.py      # Payment processing
│   │   │   ├── wallets.py       # Wallet management
│   │   │   ├── merchants.py     # Merchant endpoints
│   │   │   └── admin.py         # Admin endpoints
│   │   │
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── payment_service.py      # Payment processing
│   │   │   ├── wallet_service.py       # Wallet operations
│   │   │   ├── mpesa_service.py        # M-Pesa integration
│   │   │   ├── blockchain_service.py   # USDT transactions
│   │   │   ├── settlement_service.py   # Settlement automation
│   │   │   └── compliance_service.py   # KYC/AML checks
│   │   │
│   │   ├── core/                # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py      # JWT and encryption
│   │   │   ├── exceptions.py    # Custom exceptions
│   │   │   ├── middleware.py    # Custom middleware
│   │   │   └── logging.py       # Structured logging
│   │   │
│   │   └── tests/               # Test suite
│   │       ├── __init__.py
│   │       ├── conftest.py      # Pytest fixtures
│   │       ├── test_auth.py
│   │       ├── test_payments.py
│   │       └── test_wallets.py
│   │
│   ├── alembic/                 # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                    # Next.js Frontend Applications
│   ├── customer-portal/         # Customer web portal
│   │   ├── pages/
│   │   │   ├── index.tsx        # Landing page
│   │   │   ├── login.tsx        # Authentication
│   │   │   ├── dashboard.tsx    # Main dashboard
│   │   │   ├── wallet.tsx       # Wallet management
│   │   │   ├── payments.tsx     # Payment interface
│   │   │   ├── bills.tsx        # Utility bill payments
│   │   │   └── history.tsx      # Transaction history
│   │   ├── components/
│   │   │   ├── layout/          # Layout components
│   │   │   ├── forms/           # Form components
│   │   │   ├── wallet/          # Wallet components
│   │   │   └── payments/        # Payment components
│   │   ├── styles/
│   │   │   └── globals.css      # Tailwind CSS
│   │   ├── utils/
│   │   │   ├── api.ts           # API client
│   │   │   ├── wallet.ts        # Wallet utilities
│   │   │   └── validation.ts    # Form validation
│   │   ├── hooks/               # Custom React hooks
│   │   ├── public/              # Static assets
│   │   ├── next.config.js
│   │   ├── package.json
│   │   └── tailwind.config.js
│   │
│   ├── merchant-dashboard/      # Merchant dashboard
│   │   ├── pages/
│   │   │   ├── index.tsx        # Overview
│   │   │   ├── analytics.tsx    # Sales analytics
│   │   │   ├── payments.tsx     # Payment management
│   │   │   ├── settlements.tsx  # Settlement tracking
│   │   │   └── integration.tsx  # API integration
│   │   ├── components/
│   │   ├── utils/
│   │   └── [same structure as customer-portal]
│   │
│   └── admin-panel/             # Admin panel (React)
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── services/
│       │   └── utils/
│       ├── public/
│       ├── package.json
│       └── vite.config.ts
│
├── docker/                      # Docker configuration
│   ├── docker-compose.yml       # Development environment
│   ├── docker-compose.prod.yml  # Production environment
│   └── nginx/                   # Nginx configuration
│
├── scripts/                     # Utility scripts
│   ├── setup.sh                 # Environment setup
│   ├── deploy.sh                # Deployment script
│   └── backup.sh                # Database backup
│
├── docs/                        # Documentation
│   ├── api/                     # API documentation
│   ├── deployment/              # Deployment guides
│   └── security/                # Security documentation
│
├── .env.example                 # Environment template
├── .gitignore
├── README.md
└── CLAUDE.md                    # AI development guidelines
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: Financial system requirements
# NEVER use float for monetary calculations - always Decimal
amount = Decimal('100.000000')  # USDT with 6 decimals
kes_amount = amount * exchange_rate  # Decimal arithmetic

# CRITICAL: FastAPI async patterns
async def process_payment(request: PaymentRequest) -> PaymentResponse:
    # All database operations must be async
    async with get_db_session() as session:
        # Use async session methods
        result = await session.execute(query)

# CRITICAL: Next.js API routes for backend communication & production
// pages/api/payments.ts - GOTCHA: File-based routing
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    // Validate request method first
    if (req.method !== 'POST') {
        return res.status(405).json({error: 'Method not allowed'})
    }
    // Always use HTTPS in production
}

# CRITICAL: PostgreSQL decimal handling
# Use NUMERIC type for all currency fields
class Transaction(Base):
    amount_usdt = Column(NUMERIC(20, 6))  # 6 decimal places for USDT
    amount_kes = Column(NUMERIC(20, 2))   # 2 decimal places for KES

# CRITICAL: M-Pesa webhook signature verification
def verify_mpesa_signature(payload: str, signature: str) -> bool:
    # Always verify webhook signatures
    expected = hmac.new(webhook_secret, payload.encode(), hashlib.sha256)
    return hmac.compare_digest(expected.hexdigest(), signature)

# CRITICAL: Blockchain transaction monitoring
async def monitor_transaction(tx_hash: str, required_confirmations: int = 3):
    # Always wait for sufficient confirmations
    confirmations = 0
    while confirmations < required_confirmations:
        await asyncio.sleep(30)  # Check every 30 seconds
        confirmations = await get_transaction_confirmations(tx_hash)

# CRITICAL: Rate limiting for financial APIs
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/payments")
@limiter.limit("10/minute")  # Strict rate limiting
async def create_payment():
    pass

# CRITICAL: Responsive design for mobile browsers
// Tailwind CSS mobile-first approach
<div className="w-full px-4 sm:px-6 lg:px-8">
  <div className="max-w-md mx-auto sm:max-w-lg lg:max-w-xl">
    {/* Mobile-optimized component */}
  </div>
</div>
```

## Implementation Blueprint

### Existing Codebase Pattern References

**CRITICAL: Follow these exact patterns from the existing examples/**

**Payment Processing (examples/payment_gateway/payment_processor.py):**
```python
# PATTERN: Secure payment validation and processing
class PaymentProcessor:
    async def process_payment(self, request: PaymentRequest) -> Dict[str, Any]:
        # PATTERN: Comprehensive logging for audit trail
        await self._log_payment_attempt(request)
        
        # PATTERN: Validate request thoroughly
        await self._validate_payment_request(request)
        
        # PATTERN: Check for duplicate transactions (idempotency)
        if await self._is_duplicate_transaction(request.transaction_id):
            return await self._get_existing_transaction(request.transaction_id)
        
        # PATTERN: Monitor transaction confirmation with exponential backoff
        confirmed_tx = await self._monitor_transaction_confirmation(
            blockchain_tx['hash'], request.network
        )
```

**Dual-Account Ecosystem (examples/integrations/dual_account_ecosystem.py):**
```python
# PATTERN: Cross-account payment processing
async def process_personal_to_merchant_payment(
    self, personal_account_id: str, merchant_account_id: str,
    amount_kes: Decimal, payment_method: PaymentMethod
) -> Dict[str, Any]:
    # PATTERN: Fee structure based on payment method
    fee_rate = self.fee_structure[payment_method]
    platform_fee = amount_kes * fee_rate
    
    # PATTERN: Calculate USDT requirements with proper conversion
    usdt_amount = (amount_kes + platform_fee) / exchange_rate
```

**Security Patterns (examples/security/encryption_patterns.py):**
```python
# PATTERN: Encrypted private key storage
class SecureWallet:
    def _encrypt_private_key(self, private_key: str, password: str) -> str:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,  # CRITICAL: High iteration count
        )
```

**M-Pesa Integration (examples/settlement/mpesa_settlement.py):**
```python
# PATTERN: Kenya-specific phone number validation
def _validate_kenyan_phone(self, phone: str) -> bool:
    patterns = [
        r'^\+254[17]\d{8}$',  # +254 format  
        r'^254[17]\d{8}$',    # 254 format
        r'^0[17]\d{8}$'       # 0 format
    ]
    return any(re.match(pattern, phone) for pattern in patterns)
```

### Data Models and Structure

Create comprehensive data models for type safety and consistency:

```python
# Core SQLAlchemy models
from sqlalchemy import Column, String, NUMERIC, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from decimal import Decimal
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    account_type = Column(String(20), nullable=False)  # 'personal' or 'merchant'
    kyc_status = Column(String(20), default='pending')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    network = Column(String(20), nullable=False)  # 'ethereum' or 'tron'
    address = Column(String(255), nullable=False)
    encrypted_private_key = Column(Text, nullable=False)
    balance_usdt = Column(NUMERIC(20, 6), default=0)
    balance_kes = Column(NUMERIC(20, 2), default=0)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    transaction_type = Column(String(50), nullable=False)
    amount_usdt = Column(NUMERIC(20, 6))
    amount_kes = Column(NUMERIC(20, 2))
    exchange_rate = Column(NUMERIC(10, 4))
    status = Column(String(20), default='pending')
    blockchain_hash = Column(String(255))
    mpesa_reference = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic schemas for API validation
class PaymentRequest(BaseModel):
    amount_usdt: Decimal = Field(..., gt=0, decimal_places=6)
    recipient_address: str = Field(..., min_length=30)
    network: Literal['ethereum', 'tron']
    merchant_id: Optional[str] = None
    
    @validator('amount_usdt')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    blockchain_hash: Optional[str]
    estimated_confirmation_time: int
    gas_fee: Decimal
```

### List of Tasks (Implementation Order)

```yaml
Task 1 - Backend Foundation:
CREATE backend/app/main.py:
  - PATTERN: FastAPI app with proper CORS and middleware
  - INCLUDE: Structured logging, exception handling
  - SECURITY: Rate limiting, request validation
  - REFERENCE: examples/payment_gateway/ for patterns

CREATE backend/app/config.py:
  - PATTERN: Pydantic settings with environment validation
  - INCLUDE: Database URLs, API keys, security settings
  - REFERENCE: .env.example for complete configuration

CREATE backend/app/database.py:
  - PATTERN: Async PostgreSQL connection with pooling
  - INCLUDE: Session management, transaction handling
  - REFERENCE: examples/security/ for encryption patterns

Task 2 - Authentication System:
CREATE backend/app/core/security.py:
  - PATTERN: JWT token generation and validation
  - INCLUDE: Password hashing, 2FA support
  - SECURITY: Proper token expiration and refresh

CREATE backend/app/api/auth.py:
  - PATTERN: Authentication endpoints with validation
  - INCLUDE: Login, register, password reset
  - REFERENCE: existing auth patterns in examples/

CREATE backend/app/services/auth_service.py:
  - PATTERN: Business logic for user management
  - INCLUDE: KYC verification, account activation
  - SECURITY: Rate limiting, brute force protection

Task 3 - Payment Processing:
CREATE backend/app/services/payment_service.py:
  - MIRROR: examples/payment_gateway/payment_processor.py
  - MODIFY: Add web-specific validation and responses
  - PRESERVE: All security patterns and error handling

CREATE backend/app/services/blockchain_service.py:
  - PATTERN: USDT transaction processing for both networks
  - INCLUDE: Transaction monitoring, gas estimation
  - REFERENCE: examples/wallet/ for wallet patterns

CREATE backend/app/api/payments.py:
  - PATTERN: RESTful payment endpoints
  - INCLUDE: Payment creation, status checking, history
  - SECURITY: Proper validation and rate limiting

Task 4 - M-Pesa Integration:
CREATE backend/app/services/mpesa_service.py:
  - MIRROR: examples/settlement/mpesa_settlement.py
  - MODIFY: Add webhook handling and B2C payments
  - PRESERVE: All security and validation patterns

CREATE backend/app/api/webhooks.py:
  - PATTERN: Webhook endpoints for M-Pesa callbacks
  - INCLUDE: Signature verification, idempotency
  - SECURITY: Proper request validation

Task 5 - Customer Web Portal (Next.js):
CREATE frontend/customer-portal/pages/dashboard.tsx:
  - PATTERN: Mobile-first responsive dashboard
  - INCLUDE: Wallet balance, recent transactions
  - DESIGN: Tailwind CSS with mobile optimization

CREATE frontend/customer-portal/components/wallet/WalletInterface.tsx:
  - PATTERN: USDT wallet management component
  - INCLUDE: Send, receive, balance display
  - MOBILE: Touch-friendly interface elements

CREATE frontend/customer-portal/pages/payments.tsx:
  - PATTERN: Payment creation and management
  - INCLUDE: QR code scanning, amount input
  - VALIDATION: Client-side form validation

CREATE frontend/customer-portal/utils/api.ts:
  - PATTERN: API client with authentication
  - INCLUDE: Request/response interceptors
  - SECURITY: Token management, CSRF protection

Task 6 - Merchant Dashboard:
CREATE frontend/merchant-dashboard/pages/analytics.tsx:
  - PATTERN: Business analytics dashboard
  - INCLUDE: Charts, transaction summaries
  - DESIGN: Professional business interface

CREATE frontend/merchant-dashboard/components/payments/PaymentManagement.tsx:
  - PATTERN: Payment processing interface
  - INCLUDE: QR code generation, settlement tracking
  - FEATURES: Bulk operations, export functionality

Task 7 - Admin Panel (React):
CREATE frontend/admin-panel/src/pages/SystemMonitoring.tsx:
  - PATTERN: Real-time system monitoring
  - INCLUDE: Transaction monitoring, system health
  - FEATURES: Alerts, user management

CREATE frontend/admin-panel/src/components/compliance/ComplianceTools.tsx:
  - PATTERN: KYC/AML management interface
  - INCLUDE: User verification, transaction flagging
  - SECURITY: Role-based access control

Task 8 - Database Schema:
CREATE backend/alembic/versions/001_initial_schema.py:
  - PATTERN: Complete database schema migration
  - INCLUDE: All tables, indexes, constraints
  - REFERENCE: examples/ for table structures

Task 9 - Testing Suite:
CREATE backend/app/tests/test_payments.py:
  - MIRROR: examples/testing/financial_testing_patterns.py
  - MODIFY: Add web-specific test cases
  - INCLUDE: Integration tests, security tests

CREATE frontend/customer-portal/__tests__/wallet.test.tsx:
  - PATTERN: React component testing
  - INCLUDE: User interaction tests, responsive tests
  - TOOLS: Jest, React Testing Library

Task 10 - DevOps Setup:
CREATE docker/docker-compose.yml:
  - PATTERN: Complete development environment
  - INCLUDE: PostgreSQL, Redis, backend, frontends
  - SERVICES: Nginx reverse proxy, SSL termination

CREATE scripts/deploy.sh:
  - PATTERN: Production deployment script
  - INCLUDE: Database migrations, frontend builds
  - SECURITY: Environment validation, backup procedures
```

### Per Task Pseudocode

```python
# Task 1 - Backend Foundation
# FastAPI app with comprehensive middleware
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="Crypto-Fiat Payment Processor",
    description="Kenya Market Payment Gateway",
    version="1.0.0"
)

# SECURITY: Proper CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# PATTERN: Rate limiting middleware
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# PATTERN: Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    return response

# Task 3 - Payment Processing
async def process_usdt_payment(payment_request: PaymentRequest) -> PaymentResponse:
    # PATTERN: Comprehensive validation first
    await validate_payment_request(payment_request)
    
    # PATTERN: Database transaction for consistency
    async with get_db_session() as session:
        # CRITICAL: Check for duplicate transaction
        existing = await check_duplicate_transaction(payment_request.transaction_id)
        if existing:
            return existing
        
        # PATTERN: Estimate fees before processing
        gas_estimate = await estimate_transaction_fees(payment_request)
        
        # PATTERN: Create pending transaction record
        transaction = await create_transaction_record(payment_request, gas_estimate)
        
        try:
            # PATTERN: Execute blockchain transaction
            blockchain_result = await execute_blockchain_transaction(payment_request)
            
            # PATTERN: Update transaction with blockchain hash
            await update_transaction_status(
                transaction.id, 
                "confirmed", 
                blockchain_result["hash"]
            )
            
            # PATTERN: Trigger settlement if merchant payment
            if payment_request.merchant_id:
                await trigger_merchant_settlement(payment_request, blockchain_result)
            
            return PaymentResponse(
                transaction_id=transaction.id,
                status="confirmed",
                blockchain_hash=blockchain_result["hash"],
                estimated_confirmation_time=180,  # 3 minutes
                gas_fee=gas_estimate
            )
            
        except Exception as e:
            # PATTERN: Rollback on failure
            await update_transaction_status(transaction.id, "failed", None)
            raise PaymentError(f"Payment processing failed: {str(e)}")

# Task 5 - Customer Web Portal
// Mobile-first responsive wallet interface
const WalletInterface: React.FC = () => {
  const [balance, setBalance] = useState<Decimal>(new Decimal(0))
  const [isLoading, setIsLoading] = useState(true)
  
  // PATTERN: Mobile-optimized layout
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-md mx-auto px-4 py-6">
        {/* PATTERN: Mobile-friendly balance display */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">
            USDT Balance
          </h2>
          <p className="text-3xl font-bold text-blue-600">
            {balance.toFixed(6)} USDT
          </p>
          <p className="text-sm text-gray-500 mt-1">
            ≈ {(balance.mul(exchangeRate)).toFixed(2)} KES
          </p>
        </div>
        
        {/* PATTERN: Touch-friendly action buttons */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <TouchButton
            icon={<SendIcon />}
            label="Send"
            onClick={() => navigate('/send')}
            className="bg-blue-600 text-white"
          />
          <TouchButton
            icon={<ReceiveIcon />}
            label="Receive"
            onClick={() => navigate('/receive')}
            className="bg-green-600 text-white"
          />
        </div>
        
        {/* PATTERN: Recent transactions list */}
        <TransactionList 
          transactions={recentTransactions}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}
```

### Integration Points

```yaml
DATABASE:
  - migrations: "Create comprehensive schema with proper indexes"
  - indexes: "CREATE INDEX idx_transactions_user_date ON transactions(user_id, created_at)"
  - constraints: "ADD CONSTRAINT check_positive_amounts CHECK (amount_usdt > 0)"

BLOCKCHAIN:
  - ethereum: "Connect to Infura/Alchemy for USDT contract interaction"
  - tron: "Connect to TronGrid API for Tron USDT transactions"
  - monitoring: "Real-time transaction confirmation tracking"

MPESA:
  - daraja_api: "Integration with M-Pesa API for B2C payments"
  - webhooks: "Secure webhook handling for payment confirmations"
  - settlement: "Automated daily/weekly settlement to merchant accounts"

FRONTEND:
  - api_client: "Centralized API client with authentication"
  - state_management: "React Context for global state management"
  - responsive: "Mobile-first responsive design with Tailwind CSS"

SECURITY:
  - encryption: "Field-level encryption for sensitive data"
  - jwt: "Proper JWT token management with refresh tokens"
  - rate_limiting: "Comprehensive rate limiting on all endpoints"
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Backend validation
cd backend
uv run ruff check app/ --fix
uv run mypy app/
uv run black app/

# Frontend validation
cd frontend/customer-portal
npm run lint
npm run type-check
npm run build

cd ../merchant-dashboard
npm run lint
npm run type-check
npm run build

cd ../admin-panel
npm run lint
npm run type-check
npm run build

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests

```python
# Backend unit tests
cd backend
uv run pytest app/tests/ -v --cov=app --cov-report=html

# Key test categories:
def test_concurrent_payment_processing():
    """Test handling multiple simultaneous payments"""
    # Critical for preventing double-spending
    # Simulate concurrent requests using asyncio.gather
    async def send_concurrent_payments():
        requests = [payment_service.process_payment(PaymentRequest(
            amount_usdt=Decimal('100.000000'),
            recipient_address='0x742d35Cc6634C0532925a3b8D',
            network='ethereum'
        )) for _ in range(10)]
        results = await asyncio.gather(*requests)
        assert all(result.status == "confirmed" for result in results)
    """Test successful USDT payment processing"""
    payment_request = PaymentRequest(
        amount_usdt=Decimal('100.000000'),
        recipient_address='0x742d35Cc6634C0532925a3b8D',
        network='ethereum'
    )
    result = await payment_service.process_payment(payment_request)
    assert result.status == "confirmed"
    assert result.blockchain_hash is not None

def test_payment_validation_errors():
    """Test payment validation with invalid inputs"""
    with pytest.raises(ValidationError):
        PaymentRequest(
            amount_usdt=Decimal('-100.000000'),  # Negative amount
            recipient_address='invalid_address',
            network='ethereum'
        )

def test_mpesa_settlement_integration():
    """Test M-Pesa B2C payment settlement"""
    settlement_request = SettlementRequest(
        merchant_id='test_merchant',
        amount_kes=Decimal('13050.00'),
        phone_number='+254700000000'
    )
    result = await mpesa_service.initiate_b2c_payment(settlement_request)
    assert result.status == "success"
    assert result.mpesa_reference is not None
```

```javascript
// Frontend unit tests
// customer-portal/__tests__/wallet.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { WalletInterface } from '../components/wallet/WalletInterface'

test('displays wallet balance correctly', async () => {
  render(<WalletInterface />)
  
  // Wait for balance to load
  await waitFor(() => {
    expect(screen.getByText(/USDT Balance/)).toBeInTheDocument()
  })
  
  // Check balance display
  expect(screen.getByText(/100.000000 USDT/)).toBeInTheDocument()
  expect(screen.getByText(/≈ 13,050.00 KES/)).toBeInTheDocument()
})

test('mobile responsive design', () => {
  // Test mobile viewport
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: 375,
  })
  
  render(<WalletInterface />)
  
  // Check mobile-specific elements
  expect(screen.getByTestId('mobile-wallet-layout')).toBeVisible()
})
```

### Level 3: Integration Tests

```bash
# Start development environment
docker-compose -f docker/docker-compose.yml up -d

# Wait for services to be ready
sleep 30

# Test backend API endpoints
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "phone_number": "+254700000000",
    "account_type": "personal"
  }'

# Test payment processing
curl -X POST http://localhost:8000/api/payments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "amount_usdt": "100.000000",
    "recipient_address": "0x742d35Cc6634C0532925a3b8D",
    "network": "ethereum"
  }'

# Test frontend applications
curl -I http://localhost:3000  # Customer portal
curl -I http://localhost:3001  # Merchant dashboard
curl -I http://localhost:3002  # Admin panel

# Expected responses: 200 OK for all endpoints
# If errors: Check logs at logs/app.log for stack traces

## Detailed Deployment Integration Points

### Infrastructure and Environment Setup

**Docker Configuration (docker/docker-compose.yml):**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/cryptopay
      - REDIS_URL=redis://redis:6379
      - MPESA_CONSUMER_KEY=${MPESA_CONSUMER_KEY}
      - BLOCKCHAIN_RPC_URL=${BLOCKCHAIN_RPC_URL}
    depends_on:
      - postgres
      - redis
  
  frontend-customer:
    build: ./frontend/customer-portal
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx:/etc/nginx/conf.d
      - ./ssl:/etc/ssl
```

**Environment Variables (.env.production):**
```bash
# Database
DATABASE_URL=postgresql://cryptopay_user:${DB_PASSWORD}@localhost:5432/cryptopay_prod
REDIS_URL=redis://localhost:6379/0

# Blockchain
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/${INFURA_PROJECT_ID}
TRON_RPC_URL=https://api.trongrid.io

# M-Pesa (Production)
MPESA_ENVIRONMENT=production
MPESA_CONSUMER_KEY=${MPESA_PROD_CONSUMER_KEY}
MPESA_CONSUMER_SECRET=${MPESA_PROD_CONSUMER_SECRET}
MPESA_SHORTCODE=${MPESA_PROD_SHORTCODE}
MPESA_PASSKEY=${MPESA_PROD_PASSKEY}

# Security
SECRET_KEY=${JWT_SECRET_KEY}
ENCRYPTION_KEY=${WALLET_ENCRYPTION_KEY}
WEBHOOK_SECRET=${WEBHOOK_SIGNATURE_SECRET}

# Monitoring
SENTRY_DSN=${SENTRY_PROD_DSN}
LOG_LEVEL=INFO
```

**Database Migration Strategy:**
```bash
# Create migration
alembic revision --autogenerate -m "Initial crypto-fiat schema"

# Review migration file
vim migrations/versions/001_initial_schema.py

# Apply migration
alembic upgrade head

# Backup strategy
pg_dump cryptopay_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Nginx Production Configuration (docker/nginx/prod.conf):**
```nginx
server {
    listen 443 ssl http2;
    server_name api.cryptopay.ke;
    
    ssl_certificate /etc/ssl/cryptopay.crt;
    ssl_certificate_key /etc/ssl/cryptopay.key;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # API backend
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting
        limit_req zone=api burst=20 nodelay;
    }
}

server {
    listen 443 ssl http2;
    server_name app.cryptopay.ke;
    
    ssl_certificate /etc/ssl/cryptopay.crt;
    ssl_certificate_key /etc/ssl/cryptopay.key;
    
    # Customer portal
    location / {
        proxy_pass http://frontend-customer:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**CI/CD Pipeline (.github/workflows/deploy.yml):**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Backend Tests
        run: |
          cd backend
          uv run pytest app/tests/ -v
          uv run ruff check app/
          uv run mypy app/
      
      - name: Run Frontend Tests
        run: |
          cd frontend/customer-portal
          npm ci
          npm run test
          npm run lint
          npm run type-check
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          # Build and push Docker images
          docker build -t cryptopay/backend ./backend
          docker build -t cryptopay/frontend ./frontend/customer-portal
          
          # Deploy with zero downtime
          docker-compose -f docker-compose.prod.yml up -d --remove-orphans
          
          # Run health checks
          ./scripts/health-check.sh
```

**Monitoring Setup (docker/monitoring/docker-compose.monitoring.yml):**
```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3003:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
  
  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
  
  kibana:
    image: kibana:8.8.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

**Production Health Checks (scripts/health-check.sh):**
```bash
#!/bin/bash
set -e

echo "Running production health checks..."

# API health check
curl -f http://localhost:8000/health || exit 1

# Database connectivity
pg_isready -h localhost -p 5432 || exit 1

# Redis connectivity
redis-cli ping || exit 1

# Frontend accessibility
curl -f http://localhost:3000 || exit 1

# SSL certificate validity
openssl x509 -in /etc/ssl/cryptopay.crt -noout -checkend 86400 || exit 1

echo "All health checks passed!"
```
```

### Level 4: Mobile Responsiveness & Performance

```bash
# Test mobile responsiveness with Lighthouse
npx lighthouse http://localhost:3000 \
  --emulated-form-factor=mobile \
  --chrome-flags="--headless" \
  --output=html \
  --output-path=./lighthouse-mobile.html

# Test desktop performance
npx lighthouse http://localhost:3000 \
  --emulated-form-factor=desktop \
  --chrome-flags="--headless" \
  --output=html \
  --output-path=./lighthouse-desktop.html

# Security testing
npm install -g observatory-cli
observatory http://localhost:3000

# Load testing
npm install -g artillery
artillery quick --count 10 --num 50 http://localhost:8000/api/health

# Expected:
# - Mobile Lighthouse score > 90
# - Desktop Lighthouse score > 95
# - Security observatory grade A
# - Load test response time < 200ms
```

## Final Validation Checklist

- [ ] All backend tests pass: `uv run pytest app/tests/ -v`
- [ ] All frontend tests pass: `npm test` in each frontend directory
- [ ] No linting errors: `ruff check` and `npm run lint`
- [ ] No type errors: `mypy` and `npm run type-check`
- [ ] Mobile Lighthouse score > 90
- [ ] Desktop Lighthouse score > 95
- [ ] Security headers properly configured
- [ ] API documentation generated: `/docs` endpoint
- [ ] All environment variables configured
- [ ] Database migrations run successfully
- [ ] Payment processing flow works end-to-end
- [ ] M-Pesa integration tested with sandbox
- [ ] Blockchain transactions confirmed on testnet
- [ ] Rate limiting prevents abuse
- [ ] Error handling covers all edge cases
- [ ] Audit logging captures all financial events
- [ ] Responsive design works on mobile browsers
- [ ] PWA capabilities function correctly

---

## Anti-Patterns to Avoid

- ❌ Don't use float for monetary calculations - always use Decimal
- ❌ Don't skip transaction confirmations - wait for required blocks
- ❌ Don't ignore webhook signature verification
- ❌ Don't hardcode exchange rates - always fetch current rates
- ❌ Don't bypass validation in any endpoint
- ❌ Don't store private keys unencrypted
- ❌ Don't allow unlimited rate limits on financial endpoints
- ❌ Don't skip responsive design testing on mobile devices
- ❌ Don't deploy without comprehensive logging and monitoring
- ❌ Don't forget to implement proper error boundaries in React components

**Score: 9/10** - High confidence for one-pass implementation success with comprehensive context, proven patterns, and detailed validation loops.
