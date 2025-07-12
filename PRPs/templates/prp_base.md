# Product Requirements Prompt (PRP) Template

**Feature**: [Feature Name]  
**Type**: [Payment Processing | Blockchain Integration | Security | Compliance]  
**Priority**: [High | Medium | Low]  
**Estimated Complexity**: [Simple | Medium | Complex]  
**Confidence Score**: [1-10]/10

## 📋 Feature Overview

### Business Requirements
- **Primary Goal**: [What business problem does this solve?]
- **Success Criteria**: [How do we measure success?]
- **User Stories**: [Who benefits and how?]
- **Compliance Requirements**: [KYC/AML/CBK/CMA requirements]

### Technical Requirements
- **Core Functionality**: [What needs to be built?]
- **Integration Points**: [External services, APIs, blockchains]
- **Performance Requirements**: [Response times, throughput, scalability]
- **Security Requirements**: [Encryption, authentication, audit logging]

## 🏗️ Architecture Context

### Current System State
```
[Include relevant parts of current architecture]
backend/app/
├── [relevant directories]
└── [relevant files]
```

### Integration Points
- **Database Models**: [Which models are affected?]
- **API Endpoints**: [New or modified endpoints]
- **External Services**: [Blockchain, M-Pesa, third-party APIs]
- **Background Tasks**: [Async processing requirements]

### Dependencies
- **Internal Dependencies**: [Other Qpesapay services/modules]
- **External Dependencies**: [Third-party libraries, APIs]
- **Infrastructure Dependencies**: [Docker, Redis, PostgreSQL]

## 💰 Financial System Considerations

### Monetary Handling
- **Currency Types**: [BTC, USDT, KES, USD]
- **Decimal Precision**: [Required precision for each currency]
- **Calculation Requirements**: [Fee calculations, conversions, rounding]
- **Amount Validation**: [Min/max limits, positive values]

### Transaction Requirements
- **Idempotency**: [How to prevent duplicate processing]
- **Atomicity**: [Database transaction boundaries]
- **Rollback Scenarios**: [What happens on failure]
- **Audit Trail**: [What needs to be logged]

### Compliance Integration
- **KYC/AML Touchpoints**: [Where compliance checks occur]
- **Transaction Monitoring**: [Suspicious activity detection]
- **Regulatory Reporting**: [What data needs to be reported]
- **Data Retention**: [How long to keep records]

## 🔒 Security Requirements

### Authentication & Authorization
- **User Authentication**: [JWT, session management]
- **Role-Based Access**: [User, merchant, admin permissions]
- **API Security**: [Rate limiting, input validation]
- **Session Management**: [Token expiry, refresh mechanisms]

### Data Protection
- **Encryption Requirements**: [What data needs encryption]
- **Key Management**: [Private keys, encryption keys]
- **Secure Storage**: [Database encryption, field-level encryption]
- **Data Transmission**: [HTTPS, API security]

### Audit & Monitoring
- **Audit Logging**: [What events to log]
- **Security Monitoring**: [Suspicious activity detection]
- **Error Handling**: [Secure error messages]
- **Incident Response**: [Security breach procedures]

## 🧪 Testing Strategy

### Unit Testing Requirements
- **Test Coverage**: [Minimum coverage percentage]
- **Test Categories**: [Expected use, edge cases, failure scenarios]
- **Mock Requirements**: [External services to mock]
- **Decimal Precision Tests**: [Monetary calculation validation]

### Integration Testing Requirements
- **External Service Testing**: [Testnet only for blockchain]
- **Database Integration**: [Transaction testing]
- **API Integration**: [Endpoint testing]
- **Security Testing**: [Authentication, authorization, input validation]

### Security Testing Requirements
- **Penetration Testing**: [Security vulnerability assessment]
- **Input Validation Testing**: [SQL injection, XSS prevention]
- **Authentication Testing**: [JWT validation, session security]
- **Encryption Testing**: [Data protection validation]

## 📊 Implementation Plan

### Phase 1: Foundation
**Duration**: [X days]
**Deliverables**:
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Specific deliverable 3]

**Validation Gates**:
- [ ] Unit tests passing (>90% coverage)
- [ ] Security review completed
- [ ] Code review approved

### Phase 2: Core Implementation
**Duration**: [X days]
**Deliverables**:
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Specific deliverable 3]

**Validation Gates**:
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Security validation completed

### Phase 3: Integration & Validation
**Duration**: [X days]
**Deliverables**:
- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Specific deliverable 3]

**Validation Gates**:
- [ ] End-to-end testing completed
- [ ] Compliance requirements verified
- [ ] Documentation updated

## 🎯 Validation Checkpoints

### Functional Validation
- [ ] All business requirements implemented
- [ ] All user stories satisfied
- [ ] Performance requirements met
- [ ] Error handling implemented

### Security Validation
- [ ] All security requirements implemented
- [ ] Encryption properly implemented
- [ ] Authentication/authorization working
- [ ] Audit logging complete

### Compliance Validation
- [ ] KYC/AML requirements met
- [ ] Transaction monitoring implemented
- [ ] Regulatory reporting capable
- [ ] Data retention compliant

### Financial System Validation
- [ ] Decimal precision correct for all currencies
- [ ] Transaction idempotency implemented
- [ ] Proper rollback mechanisms
- [ ] Complete audit trail

## 📚 Reference Materials

### Code Examples
- **Payment Processing**: `examples/payment_processing/`
- **Security Patterns**: `examples/security/`
- **Domain Models**: `examples/domain/`
- **Testing Patterns**: `examples/tests/`

### Documentation
- **Architecture**: `summary.md`
- **Security Requirements**: `SECURITY.md`
- **API Documentation**: `backend/docs/api/`
- **Compliance Guidelines**: `backend/docs/compliance/`

### External Resources
- **M-Pesa Daraja API**: [Documentation links]
- **Blockchain APIs**: [Bitcoin, Ethereum, Tron documentation]
- **Security Standards**: [PCI DSS, OWASP guidelines]
- **Compliance Resources**: [CBK, CMA regulations]

## 🚨 Risk Assessment

### Technical Risks
- **Risk 1**: [Description and mitigation strategy]
- **Risk 2**: [Description and mitigation strategy]
- **Risk 3**: [Description and mitigation strategy]

### Security Risks
- **Risk 1**: [Description and mitigation strategy]
- **Risk 2**: [Description and mitigation strategy]
- **Risk 3**: [Description and mitigation strategy]

### Compliance Risks
- **Risk 1**: [Description and mitigation strategy]
- **Risk 2**: [Description and mitigation strategy]
- **Risk 3**: [Description and mitigation strategy]

## ✅ Success Criteria

### Functional Success
- [ ] All features working as specified
- [ ] All user stories completed
- [ ] Performance targets achieved
- [ ] Error handling robust

### Security Success
- [ ] Security review passed
- [ ] Penetration testing passed
- [ ] Audit logging complete
- [ ] Encryption properly implemented

### Compliance Success
- [ ] Regulatory requirements met
- [ ] Audit trail complete
- [ ] Reporting capabilities functional
- [ ] Data retention compliant

### Quality Success
- [ ] Code review approved
- [ ] Test coverage >90%
- [ ] Documentation complete
- [ ] Deployment successful

---

**Implementation Notes**:
- This is a financial system handling real money
- Security and compliance are non-negotiable
- All monetary calculations must use Decimal precision
- Testnet only for blockchain testing
- Complete audit trail required for all operations
