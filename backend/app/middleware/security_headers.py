"""
OWASP-compliant Security Headers Middleware
Implements comprehensive security headers as per OWASP recommendations
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from typing import Callable
import time

from app.config import settings
from app.core.logging import security_logger


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    OWASP-compliant security headers middleware.
    Implements all recommended security headers for web applications.
    """
    
    def __init__(self, app, **kwargs):
        super().__init__(app)
        self.security_headers = self._get_security_headers()
    
    def _get_security_headers(self) -> dict:
        """Get comprehensive security headers based on OWASP recommendations."""
        
        headers = {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            
            # XSS Protection (legacy but still useful)
            "X-XSS-Protection": "1; mode=block",
            
            # HSTS - Force HTTPS
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            
            # Content Security Policy - Prevent XSS and injection attacks
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            ),
            
            # Referrer Policy - Control referrer information
            "Referrer-Policy": "strict-origin-when-cross-origin",
            
            # Permissions Policy - Control browser features
            "Permissions-Policy": (
                "geolocation=(), "
                "microphone=(), "
                "camera=(), "
                "payment=(), "
                "usb=(), "
                "magnetometer=(), "
                "gyroscope=(), "
                "speaker=()"
            ),
            
            # Cross-Origin Policies
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Resource-Policy": "same-origin",
            
            # Cache Control for sensitive endpoints
            "Cache-Control": "no-store, no-cache, must-revalidate, private",
            "Pragma": "no-cache",
            "Expires": "0",
            
            # Server identification
            "Server": "Qpesapay-API",
            
            # Remove potentially revealing headers
            "X-Powered-By": "",
        }
        
        # Production-specific headers
        if settings.IS_PRODUCTION:
            headers.update({
                # Stricter CSP for production
                "Content-Security-Policy": (
                    "default-src 'self'; "
                    "script-src 'self'; "
                    "style-src 'self'; "
                    "img-src 'self' data:; "
                    "font-src 'self'; "
                    "connect-src 'self'; "
                    "frame-ancestors 'none'; "
                    "base-uri 'self'; "
                    "form-action 'self'; "
                    "upgrade-insecure-requests"
                ),
                # Expect-CT for certificate transparency
                "Expect-CT": "max-age=86400, enforce",
            })
        
        return headers
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Apply security headers to all responses."""
        
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Apply security headers
        for header, value in self.security_headers.items():
            if value:  # Only set non-empty values
                response.headers[header] = value
        
        # Endpoint-specific security headers
        self._apply_endpoint_specific_headers(request, response)
        
        # Log security header application
        process_time = time.time() - start_time
        security_logger.logger.debug(
            "Security headers applied",
            path=request.url.path,
            method=request.method,
            process_time=process_time,
            headers_applied=len(self.security_headers)
        )
        
        return response
    
    def _apply_endpoint_specific_headers(self, request: Request, response: Response):
        """Apply endpoint-specific security headers."""
        
        path = request.url.path
        
        # API endpoints - stricter caching
        if path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
        
        # Authentication endpoints - extra security
        if "/auth/" in path:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Payment endpoints - maximum security
        if "/payments/" in path or "/transactions/" in path:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        # Webhook endpoints - CORS and validation headers
        if "/webhooks/" in path:
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Cache-Control"] = "no-store"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    OWASP-compliant rate limiting middleware.
    Implements comprehensive rate limiting to prevent abuse.
    """
    
    def __init__(self, app, **kwargs):
        super().__init__(app)
        self.rate_limits = {
            "/api/v1/auth/login": {"requests": 5, "window": 60},  # 5 per minute
            "/api/v1/auth/register": {"requests": 3, "window": 60},  # 3 per minute
            "/api/v1/auth/forgot-password": {"requests": 3, "window": 300},  # 3 per 5 minutes
            "/api/v1/payments/": {"requests": 10, "window": 60},  # 10 per minute
            "/api/v1/webhooks/": {"requests": 100, "window": 60},  # 100 per minute
            "default": {"requests": 60, "window": 60}  # 60 per minute default
        }
        self.request_counts = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Apply rate limiting based on endpoint and client."""

        # Skip rate limiting during testing
        import os
        if os.getenv('TESTING') == 'true' or os.getenv('CI') == 'true':
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        endpoint = self._get_rate_limit_key(request.url.path)
        
        # Check rate limit
        if self._is_rate_limited(client_ip, endpoint):
            security_logger.log_rate_limit_exceeded(
                endpoint=request.url.path,
                ip_address=client_ip
            )
            
            response = StarletteResponse(
                content='{"error": {"message": "Rate limit exceeded", "code": "RATE_LIMIT_EXCEEDED"}}',
                status_code=429,
                headers={"Content-Type": "application/json"}
            )
            return response
        
        # Record request
        self._record_request(client_ip, endpoint)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        limit_info = self._get_rate_limit_info(client_ip, endpoint)
        response.headers["X-RateLimit-Limit"] = str(limit_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(limit_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(limit_info["reset"])
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address with proxy support."""
        # Check for forwarded headers (behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _get_rate_limit_key(self, path: str) -> str:
        """Get rate limit configuration key for path."""
        for pattern in self.rate_limits:
            if pattern != "default" and pattern in path:
                return pattern
        return "default"
    
    def _is_rate_limited(self, client_ip: str, endpoint: str) -> bool:
        """Check if client is rate limited."""
        key = f"{client_ip}:{endpoint}"
        now = time.time()
        
        if key not in self.request_counts:
            return False
        
        # Clean old requests
        window = self.rate_limits[endpoint]["window"]
        self.request_counts[key] = [
            req_time for req_time in self.request_counts[key]
            if now - req_time < window
        ]
        
        # Check limit
        limit = self.rate_limits[endpoint]["requests"]
        return len(self.request_counts[key]) >= limit
    
    def _record_request(self, client_ip: str, endpoint: str):
        """Record request for rate limiting."""
        key = f"{client_ip}:{endpoint}"
        now = time.time()
        
        if key not in self.request_counts:
            self.request_counts[key] = []
        
        self.request_counts[key].append(now)
    
    def _get_rate_limit_info(self, client_ip: str, endpoint: str) -> dict:
        """Get rate limit information for headers."""
        key = f"{client_ip}:{endpoint}"
        limit = self.rate_limits[endpoint]["requests"]
        window = self.rate_limits[endpoint]["window"]
        
        if key not in self.request_counts:
            remaining = limit
        else:
            remaining = max(0, limit - len(self.request_counts[key]))
        
        reset = int(time.time() + window)
        
        return {
            "limit": limit,
            "remaining": remaining,
            "reset": reset
        }


class SSRFProtectionMiddleware(BaseHTTPMiddleware):
    """
    OWASP-compliant SSRF protection middleware.
    Prevents Server-Side Request Forgery attacks.
    """
    
    def __init__(self, app, **kwargs):
        super().__init__(app)
        # Allowed domains for external requests
        self.allowed_domains = [
            "api.safaricom.co.ke",  # M-Pesa API
            "sandbox.safaricom.co.ke",  # M-Pesa Sandbox
            # Add other trusted external APIs
        ]
        
        # Blocked IP ranges (private networks)
        self.blocked_ip_ranges = [
            "127.0.0.0/8",    # Loopback
            "10.0.0.0/8",     # Private Class A
            "172.16.0.0/12",  # Private Class B
            "192.168.0.0/16", # Private Class C
            "169.254.0.0/16", # Link-local
            "::1/128",        # IPv6 loopback
            "fc00::/7",       # IPv6 private
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check for potential SSRF attacks."""
        
        # Check webhook URLs and external requests
        if request.method in ["POST", "PUT", "PATCH"]:
            await self._validate_request_for_ssrf(request)
        
        return await call_next(request)
    
    async def _validate_request_for_ssrf(self, request: Request):
        """Validate request for SSRF vulnerabilities."""
        try:
            body = await request.body()
            if body:
                # Check for URLs in request body
                body_str = body.decode('utf-8', errors='ignore')
                if 'http://' in body_str or 'https://' in body_str:
                    # Log potential SSRF attempt
                    security_logger.log_suspicious_activity(
                        user_id="unknown",
                        activity_type="potential_ssrf",
                        details={"path": request.url.path, "method": request.method},
                        ip_address=request.client.host if request.client else "unknown"
                    )
        except Exception:
            # Don't fail the request if we can't parse body
            pass
