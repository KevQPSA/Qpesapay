# Execute WebMCP-Enhanced PRP Implementation

Execute a comprehensive WebMCP-enhanced Product Requirements Prompt (PRP) for Qpesapay features with browser-based real-time integration.

## Command Usage
```
/execute-webmcp-prp <prp-file>
```

## Process

You are an expert financial systems developer implementing WebMCP-enhanced features for Qpesapay, a crypto-fiat payment processor for the Kenyan market. Execute the PRP with full browser integration and real-time capabilities.

### Step 1: Load Complete Context
Read and internalize the WebMCP-enhanced PRP file: `$ARGUMENTS`

Load all referenced context:
- CLAUDE.md for project rules and constraints
- Relevant examples from examples/ directory
- WebMCP integration patterns and security requirements
- Browser-based development workflow

### Step 2: Create Detailed Implementation Plan
Using task management tools, create a comprehensive task breakdown:

#### Backend Implementation Tasks
- API endpoint development with WebMCP integration
- Real-time data access endpoints
- Security validation for browser requests
- Database integration with live data access

#### WebMCP Integration Tasks
- Browser-based MCP server setup
- Financial-specific MCP tools implementation
- Real-time data synchronization
- Authentication integration with existing sessions

#### Frontend Integration Tasks
- Next.js component development
- React hooks for MCP management
- Real-time UI updates
- Browser extension compatibility

#### Testing and Validation Tasks
- Backend API testing
- WebMCP tool functionality testing
- Frontend integration testing
- Security validation testing

### Step 3: Systematic Implementation

#### Phase 1: Backend Foundation
**API Development**:
- Create or enhance API endpoints for browser integration
- Implement real-time data access patterns
- Add WebMCP-specific security validation
- Ensure proper CORS configuration

**Security Implementation**:
- Browser session authentication integration
- Rate limiting for MCP tool calls
- Input validation for browser requests
- Audit logging for WebMCP operations

#### Phase 2: WebMCP Server Implementation
**MCP Server Setup**:
```typescript
// Example implementation pattern
import { TabServerTransport } from '@mcp-b/transports';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

const qpesapayMcpServer = new McpServer({
  name: 'qpesapay-financial-system',
  version: '1.0.0',
});

// Implement financial-specific tools
await setupFinancialTools(qpesapayMcpServer);
```

**Financial Tools Implementation**:
- Payment validation tools
- Compliance checking tools
- Transaction monitoring tools
- Balance verification tools
- Fee calculation tools

#### Phase 3: Frontend Integration
**Next.js Integration**:
- Install WebMCP dependencies
- Set up MCP server in application
- Implement React hooks for MCP management
- Create real-time UI components

**Component Development**:
- Payment processing components with live validation
- Compliance status indicators
- Real-time transaction monitoring
- Dynamic fee display

#### Phase 4: Real-time Synchronization
**Data Synchronization**:
- Implement real-time state updates
- Cross-tab communication setup
- Conflict resolution strategies
- Performance optimization

### Step 4: WebMCP-Specific Validations

#### Browser Security Validation
- Same-origin policy compliance
- Content Security Policy configuration
- Session management security
- CORS configuration validation

#### MCP Tool Validation
- Tool functionality testing
- Input/output schema validation
- Error handling verification
- Rate limiting compliance

#### Real-time Performance Validation
- Response time measurement (<100ms for tools)
- Memory usage optimization
- Network efficiency testing
- Mobile browser compatibility

#### Financial System Validation
- Decimal precision in browser calculations
- Transaction idempotency with browser state
- Audit logging for all browser operations
- Compliance rule enforcement

### Step 5: Integration Testing

#### Backend Integration Testing
- API endpoint testing with browser requests
- Real-time data access validation
- Security middleware testing
- Database transaction integrity

#### WebMCP Integration Testing
- MCP server functionality testing
- Tool execution validation
- Cross-tab communication testing
- Browser extension compatibility

#### Frontend Integration Testing
- Component integration with MCP tools
- Real-time UI update validation
- User experience testing
- Mobile responsiveness verification

### Step 6: Security and Compliance Validation

#### Security Testing
- Browser-based authentication testing
- Session management validation
- Input sanitization verification
- Audit trail completeness

#### Compliance Testing
- KYC/AML integration validation
- Real-time compliance checking
- Regulatory reporting capability
- Data retention compliance

### Step 7: Performance Optimization

#### Browser Performance
- Memory usage optimization
- Network request minimization
- Caching strategy implementation
- Mobile browser optimization

#### Real-time Performance
- Data synchronization efficiency
- Tool execution speed optimization
- UI responsiveness enhancement
- Cross-tab coordination optimization

### Step 8: Documentation and Deployment

#### Documentation Updates
- WebMCP integration guide
- Browser development workflow
- Security configuration guide
- Troubleshooting documentation

#### Deployment Preparation
- Browser extension compatibility verification
- Production security configuration
- Performance monitoring setup
- Rollback procedures

## WebMCP Financial System Requirements

### Mandatory Implementations
- **Browser Authentication**: Seamless integration with existing sessions
- **Real-time Validation**: Live payment and compliance validation
- **Audit Logging**: Complete audit trail for browser operations
- **Security Headers**: Proper CSP and CORS configuration
- **Rate Limiting**: Protection against browser-based abuse

### Validation Requirements
- **Tool Functionality**: All MCP tools working correctly
- **Security Compliance**: Browser security model adherence
- **Performance Targets**: <100ms tool response times
- **Mobile Compatibility**: Full functionality on mobile browsers
- **Cross-tab Coordination**: Proper state synchronization

### Success Criteria
- All WebMCP tools functional and secure
- Real-time data synchronization working
- Browser security requirements met
- Performance targets achieved
- Complete audit trail implemented
- Mobile browser compatibility verified

Execute this process systematically, ensuring all WebMCP integration requirements and financial system security standards are met. Never compromise on security or compliance for the sake of browser functionality.
