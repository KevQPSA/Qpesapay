# WebMCP Integration Setup Guide for Qpesapay

This guide walks you through setting up WebMCP (Web Model Context Protocol) integration with your Qpesapay financial system, enabling real-time browser-based AI assistance.

## 🎯 Overview

WebMCP integration provides:
- **Real-time financial data access** through browser-based MCP tools
- **Live payment validation** and compliance checking
- **Interactive development** with actual financial system data
- **Secure browser-based** authentication and operations
- **Enhanced context engineering** with live data for PRPs

## 📋 Prerequisites

### System Requirements
- Node.js 18+ and npm 8+
- Modern browser with ES2020+ support
- Existing Qpesapay backend API running
- Valid authentication system in place

### Browser Compatibility
- Chrome 90+ (recommended for development)
- Firefox 88+
- Safari 14+
- Edge 90+

## 🚀 Installation Steps

### Step 1: Install WebMCP Dependencies

Create or update your frontend application's `package.json`:

```bash
# Navigate to your frontend directory
cd frontend/

# Install WebMCP dependencies
npm install @modelcontextprotocol/sdk @mcp-b/transports zod

# Install development dependencies
npm install --save-dev @types/node typescript
```

### Step 2: Set Up MCP Server

Copy the MCP server implementation:

```bash
# Copy the MCP server template
cp examples/webmcp/qpesapay_mcp_server.ts src/lib/
cp examples/webmcp/PaymentValidationComponent.tsx src/components/
cp examples/webmcp/nextjs_integration.tsx src/app/
```

### Step 3: Configure Next.js Application

Update your `next.config.js` to support WebMCP:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@modelcontextprotocol/sdk']
  },
  webpack: (config) => {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      net: false,
      tls: false,
    };
    return config;
  },
  headers: async () => [
    {
      source: '/api/:path*',
      headers: [
        { key: 'Access-Control-Allow-Origin', value: process.env.NEXT_PUBLIC_ALLOWED_ORIGINS || 'https://app.qpesapay.com,https://admin.qpesapay.com' },
        { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
        { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
      ],
    },
  ],
};

module.exports = nextConfig;
```

### Step 4: Set Up Authentication Integration

Ensure your API endpoints support browser-based authentication:

```typescript
// pages/api/auth/me.ts
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Verify authentication cookie/session
    const authToken = req.cookies.auth_token;
    
    if (!authToken) {
      return res.status(401).json({ error: 'Not authenticated' });
    }
    
    // Validate token and get user data
    const user = await validateAuthToken(authToken);
    
    res.json({
      id: user.id,
      email: user.email,
      role: user.role,
      kycStatus: user.kycStatus
    });
  } catch (error) {
    res.status(401).json({ error: 'Authentication failed' });
  }
}
```

### Step 5: Configure CORS for MCP Communication

Update your backend CORS configuration:

```python
# backend/app/core/config.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

## 🔧 Configuration

### Environment Variables

Create `.env.local` in your frontend directory:

```bash
# Frontend environment variables
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_MCP_SERVER_NAME=qpesapay-financial-system
NEXT_PUBLIC_MCP_VERSION=1.0.0

# Development settings
NODE_ENV=development
NEXT_PUBLIC_DEBUG_MCP=true
```

### Security Configuration

Update your Content Security Policy:

```javascript
// next.config.js - Add CSP headers
const nonce = crypto.randomUUID();
const cspHeader = `
  default-src 'self';
  script-src 'self' 'nonce-${nonce}';
  style-src 'self' 'nonce-${nonce}';
  img-src 'self' blob: data:;
  font-src 'self';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  connect-src 'self' ${process.env.NEXT_PUBLIC_API_BASE_URL};
`;

// Add to headers configuration
{
  source: '/(.*)',
  headers: [
    {
      key: 'Content-Security-Policy',
      value: cspHeader.replace(/\n/g, ''),
    },
  ],
}
```

## 🧪 Testing the Integration

### Step 1: Start Development Servers

```bash
# Terminal 1: Start backend
cd backend/
uvicorn app.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend/
npm run dev
```

### Step 2: Test MCP Connection

Open your browser to `http://localhost:3000` and check the browser console:

```javascript
// Should see in console:
// ✅ Qpesapay MCP Server connected successfully
```

### Step 3: Test Financial Tools

Use the payment validation component to test real-time validation:

1. Enter a payment amount (e.g., "100.50")
2. Select currencies (USDT → KES)
3. Enter a recipient phone number (+254712345678)
4. Observe real-time validation and fee calculation

### Step 4: Verify Security

Check that all security measures are working:

```bash
# Test authentication
curl -X GET http://localhost:3000/api/auth/me \
  -H "Cookie: auth_token=your_token"

# Test CORS
curl -X OPTIONS http://localhost:8000/api/v1/payments/validate \
  -H "Origin: http://localhost:3000"
```

## 🔍 Debugging

### Common Issues and Solutions

#### MCP Server Connection Failed
```javascript
// Check browser console for errors
console.error('MCP connection failed:', error);

// Solutions:
// 1. Verify API server is running
// 2. Check CORS configuration
// 3. Verify authentication cookies
// 4. Check network connectivity
```

#### Authentication Issues
```javascript
// Check authentication status
const response = await fetch('/api/auth/me');
console.log('Auth status:', response.status);

// Solutions:
// 1. Verify login credentials
// 2. Check cookie configuration
// 3. Verify session management
// 4. Check API authentication middleware
```

#### Tool Execution Errors
```javascript
// Debug MCP tool calls
try {
  const result = await mcpServer.callTool('validatePayment', params);
  console.log('Tool result:', result);
} catch (error) {
  console.error('Tool error:', error);
}

// Solutions:
// 1. Verify tool parameters
// 2. Check API endpoint availability
// 3. Verify input validation
// 4. Check rate limiting
```

### Debug Mode

Enable debug mode for detailed logging:

```typescript
// In your MCP server initialization
const mcpServer = new QpesapayMcpServer('/api/v1', {
  debug: process.env.NEXT_PUBLIC_DEBUG_MCP === 'true'
});
```

## 📊 Performance Optimization

### Caching Strategy

Implement caching for frequently accessed data:

```typescript
// Add caching to MCP tools
const cache = new Map();

const cachedValidation = cache.get(cacheKey);
if (cachedValidation && Date.now() - cachedValidation.timestamp < 30000) {
  return cachedValidation.result;
}
```

### Rate Limiting

Implement client-side rate limiting:

```typescript
// Rate limiting for MCP tool calls
const rateLimiter = new Map();

const canMakeRequest = (toolName: string) => {
  const lastCall = rateLimiter.get(toolName);
  const now = Date.now();
  
  if (lastCall && now - lastCall < 1000) { // 1 second cooldown
    return false;
  }
  
  rateLimiter.set(toolName, now);
  return true;
};
```

## 🚀 Production Deployment

### Build Configuration

```bash
# Build for production
npm run build

# Test production build locally
npm run start
```

### Environment Variables for Production

```bash
# Production environment variables
NEXT_PUBLIC_API_BASE_URL=https://api.qpesapay.com/api/v1
NEXT_PUBLIC_MCP_SERVER_NAME=qpesapay-financial-system
NEXT_PUBLIC_MCP_VERSION=1.0.0
NODE_ENV=production
```

### Security Checklist

- [ ] HTTPS enforced for all communications
- [ ] CSP headers properly configured
- [ ] Authentication cookies secure and httpOnly
- [ ] Rate limiting implemented
- [ ] Input validation on all MCP tools
- [ ] Audit logging enabled
- [ ] Error messages sanitized

## 📚 Next Steps

1. **Explore Advanced Features**: Implement additional MCP tools for blockchain monitoring and compliance
2. **Mobile Optimization**: Test and optimize for mobile browsers
3. **Performance Monitoring**: Set up monitoring for MCP tool performance
4. **User Training**: Train users on the new real-time capabilities
5. **Feedback Collection**: Gather user feedback on the WebMCP integration

## 🆘 Support

If you encounter issues:

1. Check the browser console for error messages
2. Verify all prerequisites are met
3. Review the debugging section above
4. Check the examples in `examples/webmcp/`
5. Ensure your backend API is properly configured

Remember: This is a financial system handling real money. Always prioritize security and compliance over convenience.
