# Execute PRP Implementation

Execute a comprehensive Product Requirements Prompt (PRP) for Qpesapay features with financial system validation.

## Command Usage
```
/execute-prp <prp-file>
```

## Process

You are an expert financial systems developer implementing features for Qpesapay, a crypto-fiat payment processor for the Kenyan market. Execute the PRP with extreme attention to financial system requirements.

### Step 1: Load Complete Context
Read and internalize the PRP file: `$ARGUMENTS`

Load all referenced context:
- CLAUDE.md for project rules and constraints
- Relevant examples from examples/ directory
- Current codebase patterns and architecture
- Security and compliance requirements

### Step 2: Create Detailed Implementation Plan
Using task management tools, create a comprehensive task breakdown:
- Break down into meaningful development units (~20 minutes each)
- Include validation checkpoints
- Add security verification steps
- Include compliance validation gates
- Add testing requirements

### Step 3: Systematic Implementation
For each implementation step:

#### Code Implementation
- Follow Sandi Metz principles from CLAUDE.md
- Use existing patterns from examples/
- Implement proper error handling
- Add comprehensive logging
- Include security validations

#### Financial System Validations
- Verify Decimal usage for all monetary calculations
- Implement transaction idempotency
- Add proper audit logging
- Validate input sanitization
- Check rate limiting implementation

#### Security Checkpoints
- Validate private key handling
- Verify transaction signing
- Check authentication/authorization
- Validate HTTPS enforcement
- Review error message sanitization

#### Compliance Verification
- Verify KYC/AML integration points
- Check transaction monitoring
- Validate audit trail creation
- Review data retention compliance
- Confirm regulatory reporting capability

### Step 4: Testing Implementation
For each component implemented:

#### Unit Testing
- Create comprehensive unit tests
- Test expected functionality
- Test edge cases
- Test failure scenarios
- Validate error handling

#### Integration Testing
- Test with external services (testnet only)
- Validate API integrations
- Test webhook handling
- Verify database transactions
- Test security middleware

#### Security Testing
- Validate input sanitization
- Test authentication/authorization
- Verify rate limiting
- Test encryption/decryption
- Validate audit logging

### Step 5: Validation Gates
Before marking any component complete:

#### Functional Validation
- All requirements implemented
- All tests passing
- Error handling working
- Logging implemented
- Documentation updated

#### Security Validation
- Security requirements met
- No hardcoded secrets
- Proper encryption used
- Rate limiting active
- Audit trails complete

#### Compliance Validation
- KYC/AML requirements met
- Transaction monitoring active
- Regulatory reporting capable
- Data retention compliant
- Audit trails immutable

#### Performance Validation
- Response time targets met
- Resource usage acceptable
- Scalability considerations addressed
- Error rates within limits
- Monitoring implemented

### Step 6: Documentation and Cleanup
- Update relevant documentation
- Add code comments for complex logic
- Update API documentation if applicable
- Create deployment notes
- Update security documentation

### Step 7: Final Validation and Summary
- Run complete test suite
- Verify all validation gates passed
- Confirm compliance requirements met
- Validate security implementations
- Provide implementation summary

## Financial System Specific Requirements

### Mandatory Implementations
- **Decimal Precision**: All monetary calculations use Decimal type
- **Idempotency**: All financial operations are idempotent
- **Audit Logging**: Complete audit trail for all operations
- **Error Handling**: Graceful handling with proper rollback
- **Security**: Encryption, authentication, authorization

### Validation Requirements
- **Testnet Only**: Never use mainnet during development
- **Security Audit**: Each component security reviewed
- **Compliance Check**: Regulatory requirements verified
- **Performance Test**: Response times and resource usage validated
- **Integration Test**: External service integrations tested

### Success Criteria
- All functional requirements implemented
- All security requirements satisfied
- All compliance requirements met
- All tests passing (unit, integration, security)
- Performance targets achieved
- Documentation complete

Execute this process systematically, never compromising on financial system security or compliance requirements.
