"""
Global error handlers for FastAPI application.
Provides secure error handling with proper logging and sanitization.
"""

import traceback
from typing import Union
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.core.exceptions import (
    QPesaPayException, SecureErrorHandler, SecurityAwareHTTPException
)
from app.core.logging import security_logger, get_logger
from app.config import settings

logger = get_logger(__name__)


async def qpesapay_exception_handler(request: Request, exc: QPesaPayException) -> JSONResponse:
    """
    Handle custom QPesaPay exceptions.
    
    Args:
        request: FastAPI request object
        exc: QPesaPay exception
        
    Returns:
        JSONResponse: Secure error response
    """
    # Determine appropriate HTTP status code
    status_code = status.HTTP_400_BAD_REQUEST
    
    if isinstance(exc, (AuthenticationError,)):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, (AuthorizationError,)):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, (ValidationError,)):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(exc, (PaymentError, WalletError)):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, (DatabaseError,)):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif isinstance(exc, (RateLimitError,)):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
    
    # Create secure error response
    error_response = SecureErrorHandler.create_error_response(
        status_code=status_code,
        message=exc.message,
        details=exc.details,
        is_production=settings.IS_PRODUCTION
    )
    
    # Log the error
    logger.error(
        "QPesaPay exception occurred",
        exception_type=type(exc).__name__,
        message=exc.message,
        details=exc.details,
        path=request.url.path,
        method=request.method,
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions with secure error responses.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSONResponse: Secure error response
    """
    # Check if it's our security-aware exception
    if isinstance(exc, SecurityAwareHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"message": exc.detail}},
            headers=exc.headers
        )
    
    # Create secure error response for regular HTTP exceptions
    error_response = SecureErrorHandler.create_error_response(
        status_code=exc.status_code,
        message=str(exc.detail),
        is_production=settings.IS_PRODUCTION
    )
    
    # Log security events for certain status codes
    if exc.status_code in [401, 403, 429]:
        security_logger.log_suspicious_activity(
            user_id="unknown",
            activity_type="http_error",
            details={
                "status_code": exc.status_code,
                "detail": str(exc.detail),
                "path": request.url.path,
                "method": request.method,
            },
            ip_address=request.client.host if request.client else "unknown"
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
        headers=getattr(exc, 'headers', None)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    
    Args:
        request: FastAPI request object
        exc: Validation error
        
    Returns:
        JSONResponse: Secure error response
    """
    # Extract validation errors
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append({"field": field, "message": message})
    
    # Create secure error response
    error_response = SecureErrorHandler.create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation failed",
        details={"validation_errors": errors} if not settings.IS_PRODUCTION else None,
        is_production=settings.IS_PRODUCTION
    )
    
    # Log validation errors (might indicate attack attempts)
    logger.warning(
        "Validation error occurred",
        path=request.url.path,
        method=request.method,
        errors=errors,
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Handle database errors securely.
    
    Args:
        request: FastAPI request object
        exc: SQLAlchemy error
        
    Returns:
        JSONResponse: Secure error response
    """
    # Log the full database error for debugging
    logger.error(
        "Database error occurred",
        error_type=type(exc).__name__,
        error_message=str(exc),
        path=request.url.path,
        method=request.method,
        traceback=traceback.format_exc() if not settings.IS_PRODUCTION else None,
    )
    
    # Create generic error response (never expose database details)
    error_response = SecureErrorHandler.create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="A database error occurred",
        is_production=True  # Always use production mode for DB errors
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all other exceptions securely.
    
    Args:
        request: FastAPI request object
        exc: General exception
        
    Returns:
        JSONResponse: Secure error response
    """
    # Log the full error for debugging
    logger.error(
        "Unhandled exception occurred",
        error_type=type(exc).__name__,
        error_message=str(exc),
        path=request.url.path,
        method=request.method,
        traceback=traceback.format_exc() if not settings.IS_PRODUCTION else None,
    )
    
    # Log as potential security event
    security_logger.log_suspicious_activity(
        user_id="unknown",
        activity_type="unhandled_exception",
        details={
            "error_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method,
        },
        ip_address=request.client.host if request.client else "unknown"
    )
    
    # Create generic error response
    error_response = SecureErrorHandler.create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected error occurred",
        is_production=settings.IS_PRODUCTION
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


def setup_error_handlers(app):
    """
    Set up all error handlers for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    # Custom exception handlers
    app.add_exception_handler(QPesaPayException, qpesapay_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("Error handlers configured successfully")
