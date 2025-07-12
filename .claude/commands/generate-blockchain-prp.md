# Generate Blockchain Integration PRP

Generate a comprehensive Product Requirements Prompt (PRP) for blockchain integration features in Qpesapay.

## Command Usage
```
/generate-blockchain-prp <feature-file>
```

## Process

You are an expert blockchain integration architect specializing in Bitcoin and USDT (Ethereum/Tron) for payment processors. Your task is to create a comprehensive PRP for blockchain integration features.

### Step 1: Read and Analyze Feature Request
Read the feature request file: `$ARGUMENTS`

### Step 2: Multi-Agent Research Phase
Execute these research tasks in parallel:

1. **Bitcoin Integration Research**
   - Bitcoin Core RPC API documentation
   - HD wallet implementation patterns
   - Transaction fee estimation strategies
   - Confirmation monitoring best practices
   - Testnet vs mainnet considerations

2. **USDT Ethereum Research**
   - ERC-20 USDT contract interactions
   - Web3.py integration patterns
   - Gas fee management strategies
   - Infura/Alchemy node provider setup
   - Transaction monitoring and confirmations

3. **USDT Tron Research**
   - TRC-20 USDT contract interactions
   - Tronpy library integration
   - TRX energy and bandwidth management
   - Tron API integration patterns
   - Transaction confirmation handling

4. **Security Research**
   - Private key derivation and storage
   - Transaction signing security
   - Multi-signature wallet implementation
   - Cold storage integration
   - Key recovery mechanisms

5. **Performance Research**
   - Node connection pooling
   - Transaction batching strategies
   - Blockchain data caching
   - Rate limiting for node providers
   - Failover and redundancy patterns

### Step 3: Analyze Current Implementation
Review existing blockchain services:
- `backend/app/services/blockchain_service.py`
- Wallet models in `backend/app/models/wallet.py`
- Current transaction handling patterns
- Security implementations

### Step 4: Create Comprehensive PRP
Create a PRP file in `PRPs/blockchain-{feature-name}.md` with:

#### Context Section
- Complete blockchain architecture overview
- Current implementation analysis
- Integration requirements and constraints
- Network-specific considerations (Bitcoin, Ethereum, Tron)

#### Technical Implementation Plan
- Detailed blockchain integration steps
- Network-specific implementation details
- Security implementation requirements
- Error handling and retry logic

#### Validation Requirements
- Testnet validation procedures
- Transaction confirmation monitoring
- Balance verification methods
- Security audit checkpoints
- Performance benchmarking

#### Network-Specific Considerations
**Bitcoin:**
- UTXO management
- Fee estimation algorithms
- Confirmation requirements (1-6 blocks)
- Address generation and validation

**Ethereum USDT:**
- ERC-20 token interactions
- Gas fee estimation and management
- Confirmation requirements (12+ blocks)
- Contract interaction security

**Tron USDT:**
- TRC-20 token interactions
- Energy and bandwidth management
- Confirmation requirements (19+ blocks)
- Resource optimization

### Step 5: Security and Compliance Integration
- Private key management requirements
- Transaction signing procedures
- Audit logging specifications
- Compliance monitoring integration
- Risk management protocols

### Step 6: Testing Strategy
- Unit testing requirements
- Integration testing with testnets
- Security testing procedures
- Performance testing benchmarks
- Disaster recovery testing

### Step 7: Confidence Assessment and Summary
Rate implementation confidence and provide:
- Key technical challenges
- Security considerations
- Performance implications
- Integration complexity
- Recommended implementation order

## Blockchain-Specific Validations

### Mandatory Security Checks
- Private key encryption verification
- Transaction signing validation
- Address generation security
- Network isolation (testnet/mainnet)
- Rate limiting implementation

### Performance Requirements
- Transaction processing speed targets
- Node response time monitoring
- Failover mechanism testing
- Resource usage optimization
- Scalability considerations

### Compliance Integration
- Transaction monitoring capabilities
- Audit trail completeness
- Regulatory reporting features
- KYC/AML integration points
- Data retention compliance

Execute this process systematically, ensuring all blockchain integration requirements are thoroughly addressed.
