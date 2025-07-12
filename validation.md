# Validation Loop Structure - Crypto-Fiat Payment Processor

## Overview

This document outlines the step-by-step validation loops for all 10 tasks in the web-first crypto-fiat payment processor development. Each task follows a consistent **Build → Test → Validate → Feedback** cycle.

## Core Validation Principles

1. **Progressive Validation**: Each task must pass all levels before proceeding
2. **Early Failure Detection**: Catch issues immediately, not at the end
3. **User Feedback Integration**: Regular checkpoints for user approval
4. **Incremental Confidence**: Build trust through proven components

---

## Task 1: Backend Foundation

### Build Phase
```yaml
Components:
- FastAPI app with middleware setup
- CORS configuration
- Rate limiting implementation
- Request logging middleware
- Basic project structure
```

### Validation Loops

#### Level 1: Syntax & Style (Immediate)
```bash
cd backend
uv run ruff check app/ --fix
uv run mypy app/
uv run black app/ --check

# Expected: No syntax errors, type checking passes
# If errors: Fix immediately before proceeding
```

#### Level 2: Unit Tests (Component)
```bash
uv run pytest app/tests/test_main.py -v

# Test cases:
# - FastAPI app initialization
# - Middleware configuration
# - CORS headers present
# - Rate limiting functional
```

#### Level 3: Integration Tests (System)
```bash
# Start the FastAPI server
uv run uvicorn app.main:app --reload &

# Test basic endpoints
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/docs

# Expected: 200 responses, API docs accessible
```

#### Level 4: User Acceptance (Feedback)
```
✅ User validates:
- API documentation loads at /docs
- Health endpoint responds correctly
- CORS allows frontend connections
- Rate limiting prevents abuse

User decision: "Proceed to authentication" or "Adjust configuration"
```

---

## Task 2: Authentication System

### Build Phase
```yaml
Components:
- JWT token generation and validation
- User registration/login endpoints
- Password hashing with bcrypt
- 2FA support structure
- Security middleware
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
uv run ruff check app/core/security.py app/api/auth.py --fix
uv run mypy app/core/security.py app/api/auth.py

# Expected: No security-related lint warnings
```

#### Level 2: Unit Tests
```bash
uv run pytest app/tests/test_auth.py -v

# Test cases:
def test_user_registration():
    """Test successful user registration"""
    
def test_login_with_valid_credentials():
    """Test successful login returns JWT token"""
    
def test_login_with_invalid_credentials():
    """Test failed login returns 401"""
    
def test_jwt_token_validation():
    """Test JWT token validation works"""
    
def test_password_hashing():
    """Test password hashing is secure"""
```

#### Level 3: Integration Tests
```bash
# Test user registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "phone_number": "+254700000000",
    "account_type": "personal"
  }'

# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Expected: JWT tokens returned, user created in database
```

#### Level 4: User Acceptance
```
✅ User validates:
- Registration flow works smoothly
- Login returns valid JWT tokens
- Protected endpoints require authentication
- Password requirements are enforced

User decision: "Proceed to payment processing" or "Enhance security"
```

---

## Task 3: Payment Processing

### Build Phase
```yaml
Components:
- USDT payment processing service
- Blockchain transaction handling
- Gas fee estimation
- Transaction monitoring
- Error handling and rollbacks
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
uv run ruff check app/services/payment_service.py app/api/payments.py --fix
uv run mypy app/services/payment_service.py app/api/payments.py

# Expected: Financial calculations use Decimal, not float
```

#### Level 2: Unit Tests
```bash
uv run pytest app/tests/test_payments.py -v

# Test cases:
def test_payment_processing_happy_path():
    """Test successful USDT payment"""
    
def test_payment_validation_negative_amount():
    """Test payment fails with negative amount"""
    
def test_payment_gas_estimation():
    """Test accurate gas fee estimation"""
    
def test_payment_transaction_rollback():
    """Test rollback on blockchain failure"""
    
def test_duplicate_transaction_handling():
    """Test idempotency with duplicate requests"""
```

#### Level 3: Integration Tests
```bash
# Test payment creation (testnet)
curl -X POST http://localhost:8000/api/payments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "amount_usdt": "10.000000",
    "recipient_address": "0x742d35Cc6634C0532925a3b8D37c4E6C5e-TEST",
    "network": "ethereum"
  }'

# Test payment status checking
curl -X GET http://localhost:8000/api/payments/{transaction_id} \
  -H "Authorization: Bearer $JWT_TOKEN"

# Expected: Transaction created, blockchain hash returned
```

#### Level 4: User Acceptance
```
✅ User validates:
- Payment processing works on testnet
- Gas fees are accurately calculated
- Transaction status updates correctly
- Error messages are clear and helpful

User decision: "Proceed to M-Pesa integration" or "Refine payment flow"
```

---

## Task 4: M-Pesa Integration

### Build Phase
```yaml
Components:
- M-Pesa Daraja API integration
- B2C payment processing
- Webhook signature verification
- Settlement automation
- Error handling for M-Pesa responses
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
uv run ruff check app/services/mpesa_service.py app/api/webhooks.py --fix
uv run mypy app/services/mpesa_service.py app/api/webhooks.py

# Expected: Proper async/await patterns for API calls
```

#### Level 2: Unit Tests
```bash
uv run pytest app/tests/test_mpesa.py -v

# Test cases:
def test_mpesa_b2c_payment_request():
    """Test B2C payment request formatting"""
    
def test_webhook_signature_verification():
    """Test webhook signature validation"""
    
def test_phone_number_validation():
    """Test Kenya phone number formats"""
    
def test_mpesa_error_handling():
    """Test proper error handling for API failures"""
    
def test_settlement_calculation():
    """Test merchant settlement calculations"""
```

#### Level 3: Integration Tests
```bash
# Test M-Pesa B2C payment (sandbox)
curl -X POST http://localhost:8000/api/mpesa/b2c \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "phone_number": "+254700000000",
    "amount": "1000.00",
    "occasion": "Settlement payment"
  }'

# Test webhook endpoint
curl -X POST http://localhost:8000/api/webhooks/mpesa \
  -H "Content-Type: application/json" \
  -d '{"test": "webhook_payload"}'

# Expected: M-Pesa sandbox responds, webhooks process correctly
```

#### Level 4: User Acceptance
```
✅ User validates:
- M-Pesa sandbox integration works
- Phone number validation accepts Kenya formats
- Webhook processing is secure and reliable
- Settlement calculations are accurate

User decision: "Proceed to customer portal" or "Enhance M-Pesa features"
```

---

## Task 5: Customer Web Portal (Next.js)

### Build Phase
```yaml
Components:
- Mobile-first responsive dashboard
- USDT wallet interface
- Payment creation forms
- Transaction history
- Progressive Web App features
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
cd frontend/customer-portal
npm run lint
npm run type-check
npm run build

# Expected: No TypeScript errors, build succeeds
```

#### Level 2: Unit Tests
```bash
npm test

# Test cases:
test('wallet balance displays correctly', () => {})
test('payment form validation works', () => {})
test('transaction history loads', () => {})
test('mobile responsive layout', () => {})
test('PWA manifest is valid', () => {})
```

#### Level 3: Integration Tests
```bash
# Start development server
npm run dev

# Test pages load
curl -I http://localhost:3000
curl -I http://localhost:3000/dashboard
curl -I http://localhost:3000/wallet

# Test mobile responsiveness
npx lighthouse http://localhost:3000 \
  --emulated-form-factor=mobile \
  --chrome-flags="--headless"

# Expected: All pages load, mobile Lighthouse score > 90
```

#### Level 4: User Acceptance
```
✅ User validates:
- Dashboard loads quickly on mobile browser
- Touch interactions work smoothly
- Forms are easy to use on small screens
- Visual design matches requirements
- PWA can be added to home screen

User decision: "Proceed to merchant dashboard" or "Refine user experience"
```

---

## Task 6: Merchant Dashboard

### Build Phase
```yaml
Components:
- Business analytics interface
- Payment management system
- Settlement tracking
- QR code generation
- Export functionality
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
cd frontend/merchant-dashboard
npm run lint
npm run type-check
npm run build

# Expected: Professional business interface code quality
```

#### Level 2: Unit Tests
```bash
npm test

# Test cases:
test('analytics charts render correctly', () => {})
test('payment QR codes generate', () => {})
test('settlement tracking works', () => {})
test('export functionality works', () => {})
test('responsive design for tablets', () => {})
```

#### Level 3: Integration Tests
```bash
# Test merchant dashboard
curl -I http://localhost:3001
curl -I http://localhost:3001/analytics
curl -I http://localhost:3001/settlements

# Test API integration
curl -X GET http://localhost:8000/api/merchants/analytics \
  -H "Authorization: Bearer $MERCHANT_JWT_TOKEN"

# Expected: Dashboard loads, API data displays correctly
```

#### Level 4: User Acceptance
```
✅ User validates:
- Analytics provide meaningful business insights
- Payment management is intuitive
- Settlement tracking is accurate
- QR code generation works reliably
- Interface works well on tablets and desktops

User decision: "Proceed to admin panel" or "Add more merchant features"
```

---

## Task 7: Admin Panel (React)

### Build Phase
```yaml
Components:
- System monitoring dashboard
- User management interface
- Transaction oversight
- Compliance tools
- Real-time alerts
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
cd frontend/admin-panel
npm run lint
npm run type-check
npm run build

# Expected: Enterprise-grade code quality
```

#### Level 2: Unit Tests
```bash
npm test

# Test cases:
test('system monitoring displays metrics', () => {})
test('user management CRUD works', () => {})
test('transaction filtering works', () => {})
test('compliance alerts trigger', () => {})
test('role-based access control', () => {})
```

#### Level 3: Integration Tests
```bash
# Test admin panel
curl -I http://localhost:3002
curl -I http://localhost:3002/monitoring
curl -I http://localhost:3002/users

# Test admin API access
curl -X GET http://localhost:8000/api/admin/system-health \
  -H "Authorization: Bearer $ADMIN_JWT_TOKEN"

# Expected: Admin panel secure, monitoring data accurate
```

#### Level 4: User Acceptance
```
✅ User validates:
- System monitoring provides real-time insights
- User management controls are comprehensive
- Transaction oversight tools are effective
- Compliance features meet regulatory needs
- Security controls are properly implemented

User decision: "Proceed to database setup" or "Enhance admin features"
```

---

## Task 8: Database Schema

### Build Phase
```yaml
Components:
- Complete PostgreSQL schema
- Alembic migrations
- Indexes for performance
- Constraints for data integrity
- Audit trail tables
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
cd backend
uv run alembic check
uv run alembic history

# Expected: Migration files are valid
```

#### Level 2: Unit Tests
```bash
uv run pytest app/tests/test_models.py -v

# Test cases:
def test_user_model_creation():
    """Test user model with all fields"""
    
def test_wallet_model_relationships():
    """Test wallet foreign key relationships"""
    
def test_transaction_model_constraints():
    """Test transaction amount constraints"""
    
def test_database_indexes():
    """Test performance indexes exist"""
```

#### Level 3: Integration Tests
```bash
# Run database migrations
uv run alembic upgrade head

# Test database operations
python -c "
from app.database import get_session
from app.models import User, Wallet, Transaction
# Test CRUD operations
"

# Check database constraints
psql -d crypto_fiat_db -c "SELECT * FROM users LIMIT 1;"

# Expected: All migrations apply, constraints work
```

#### Level 4: User Acceptance
```
✅ User validates:
- Database schema supports all features
- Migrations run without errors
- Performance is acceptable with test data
- Data integrity constraints work properly
- Audit trail captures all required events

User decision: "Proceed to testing suite" or "Optimize database design"
```

---

## Task 9: Testing Suite

### Build Phase
```yaml
Components:
- Comprehensive unit tests
- Integration test scenarios
- Security test cases
- Performance benchmarks
- End-to-end user journeys
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
cd backend
uv run ruff check app/tests/ --fix
uv run mypy app/tests/

cd frontend/customer-portal
npm run lint:test

# Expected: Test code follows quality standards
```

#### Level 2: Unit Tests (Meta-testing)
```bash
# Run all backend tests
uv run pytest app/tests/ -v --cov=app --cov-report=html

# Run all frontend tests
cd frontend/customer-portal && npm test -- --coverage
cd frontend/merchant-dashboard && npm test -- --coverage
cd frontend/admin-panel && npm test -- --coverage

# Expected: >90% code coverage across all components
```

#### Level 3: Integration Tests (Full System)
```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Wait for services
sleep 30

# Run end-to-end tests
uv run pytest app/tests/test_e2e.py -v

# Test complete user journeys
# 1. User registration → KYC → First payment
# 2. Merchant onboarding → First settlement
# 3. Admin user management → Compliance check

# Expected: All user journeys complete successfully
```

#### Level 4: User Acceptance
```
✅ User validates:
- All critical user journeys work end-to-end
- Error scenarios are handled gracefully
- Performance meets requirements
- Security tests pass
- System behaves correctly under load

User decision: "Proceed to deployment" or "Add more test coverage"
```

---

## Task 10: DevOps Setup

### Build Phase
```yaml
Components:
- Docker containerization
- Production configuration
- CI/CD pipeline setup
- Monitoring and logging
- Backup procedures
```

### Validation Loops

#### Level 1: Syntax & Style
```bash
# Validate Docker configurations
docker-compose -f docker/docker-compose.yml config
docker-compose -f docker/docker-compose.prod.yml config

# Validate deployment scripts
shellcheck scripts/deploy.sh
shellcheck scripts/backup.sh

# Expected: All configuration files are valid
```

#### Level 2: Unit Tests (Infrastructure)
```bash
# Test Docker builds
docker build -t crypto-fiat-backend backend/
docker build -t crypto-fiat-frontend-customer frontend/customer-portal/
docker build -t crypto-fiat-frontend-merchant frontend/merchant-dashboard/

# Test environment configurations
docker run --rm crypto-fiat-backend python -c "import app.config; print('Config OK')"

# Expected: All Docker images build successfully
```

#### Level 3: Integration Tests (Deployment)
```bash
# Test production-like deployment
docker-compose -f docker/docker-compose.prod.yml up -d

# Test all services are healthy
curl -f http://localhost/api/health
curl -f http://localhost/customer/
curl -f http://localhost/merchant/
curl -f http://localhost/admin/

# Test backup procedures
./scripts/backup.sh

# Expected: Production deployment works, backups successful
```

#### Level 4: User Acceptance (Go-Live)
```
✅ User validates:
- Production deployment is stable
- All services are accessible
- Monitoring and logging work
- Backup and recovery procedures tested
- Security configurations are production-ready
- Performance meets production requirements

User decision: "Deploy to production" or "Additional hardening needed"
```

---

## Overall Validation Summary

### Pre-Production Checklist

```bash
# Final comprehensive validation
./scripts/run-all-tests.sh

# Performance validation
npx lighthouse http://localhost:3000 --chrome-flags="--headless"
artillery quick --count 10 --num 100 http://localhost:8000/api/health

# Security validation
npm audit
safety check requirements.txt
bandit -r backend/app/

# Compliance validation
# - All financial transactions logged
# - KYC/AML workflows functional
# - Data encryption verified
# - Audit trails complete
```

### Success Criteria

- [ ] All 40 validation loops pass
- [ ] Mobile Lighthouse score > 90
- [ ] Backend test coverage > 90%
- [ ] Frontend test coverage > 85%
- [ ] Security audit passes
- [ ] Performance benchmarks met
- [ ] User acceptance confirmed for all tasks

### Timeline Expectations

**With Validation Loops**: 6-8 hours total
- Each task: 30-45 minutes development + 15-30 minutes validation
- User feedback: 5-10 minutes per task
- Issue resolution: Built into each loop

**Benefit**: Zero surprises, high confidence, production-ready system

---

## Emergency Procedures

### If Validation Fails

1. **Stop immediately** - Don't proceed to next task
2. **Analyze the failure** - Use validation output to identify issue
3. **Fix the specific problem** - Don't rebuild everything
4. **Re-run validation** - Ensure fix works
5. **Get user confirmation** - Verify satisfaction before proceeding

### If Timeline Extends

1. **Identify bottleneck** - Which validation is taking longest?
2. **Simplify scope** - Can features be moved to v2?
3. **Parallel development** - Can frontend start while backend stabilizes?
4. **User prioritization** - Which features are most critical?

**Remember**: The validation loops are your safety net - trust the process! 🛡️
