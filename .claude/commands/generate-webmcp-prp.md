# Generate WebMCP-Enhanced PRP

Generate a comprehensive Product Requirements Prompt (PRP) with WebMCP browser-based integration for Qpesapay features.

## Command Usage
```
/generate-webmcp-prp <feature-file>
```

## Process

You are an expert financial systems architect specializing in browser-based MCP integration for crypto-fiat payment processors. Your task is to create a comprehensive PRP that includes both backend implementation and real-time browser interaction capabilities.

### Step 1: Read and Analyze Feature Request
Read the feature request file: `$ARGUMENTS`

### Step 2: Multi-Agent Research Phase (Parallel Execution)
Execute these research tasks simultaneously:

1. **Codebase Analysis**
   - Analyze existing payment processing patterns in `backend/app/services/payment/`
   - Review domain models in `backend/app/domain/`
   - Examine current API endpoints in `backend/app/api/v1/endpoints/`
   - Study security implementations in `backend/app/core/security.py`

2. **WebMCP Integration Research**
   - Research WebMCP browser-based MCP server patterns
   - Study @mcp-b/transports for browser integration
   - Analyze real-time data access patterns
   - Review browser security model for financial applications

3. **Financial System Research**
   - Research CBK (Central Bank of Kenya) requirements for web applications
   - Review KYC/AML compliance for browser-based systems
   - Analyze M-Pesa integration security for web interfaces
   - Study transaction monitoring for real-time systems

4. **Frontend Integration Research**
   - Research Next.js integration with WebMCP
   - Study React hooks for MCP server management
   - Analyze real-time state synchronization patterns
   - Review browser authentication integration

5. **Security Research**
   - Study browser-based financial application security
   - Research WebMCP security model for payment processors
   - Analyze session management for MCP tools
   - Review audit logging for browser-based operations

### Step 3: Create Comprehensive WebMCP-Enhanced PRP
Create a PRP file in `PRPs/webmcp-{feature-name}.md` with:

#### Context Section
- Complete project background from CLAUDE.md
- WebMCP integration architecture
- Browser-based development workflow
- Real-time data access patterns
- Security considerations for browser-based financial tools

#### Implementation Plan
**Backend Implementation**:
- Standard backend service implementation
- API endpoints for browser integration
- Real-time data access endpoints
- Security validation for browser requests

**WebMCP Integration**:
- Browser-based MCP server setup
- Financial-specific MCP tools
- Real-time data synchronization
- Authentication integration

**Frontend Integration**:
- Next.js component integration
- React hooks for MCP management
- Real-time UI updates
- Browser extension compatibility

#### WebMCP Tools Specification
Define specific MCP tools for the feature:
- Tool names and descriptions
- Input/output schemas using Zod
- Authentication requirements
- Rate limiting considerations
- Error handling patterns

#### Validation Gates
**Backend Validation**:
- Standard backend testing (unit, integration, security)
- API endpoint validation
- Database transaction testing

**WebMCP Validation**:
- Browser-based MCP server testing
- Tool functionality validation
- Real-time data synchronization testing
- Cross-tab communication testing

**Frontend Validation**:
- Component integration testing
- User experience validation
- Mobile responsiveness testing
- Browser compatibility testing

**Security Validation**:
- Browser security model compliance
- Session management validation
- CORS and CSP configuration
- Audit logging verification

#### Browser Development Workflow
- Local development setup with WebMCP
- Browser extension integration
- Real-time testing procedures
- Debugging and monitoring tools

### Step 4: WebMCP-Specific Considerations

#### Browser Security Model
- Same-origin policy compliance
- Content Security Policy configuration
- Session management integration
- CORS configuration for MCP communication

#### Real-time Data Access
- Live transaction monitoring
- Real-time compliance checking
- Dynamic fee calculation
- Instant validation feedback

#### Multi-tab Coordination
- Cross-tab state synchronization
- Shared authentication state
- Coordinated tool execution
- Conflict resolution strategies

#### Performance Optimization
- Browser-based caching strategies
- Efficient data synchronization
- Minimal network requests
- Optimized tool execution

### Step 5: Integration Examples
Include specific code examples for:
- WebMCP server setup in frontend application
- Financial-specific MCP tools
- React component integration
- Authentication flow integration

### Step 6: Confidence Assessment and Summary
Rate implementation confidence (1-10) based on:
- Completeness of WebMCP integration context
- Clarity of browser-based requirements
- Availability of financial system examples
- Complexity of real-time integration

Provide summary of:
- Key WebMCP integration challenges
- Browser security considerations
- Real-time data access requirements
- Frontend development complexity

## WebMCP Financial System Patterns

### Mandatory WebMCP Tools
- **Payment Validation**: Real-time payment validation with live data
- **Compliance Checking**: Instant KYC/AML status verification
- **Transaction Monitoring**: Live transaction status updates
- **Balance Verification**: Real-time wallet balance checking
- **Fee Calculation**: Dynamic fee estimation with current rates

### Security Requirements
- Browser session authentication integration
- Secure MCP tool execution
- Audit logging for all browser-based operations
- Rate limiting for MCP tool calls
- Input validation for all tool parameters

### Performance Requirements
- <100ms response time for MCP tools
- Real-time data synchronization
- Efficient browser memory usage
- Minimal network overhead
- Optimized for mobile browsers

### Compliance Integration
- Real-time KYC status checking
- Live AML screening
- Dynamic compliance rule evaluation
- Instant regulatory reporting
- Continuous audit trail generation

Execute this process systematically, ensuring all WebMCP integration requirements and financial system security considerations are thoroughly addressed.
