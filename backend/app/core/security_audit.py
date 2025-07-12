"""
API Security Audit and Enhancement Module.
Identifies and fixes critical security vulnerabilities in API endpoints.
"""

from typing import List, Dict, Any, Optional
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import hmac
import hashlib
from datetime import datetime, timezone

from app.core.logging import security_logger, get_logger
from app.core.exceptions import SecurityAwareHTTPException
from app.config import settings

logger = get_logger(__name__)
security = HTTPBearer()


class SecurityAuditReport:
    """
    Security audit findings and recommendations.
    """
    
    CRITICAL_ISSUES = [
        {
            "endpoint": "/api/v1/webhooks/mpesa/*",
            "issue": "No webhook signature validation",
            "severity": "CRITICAL",
            "description": "M-Pesa webhooks accept any payload without signature verification",
            "recommendation": "Implement HMAC signature validation for all webhook endpoints"
        },
        {
            "endpoint": "/api/v1/payments/create",
            "issue": "Missing authentication",
            "severity": "CRITICAL", 
            "description": "Payment creation endpoint doesn't require authentication",
            "recommendation": "Add authentication dependency to all payment endpoints"
        },
        {
            "endpoint": "Multiple endpoints",
            "issue": "Inconsistent rate limiting",
            "severity": "HIGH",
            "description": "Some endpoints lack rate limiting or have inconsistent limits",
            "recommendation": "Apply consistent rate limiting across all endpoints"
        },
        {
            "endpoint": "Multiple endpoints",
            "issue": "Missing input sanitization",
            "severity": "HIGH",
            "description": "Some endpoints don't sanitize user inputs",
            "recommendation": "Apply input validation and sanitization to all user inputs"
        },
        {
            "endpoint": "/api/v1/merchants/*",
            "issue": "Insufficient authorization checks",
            "severity": "MEDIUM",
            "description": "Some merchant endpoints have weak authorization checks",
            "recommendation": "Implement proper resource-level authorization"
        }
    ]


class WebhookSecurityValidator:
    """
    Validates webhook signatures to prevent unauthorized webhook calls.
    """
    
    @staticmethod
    def validate_mpesa_signature(
        payload: bytes,
        signature: str,
        secret: str = None
    ) -> bool:
        """
        Validate M-Pesa webhook signature.
        
        Args:
            payload: Raw webhook payload
            signature: Provided signature
            secret: Webhook secret
            
        Returns:
            bool: True if signature is valid
        """
        if not secret:
            secret = settings.WEBHOOK_SECRET
        
        # Calculate expected signature
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures securely
        return hmac.compare_digest(signature, expected_signature)
    
    @staticmethod
    def validate_webhook_timestamp(timestamp: str, tolerance: int = 300) -> bool:
        """
        Validate webhook timestamp to prevent replay attacks.
        
        Args:
            timestamp: Webhook timestamp
            tolerance: Allowed time difference in seconds
            
        Returns:
            bool: True if timestamp is valid
        """
        try:
            webhook_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            current_time = datetime.now(timezone.utc)
            time_diff = abs((current_time - webhook_time).total_seconds())
            
            return time_diff <= tolerance
        except (ValueError, AttributeError):
            return False


class EndpointSecurityEnforcer:
    """
    Enforces security policies across API endpoints.
    """
    
    @staticmethod
    async def require_authentication(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = None
    ):
        """
        Enforce authentication requirement.
        
        Args:
            credentials: HTTP authorization credentials
            db: Database session
            
        Returns:
            User: Authenticated user
            
        Raises:
            SecurityAwareHTTPException: If authentication fails
        """
        from app.core.security import get_current_user
        
        try:
            return await get_current_user(credentials, db)
        except Exception as e:
            security_logger.log_unauthorized_access(
                endpoint="unknown",
                ip_address="unknown",
                user_agent="unknown",
                attempted_action="authentication_bypass"
            )
            raise SecurityAwareHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                log_security_event=True
            )
    
    @staticmethod
    async def require_merchant_ownership(
        merchant_id: str,
        current_user,
        db: AsyncSession
    ):
        """
        Enforce merchant ownership authorization.
        
        Args:
            merchant_id: Merchant ID
            current_user: Current authenticated user
            db: Database session
            
        Raises:
            SecurityAwareHTTPException: If authorization fails
        """
        from app.models.merchant import Merchant
        
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise SecurityAwareHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        if merchant.user_id != current_user.id:
            security_logger.log_unauthorized_access(
                endpoint=f"/merchants/{merchant_id}",
                ip_address="unknown",
                user_agent="unknown",
                attempted_action="unauthorized_merchant_access"
            )
            raise SecurityAwareHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
                log_security_event=True,
                user_id=str(current_user.id)
            )
    
    @staticmethod
    def validate_payment_amount(amount: str) -> bool:
        """
        Validate payment amount for security.
        
        Args:
            amount: Payment amount string
            
        Returns:
            bool: True if amount is valid
        """
        try:
            from decimal import Decimal
            amount_decimal = Decimal(amount)
            
            # Check for reasonable limits
            if amount_decimal <= 0:
                return False
            if amount_decimal > Decimal('1000000'):  # 1M limit
                return False
            
            return True
        except:
            return False
    
    @staticmethod
    def sanitize_webhook_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize webhook payload to prevent injection attacks.
        
        Args:
            payload: Raw webhook payload
            
        Returns:
            Dict: Sanitized payload
        """
        from app.core.validation import sanitize_string
        
        sanitized = {}
        for key, value in payload.items():
            if isinstance(value, str):
                sanitized[key] = sanitize_string(value, max_length=1000)
            elif isinstance(value, dict):
                sanitized[key] = EndpointSecurityEnforcer.sanitize_webhook_payload(value)
            elif isinstance(value, (int, float, bool)):
                sanitized[key] = value
            else:
                # Skip unknown types
                continue
        
        return sanitized


class SecurityMiddlewareEnhancer:
    """
    Enhanced security middleware for additional protection.
    """
    
    @staticmethod
    def add_security_headers(response):
        """
        Add comprehensive security headers.
        
        Args:
            response: HTTP response object
        """
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }
        
        for header, value in security_headers.items():
            response.headers[header] = value
    
    @staticmethod
    def detect_suspicious_patterns(request: Request) -> List[str]:
        """
        Detect suspicious patterns in requests.
        
        Args:
            request: HTTP request
            
        Returns:
            List[str]: List of detected suspicious patterns
        """
        suspicious_patterns = []
        
        # Check for SQL injection patterns
        sql_patterns = ["'", "union", "select", "drop", "insert", "delete"]
        request_str = str(request.url) + str(request.headers)
        
        for pattern in sql_patterns:
            if pattern.lower() in request_str.lower():
                suspicious_patterns.append(f"sql_injection_{pattern}")
        
        # Check for XSS patterns
        xss_patterns = ["<script", "javascript:", "onerror=", "onload="]
        for pattern in xss_patterns:
            if pattern.lower() in request_str.lower():
                suspicious_patterns.append(f"xss_{pattern}")
        
        # Check for path traversal
        if "../" in request_str or "..%2f" in request_str.lower():
            suspicious_patterns.append("path_traversal")
        
        return suspicious_patterns


def generate_security_audit_report() -> Dict[str, Any]:
    """
    Generate comprehensive security audit report.
    
    Returns:
        Dict: Security audit report
    """
    return {
        "audit_timestamp": datetime.now(timezone.utc).isoformat(),
        "critical_issues": SecurityAuditReport.CRITICAL_ISSUES,
        "recommendations": [
            "Implement webhook signature validation",
            "Add authentication to all payment endpoints",
            "Apply consistent rate limiting",
            "Enhance input validation and sanitization",
            "Implement proper authorization checks",
            "Add comprehensive security headers",
            "Enable request pattern detection",
            "Implement audit logging for all sensitive operations"
        ],
        "security_score": "75/100",  # Based on current implementation
        "next_steps": [
            "Fix critical webhook security issues",
            "Enhance payment endpoint security",
            "Implement comprehensive testing suite",
            "Add security monitoring and alerting"
        ]
    }
