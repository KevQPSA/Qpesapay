# Generate Payment Processing PRP

Generate a comprehensive Product Requirements Prompt (PRP) for payment processing features in Qpesapay.

## Command Usage
```
/generate-payment-prp <feature-file>
```

## Process

You are an expert financial systems architect specializing in crypto-fiat payment processors for the Kenyan market. Your task is to create a comprehensive PRP for payment processing features.

### Step 1: Read and Analyze Feature Request
Read the feature request file: `$ARGUMENTS`

### Step 2: Research Phase (Parallel Execution)
Execute these research tasks simultaneously:

1. **Codebase Analysis**
   - Analyze existing payment processing patterns in `backend/app/services/payment/`
   - Review domain models in `backend/app/domain/`
   - Examine current transaction handling in `backend/app/models/transaction.py`
   - Study security implementations in `backend/app/core/security.py`

2. **Financial Compliance Research**
   - Research CBK (Central Bank of Kenya) payment processor requirements
   - Review KYC/AML compliance for crypto-fiat transactions
   - Analyze M-Pesa integration compliance requirements
   - Study transaction monitoring and reporting obligations

3. **Blockchain Integration Research**
   - Research Bitcoin payment processing best practices
   - Study USDT (Ethereum/Tron) integration patterns
   - Analyze gas fee management strategies
   - Review transaction confirmation requirements

4. **Security Research**
   - Study private key management for payment processors
   - Research transaction signing security
   - Analyze rate limiting for financial APIs
   - Review audit logging requirements

### Step 3: Create Comprehensive PRP
Create a PRP file in `PRPs/payment-{feature-name}.md` with:

#### Context Section
- Complete project background from CLAUDE.md
- Relevant code examples from examples/payment_processing/
- Financial system constraints and requirements
- Kenyan market specific considerations

#### Implementation Plan
- Detailed step-by-step implementation
- Security validation checkpoints
- Compliance verification gates
- Testing requirements (unit, integration, security)

#### Validation Gates
- Testnet transaction validation
- Security audit checkpoints
- Compliance verification
- Performance benchmarks
- Error handling validation

#### Success Criteria
- Functional requirements met
- Security requirements satisfied
- Compliance requirements fulfilled
- Performance targets achieved
- All tests passing

### Step 4: Confidence Assessment
Rate implementation confidence (1-10) based on:
- Completeness of context
- Clarity of requirements
- Availability of examples
- Complexity of integration

### Step 5: Save and Summarize
Save the PRP and provide a summary of:
- Key implementation challenges
- Required integrations
- Security considerations
- Compliance requirements
- Next steps for execution

## Financial System Specific Considerations

### Mandatory Validations
- All monetary calculations use Decimal type
- Transaction idempotency verification
- Proper error handling and rollback
- Audit trail creation
- Rate limiting implementation

### Security Requirements
- Private key encryption validation
- Transaction signing verification
- Input sanitization checks
- Authentication/authorization validation
- HTTPS enforcement

### Compliance Checks
- KYC/AML requirement verification
- Transaction monitoring implementation
- Regulatory reporting capability
- Audit trail completeness
- Data retention compliance

Execute this process systematically, ensuring all financial system requirements are addressed.
