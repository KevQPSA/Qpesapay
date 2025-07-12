"""
Custom exception classes for QPesaPay backend.
Provides comprehensive error handling with proper HTTP status codes.
Includes secure error handling that doesn't leak sensitive information.
"""

import uuid
import traceback
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.core.logging import security_logger, get_logger

logger = get_logger(__name__)


class QPesaPayException(Exception):
    """Base exception class for QPesaPay application."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(QPesaPayException):
    """Authentication related errors."""
    pass


class AuthorizationError(QPesaPayException):
    """Authorization related errors."""
    pass


class ValidationError(QPesaPayException):
    """Data validation errors."""
    pass


class PaymentError(QPesaPayException):
    """Payment processing errors."""
    pass


class WalletError(QPesaPayException):
    """Wallet operation errors."""
    pass


class BlockchainError(QPesaPayException):
    """Blockchain interaction errors."""
    pass


class MpesaError(QPesaPayException):
    """M-Pesa integration errors."""
    pass


class DatabaseError(QPesaPayException):
    """Database operation errors."""
    pass


class RateLimitError(QPesaPayException):
    """Rate limiting errors."""
    pass


# HTTP Exception classes with proper status codes
class HTTPAuthenticationError(HTTPException):
    """HTTP Authentication error with 401 status."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class HTTPAuthorizationError(HTTPException):
    """HTTP Authorization error with 403 status."""
    
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class HTTPValidationError(HTTPException):
    """HTTP Validation error with 422 status."""
    
    def __init__(self, detail: str = "Validation failed", errors: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": detail, "errors": errors or {}},
        )


class HTTPPaymentError(HTTPException):
    """HTTP Payment error with 400 status."""
    
    def __init__(self, detail: str = "Payment processing failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class HTTPWalletError(HTTPException):
    """HTTP Wallet error with 400 status."""
    
    def __init__(self, detail: str = "Wallet operation failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class HTTPInsufficientFundsError(HTTPException):
    """HTTP Insufficient funds error with 402 status."""
    
    def __init__(self, detail: str = "Insufficient funds"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )


class HTTPNotFoundError(HTTPException):
    """HTTP Not found error with 404 status."""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class HTTPConflictError(HTTPException):
    """HTTP Conflict error with 409 status."""
    
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class HTTPRateLimitError(HTTPException):
    """HTTP Rate limit error with 429 status."""
    
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
        )


class HTTPInternalServerError(HTTPException):
    """HTTP Internal server error with 500 status."""
    
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class HTTPServiceUnavailableError(HTTPException):
    """HTTP Service unavailable error with 503 status."""

    def __init__(self, detail: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )


class SecureErrorHandler:
    """
    Secure error handler that sanitizes error messages and logs security events.
    Prevents sensitive information leakage while maintaining proper debugging.
    """

    # Sensitive patterns that should never be exposed
    SENSITIVE_PATTERNS = [
        'password', 'secret', 'key', 'token', 'hash', 'private',
        'database', 'connection', 'sql', 'query', 'traceback',
        'file', 'path', 'directory', 'env', 'config'
    ]

    # Generic error messages for production
    GENERIC_MESSAGES = {
        400: "Invalid request. Please check your input and try again.",
        401: "Authentication required. Please log in and try again.",
        403: "Access denied. You don't have permission to perform this action.",
        404: "The requested resource was not found.",
        409: "Conflict detected. The resource already exists or is in use.",
        422: "Invalid data provided. Please check your input.",
        429: "Too many requests. Please wait before trying again.",
        500: "An internal error occurred. Please try again later.",
        503: "Service temporarily unavailable. Please try again later.",
    }

    @classmethod
    def sanitize_error_message(cls, message: str, is_production: bool = True) -> str:
        """
        Sanitize error message to prevent information leakage.

        Args:
            message: Original error message
            is_production: Whether running in production

        Returns:
            str: Sanitized error message
        """
        if not is_production:
            return message

        # Check for sensitive patterns
        message_lower = message.lower()
        for pattern in cls.SENSITIVE_PATTERNS:
            if pattern in message_lower:
                return "An error occurred while processing your request."

        # Limit message length
        if len(message) > 200:
            return "An error occurred while processing your request."

        return message

    @classmethod
    def create_error_response(
        cls,
        status_code: int,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        is_production: bool = True
    ) -> Dict[str, Any]:
        """
        Create standardized error response.

        Args:
            status_code: HTTP status code
            message: Error message
            error_code: Application-specific error code
            details: Additional error details
            is_production: Whether running in production

        Returns:
            Dict: Standardized error response
        """
        # Generate unique error ID for tracking
        error_id = str(uuid.uuid4())

        # Use generic message in production for common status codes
        if is_production and status_code in cls.GENERIC_MESSAGES:
            user_message = cls.GENERIC_MESSAGES[status_code]
        else:
            user_message = cls.sanitize_error_message(message, is_production)

        response = {
            "error": {
                "id": error_id,
                "message": user_message,
                "status_code": status_code,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        }

        # Add error code if provided
        if error_code:
            response["error"]["code"] = error_code

        # Add details only in development
        if not is_production and details:
            response["error"]["details"] = details

        # Log the full error for debugging
        logger.error(
            "Error response generated",
            error_id=error_id,
            status_code=status_code,
            original_message=message,
            user_message=user_message,
            error_code=error_code,
            details=details,
        )

        return response

    @classmethod
    def log_security_error(
        cls,
        error_type: str,
        message: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ):
        """
        Log security-related errors.

        Args:
            error_type: Type of security error
            message: Error message
            user_id: User ID (if available)
            ip_address: IP address (if available)
            additional_context: Additional context
        """
        security_logger.log_suspicious_activity(
            user_id=user_id or "anonymous",
            activity_type=error_type,
            details={
                "message": message,
                "additional_context": additional_context or {},
            },
            ip_address=ip_address or "unknown"
        )


class SecurityAwareHTTPException(HTTPException):
    """
    HTTP Exception that automatically sanitizes error messages and logs security events.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        log_security_event: bool = False,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        # Import here to avoid circular imports
        from app.config import settings

        # Create secure error response
        error_response = SecureErrorHandler.create_error_response(
            status_code=status_code,
            message=detail,
            error_code=error_code,
            is_production=settings.IS_PRODUCTION
        )

        # Log security event if requested
        if log_security_event:
            SecureErrorHandler.log_security_error(
                error_type="http_error",
                message=detail,
                user_id=user_id,
                ip_address=ip_address,
                additional_context={"status_code": status_code, "error_code": error_code}
            )

        super().__init__(
            status_code=status_code,
            detail=error_response["error"]["message"],
            headers=headers
        )

        # Store full error info for internal use
        self.error_id = error_response["error"]["id"]
        self.original_detail = detail
        self.error_code = error_code