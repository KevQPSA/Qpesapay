# Feature Request Template

Use this template to request new features for Qpesapay. The more detailed and specific you are, the better the AI can generate comprehensive PRPs and implementations.

## 🎯 FEATURE

**Feature Name**: [Descriptive name for the feature]

**Feature Type**: [Choose one: Payment Processing | Blockchain Integration | Security | Compliance | API | Frontend | Infrastructure]

**Priority**: [High | Medium | Low]

**Description**: 
[Provide a detailed description of what you want to build. Be specific about functionality, user interactions, and business requirements.]

**Business Justification**:
[Explain why this feature is needed. What business problem does it solve? What value does it provide?]

## 👥 USER STORIES

**Primary Users**: [Who will use this feature? Customers, merchants, admins?]

**User Story 1**: As a [user type], I want to [action] so that [benefit].

**User Story 2**: As a [user type], I want to [action] so that [benefit].

**User Story 3**: As a [user type], I want to [action] so that [benefit].

## 🔧 TECHNICAL REQUIREMENTS

**Core Functionality**:
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

**Integration Requirements**:
- [External services to integrate with]
- [APIs to consume or provide]
- [Database changes needed]

**Performance Requirements**:
- [Response time requirements]
- [Throughput requirements]
- [Scalability considerations]

## 💰 FINANCIAL CONSIDERATIONS

**Currency Handling**:
- [Which currencies are involved: BTC, USDT, KES, USD?]
- [What precision is required?]
- [Any currency conversion needed?]

**Transaction Requirements**:
- [Transaction types involved]
- [Fee calculations needed]
- [Settlement requirements]

**Compliance Requirements**:
- [KYC/AML requirements]
- [Regulatory reporting needs]
- [Audit trail requirements]

## 🔒 SECURITY REQUIREMENTS

**Authentication & Authorization**:
- [Who can access this feature?]
- [What permissions are required?]
- [Any special security considerations?]

**Data Protection**:
- [What sensitive data is involved?]
- [Encryption requirements]
- [Privacy considerations]

**Audit & Monitoring**:
- [What events need to be logged?]
- [Monitoring requirements]
- [Alert conditions]

## 📋 EXAMPLES

**Reference Implementations**:
[List any files in the examples/ directory that should be used as patterns]
- `examples/payment_processing/crypto_payment.py` - [How it relates to your feature]
- `examples/security/encryption_patterns.py` - [How it relates to your feature]
- `examples/domain/value_objects.py` - [How it relates to your feature]

**Similar Features**:
[Reference any existing features in Qpesapay that are similar]

**External References**:
[Any external systems, APIs, or standards to reference]

## 📚 DOCUMENTATION

**API Documentation**:
[Links to relevant API documentation]
- M-Pesa Daraja API: [Specific endpoints if relevant]
- Bitcoin RPC: [Specific methods if relevant]
- Ethereum JSON-RPC: [Specific methods if relevant]
- Tron API: [Specific endpoints if relevant]

**Standards & Compliance**:
[Relevant standards or compliance requirements]
- CBK regulations: [Specific requirements]
- KYC/AML standards: [Specific requirements]
- Security standards: [PCI DSS, OWASP, etc.]

**Technical Resources**:
[Any technical documentation, whitepapers, or resources]

## ⚠️ OTHER CONSIDERATIONS

**Known Challenges**:
[Any known technical challenges or complexities]

**Dependencies**:
[Features or systems this depends on]

**Constraints**:
[Any limitations or constraints to consider]

**Gotchas**:
[Common pitfalls or things AI assistants commonly miss]

**Testing Considerations**:
[Special testing requirements or considerations]

**Deployment Considerations**:
[Any special deployment or infrastructure requirements]

## 🎯 SUCCESS CRITERIA

**Functional Success**:
- [Specific measurable criteria for functional success]

**Performance Success**:
- [Specific performance benchmarks]

**Security Success**:
- [Security validation requirements]

**User Experience Success**:
- [User experience criteria]

---

## 📝 EXAMPLE FEATURE REQUEST

Here's an example of how to fill out this template:

### 🎯 FEATURE

**Feature Name**: Bitcoin Lightning Network Integration

**Feature Type**: Blockchain Integration

**Priority**: Medium

**Description**: 
Integrate Bitcoin Lightning Network to enable instant, low-fee Bitcoin payments for small transactions. This will allow customers to make micropayments and merchants to receive instant settlements for small purchases.

**Business Justification**:
Current Bitcoin transactions have high fees and slow confirmation times for small amounts. Lightning Network enables instant payments with minimal fees, making Bitcoin practical for everyday transactions and improving user experience.

### 👥 USER STORIES

**Primary Users**: Customers making small Bitcoin payments, merchants receiving micropayments

**User Story 1**: As a customer, I want to make instant Bitcoin payments under $10 so that I don't pay high transaction fees.

**User Story 2**: As a merchant, I want to receive instant Bitcoin payments so that I can provide immediate service without waiting for confirmations.

**User Story 3**: As a system administrator, I want to monitor Lightning Network channels so that I can ensure adequate liquidity.

### 🔧 TECHNICAL REQUIREMENTS

**Core Functionality**:
- Lightning Network node integration
- Payment channel management
- Invoice generation and payment
- Channel liquidity monitoring

**Integration Requirements**:
- LND (Lightning Network Daemon) integration
- Bitcoin Core node connection
- Existing wallet system integration
- Payment processing pipeline integration

**Performance Requirements**:
- Sub-second payment processing
- 99.9% uptime for Lightning node
- Support for 1000+ concurrent payments

### 💰 FINANCIAL CONSIDERATIONS

**Currency Handling**:
- Bitcoin (BTC) with 8 decimal precision
- Lightning Network satoshi precision
- Fee calculations for channel operations

**Transaction Requirements**:
- Instant payment confirmation
- Channel opening/closing fees
- Routing fee calculations

**Compliance Requirements**:
- Same KYC/AML as regular Bitcoin transactions
- Enhanced monitoring for Lightning payments
- Audit trail for channel operations

[Continue with other sections...]

---

**Instructions for AI**: 
When you receive a completed INITIAL.md, use the `/generate-payment-prp` or `/generate-blockchain-prp` command to create a comprehensive PRP, then use `/execute-prp` to implement the feature following all Qpesapay security and compliance requirements.
