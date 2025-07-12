"""
Custom exception classes for QPesaPay backend.
Provides comprehensive error handling with proper HTTP status codes.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


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