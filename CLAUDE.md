# Qpesapay Development Guidelines

**Project**: Qpesapay - Web-first crypto-fiat payment processor for Kenya market  
**Domain**: Financial payment processing with blockchain integration  
**Market**: Kenya (M-Pesa, KES, CBK/CMA compliance)  
**Architecture**: Domain-Driven Design with Sandi Metz principles

## 🏗️ Project Architecture

### Core Technology Stack
- **Backend**: FastAPI (Python 3.11+), PostgreSQL, Redis
- **Authentication**: JWT with bcrypt, role-based access control
- **Payments**: M-Pesa Daraja API, Bitcoin, USDT (Ethereum/Tron)
- **Infrastructure**: Docker, Nginx, GitHub Actions
- **Testing**: Pytest with async support, comprehensive coverage

### Domain Architecture
```
backend/app/
├── domain/                    # Domain layer (DDD)
│   ├── value_objects.py      # Money, Address, PhoneNumber, etc.
│   └── entities.py           # PaymentRequest, TransactionRecord
├── services/payment/          # Business logic services
│   ├── validator.py          # Payment validation
│   ├── fee_estimator.py      # Fee calculation
│   ├── transaction_creator.py # Transaction creation
│   └── orchestrator.py       # Payment orchestration
├── commands/                  # Command pattern implementation
├── queries/                   # Query pattern implementation
├── models/                    # SQLAlchemy database models
├── schemas/                   # Pydantic request/response models
├── api/v1/endpoints/         # FastAPI routers
└── core/                     # Security, middleware, exceptions
```

## 🎯 Development Philosophy

### Sandi Metz Principles (SACRED)
1. **Small Objects**: Classes under 100 lines, methods under 5 lines
2. **Single Responsibility**: Each class has one reason to change
3. **Dependency Injection**: Explicit dependencies, easy testing
4. **Tell Don't Ask**: Objects should tell other objects what to do
5. **Law of Demeter**: Only talk to immediate neighbors

### Martin Fowler Patterns
- **Transaction Script**: For simple financial operations
- **Domain Model**: For complex business rules
- **Gateway Pattern**: For external integrations (M-Pesa, blockchain)
- **Repository Pattern**: For data access abstraction

### Clean Architecture Principles
- **Dependency Inversion**: Core business logic independent of frameworks
- **Clear Boundaries**: Separate concerns between layers
- **Testable Design**: Easy to unit test business logic

## 🔄 Project Awareness & Context

### Before Starting Any Task
1. **Read current task list** - Check what's in progress
2. **Review examples/** - Understand existing patterns
3. **Check INITIAL.md** - Understand feature requirements
4. **Use Docker** - All development through Docker containers
5. **Research thoroughly** - 30-100 pages for complex features

### Context Engineering Workflow
1. **Feature Request** → Create/update INITIAL.md
2. **Generate PRP** → `/generate-payment-prp` or `/generate-blockchain-prp`
3. **Execute PRP** → `/execute-prp PRPs/feature-name.md`
4. **Validate** → Security, compliance, performance checks
5. **Document** → Update examples/ and documentation

## 🧱 Code Structure & Quality

### File Organization
- **Maximum 500 lines per file** - Refactor if approaching limit
- **Clear module separation** - Group by feature/responsibility
- **Consistent imports** - Prefer relative imports within packages
- **Environment variables** - Use python_dotenv and load_env()

### Code Style
- **Python 3.11+** with type hints everywhere
- **PEP8 compliance** - Format with Black
- **Pydantic validation** - All input/output validation
- **Google-style docstrings** - Every function documented
- **Meaningful comments** - Explain why, not what

### Example Docstring Format
```python
def process_payment(amount: Decimal, currency: str) -> PaymentResult:
    """
    Process a crypto-fiat payment with full validation.

    Args:
        amount: Payment amount (must be positive)
        currency: Currency code (BTC, USDT, KES)

    Returns:
        PaymentResult: Contains transaction ID and status

    Raises:
        ValidationError: If amount or currency invalid
        PaymentError: If processing fails
    """
```

## 🏦 Financial System Requirements

### Security & Compliance (MANDATORY)
- **NO hardcoded secrets** - Environment variables only
- **Encryption everywhere** - AES-256 for sensitive data
- **Multi-signature wallets** - For business accounts
- **Immutable audit logs** - Every financial transaction logged
- **PCI DSS compliance** - Payment data handling standards
- **KYC/AML from day one** - Never skip compliance
- **Aggressive rate limiting** - Prevent abuse and attacks
- **Input validation/sanitization** - All financial data validated

### Financial Data Handling (CRITICAL)
- **Decimal type ONLY** - NEVER use float for money calculations
- **Banker's rounding** - Proper financial rounding
- **Currency precision** - USDT: 6 decimals, KES: 2 decimals
- **Transaction idempotency** - Unique transaction IDs
- **Database transactions** - Multi-step operations in transactions
- **Rollback mechanisms** - Failed transaction recovery
- **Amount validation** - Positive values, acceptable ranges

### Kenyan Market Specifics
- **M-Pesa Daraja API** - Follow patterns exactly
- **CBK compliance** - Central Bank of Kenya regulations
- **EAT timezone** - East Africa Time handling
- **Phone format** - Kenyan numbers (+254 format)
- **KES currency** - No cents in practice
- **Pesapal/Pesalink** - Proper webhook handling

### Blockchain/Crypto Requirements
- **Gas fee estimation** - Always estimate and handle properly
- **Transaction confirmations** - Wait for proper confirmations
- **Multi-network support** - Ethereum and Tron for USDT
- **HD wallets** - Hierarchical deterministic wallets
- **Blockchain reorg handling** - Handle reorganizations gracefully
- **Transaction monitoring** - Real-time blockchain monitoring

## 🧪 Testing Strategy

### Test Requirements
- **Pytest unit tests** - Every new feature tested
- **Test structure mirrors app** - tests/ folder organization
- **Minimum test coverage**:
  - 1 expected use case
  - 1 edge case
  - 1 failure scenario
- **Testnet only** - NEVER use mainnet in tests
- **Mock external APIs** - Unit tests with mocks
- **Integration tests** - Real API testing
- **Security testing** - Validate all security measures

### Financial Testing Specifics
- **Decimal precision tests** - Verify monetary calculations
- **Idempotency tests** - Duplicate transaction handling
- **Rollback tests** - Failed transaction recovery
- **Rate limiting tests** - API abuse prevention
- **Compliance tests** - KYC/AML workflow validation

## 🔒 Security Implementation

### Authentication & Authorization
- **JWT with refresh tokens** - Secure session management
- **Role-based access** - User, merchant, admin roles
- **Rate limiting** - Login attempt protection
- **Session management** - Proper session handling
- **Password policies** - Strong password requirements

### Data Protection
- **Field-level encryption** - Sensitive data encrypted
- **HTTPS everywhere** - No unencrypted communication
- **Input sanitization** - Prevent injection attacks
- **Error message sanitization** - No information leakage
- **Audit trail integrity** - Tamper-proof logging

### Wallet Security
- **Private key encryption** - AES-256 encryption
- **Key derivation** - PBKDF2 with high iterations
- **Secure key storage** - Never expose to frontend
- **Transaction signing** - Secure signing process
- **Balance protection** - Prevent unauthorized access

## 📊 Monitoring & Alerting

### Real-time Monitoring
- **Transaction monitoring** - All financial operations
- **Suspicious activity alerts** - Unusual patterns
- **Exchange rate monitoring** - Significant fluctuations
- **Settlement time tracking** - Delay alerts
- **Wallet balance monitoring** - Low fund alerts
- **System health** - Database, API, service health

### Performance Requirements
- **API response times** - < 200ms for most endpoints
- **Transaction processing** - < 30 seconds end-to-end
- **Database queries** - Optimized with proper indexing
- **Caching strategy** - Redis for frequently accessed data
- **Load testing** - Handle realistic transaction volumes

## 🚀 Development Workflow

### Task Management
- **Use task management tools** - For complex features
- **Break down work** - ~20 minute development units
- **Update task status** - Mark progress systematically
- **Validation checkpoints** - Security, compliance, performance

### Code Quality Gates
- **All tests passing** - Unit, integration, security
- **Security review** - Every financial component
- **Compliance check** - Regulatory requirements
- **Performance validation** - Response times, resource usage
- **Documentation updated** - Code, API, deployment docs

### AI Behavior Rules
- **Never assume context** - Ask questions if uncertain
- **No hallucinated libraries** - Use verified packages only
- **Confirm file paths** - Verify before referencing
- **Never delete code** - Unless explicitly instructed
- **Follow examples/** - Use existing patterns
- **Validate everything** - Security, compliance, performance

## 📚 Key Resources

### Documentation References
- **Phase 1 MVP Core Features.txt** - Feature specifications
- **summary.md** - Codebase analysis and architecture
- **examples/** - Code patterns and implementations
- **PRPs/** - Product Requirements Prompts
- **backend/SANDI_METZ_REFACTORING_SUMMARY.md** - Refactoring guide

### External APIs
- **M-Pesa Daraja API** - Mobile money integration
- **Bitcoin Core RPC** - Bitcoin blockchain interaction
- **Ethereum JSON-RPC** - Ethereum blockchain (USDT)
- **Tron API** - Tron blockchain (USDT)
- **Exchange Rate APIs** - Currency conversion rates

### Context Engineering Commands
- `/generate-payment-prp <feature-file>` - Generate payment processing PRP
- `/generate-blockchain-prp <feature-file>` - Generate blockchain integration PRP
- `/generate-webmcp-prp <feature-file>` - Generate WebMCP-enhanced PRP with browser integration
- `/execute-prp <prp-file>` - Execute comprehensive PRP implementation
- `/execute-webmcp-prp <prp-file>` - Execute WebMCP-enhanced PRP with real-time browser tools

## 🌐 WebMCP Integration

### Browser-Based Development
Qpesapay integrates WebMCP (Web Model Context Protocol) for real-time browser-based financial system interaction. This enables AI assistants to work directly with live financial data through standardized browser tools.

### WebMCP Architecture
- **Browser-based MCP Server**: Runs directly in the web application
- **Real-time Financial Tools**: Live payment validation, compliance checking, blockchain monitoring
- **Secure Authentication**: Uses existing browser sessions and authentication
- **Cross-tab Coordination**: Synchronized state across multiple browser tabs

### WebMCP Tools Available
- **Payment Validation**: Real-time crypto-fiat payment validation
- **Compliance Checking**: Live KYC/AML status verification
- **Fee Calculation**: Dynamic transaction fee estimation
- **Risk Assessment**: Real-time transaction risk scoring
- **Blockchain Monitoring**: Live transaction status updates
- **M-Pesa Integration**: Real-time settlement status checking
- **System Health**: Live system status monitoring

### Security Model
- **Browser Sandbox**: All operations within browser security model
- **Session Authentication**: Uses existing authenticated sessions
- **Same-Origin Policy**: Respects browser security boundaries
- **Rate Limiting**: Prevents abuse of financial tools
- **Audit Logging**: Complete audit trail for browser operations

### Development Workflow with WebMCP
1. **Feature Request** → Create/update INITIAL.md
2. **Generate WebMCP PRP** → `/generate-webmcp-prp INITIAL.md`
3. **Execute WebMCP PRP** → `/execute-webmcp-prp PRPs/webmcp-feature-name.md`
4. **Real-time Testing** → Use browser-based MCP tools for live validation
5. **Deploy** → Frontend with integrated MCP server

### WebMCP Examples
- **MCP Server Setup**: `examples/webmcp/qpesapay_mcp_server.ts`
- **React Integration**: `examples/webmcp/PaymentValidationComponent.tsx`
- **Next.js Integration**: `examples/webmcp/nextjs_integration.tsx`
- **Package Configuration**: `examples/webmcp/package.json.template`

---

**Remember**: This is a financial system handling real money. Every decision must prioritize security, compliance, and reliability over convenience or speed of development.
