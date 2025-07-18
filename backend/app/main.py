"""
Main FastAPI application for QPesaPay backend.
Configures the application with middleware, routes, and error handling.
"""

from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.middleware import RequestLoggingMiddleware, AuthenticationMiddleware
from app.core.exceptions import QPesaPayException
from app.core.error_handlers import setup_error_handlers
from app.database import check_db_connection
from app.api.v1.api import api_router
from app.middleware.security_headers import (
    SecurityHeadersMiddleware,
    RateLimitMiddleware,
    SSRFProtectionMiddleware
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("QPesaPay application starting up")

    # TODO: Initialize services
    # - Database connection pool
    # - Redis connection
    # - Background task scheduler
    # - External service connections

    logger.info("QPesaPay application startup complete")

    yield

    # Shutdown
    logger.info("QPesaPay application shutting down")

    # TODO: Cleanup resources
    # - Close database connections
    # - Close Redis connections
    # - Stop background tasks
    # - Flush logs

    logger.info("QPesaPay application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Kenya Market Payment Gateway - Web-first crypto-fiat payment processor",
    version="1.0.0",
    docs_url="/docs" if not settings.IS_PRODUCTION else None,
    redoc_url="/redoc" if not settings.IS_PRODUCTION else None,
    lifespan=lifespan,
)

# Add CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

# Add OWASP-compliant security middleware (consolidated)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SSRFProtectionMiddleware)

# Add core middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(AuthenticationMiddleware)

# Add rate limiting middleware with testing bypass
import os
if not (os.getenv('TESTING') == 'true' or os.getenv('CI') == 'true'):
    app.add_middleware(RateLimitMiddleware)

# Setup comprehensive error handlers
setup_error_handlers(app)


# Exception handlers
@app.exception_handler(QPesaPayException)
async def qpesapay_exception_handler(request: Request, exc: QPesaPayException):
    """Handle custom QPesaPay exceptions."""
    logger.error(
        "QPesaPay exception occurred",
        exception_type=type(exc).__name__,
        message=exc.message,
        details=exc.details,
        url=str(request.url),
        method=request.method,
    )
    
    return JSONResponse(
        status_code=400,
        content={
            "error": type(exc).__name__,
            "message": exc.message,
            "details": exc.details,
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(
        "Validation error occurred",
        errors=exc.errors(),
        url=str(request.url),
        method=request.method,
    )

    # Serialize error details to ensure JSON compatibility
    serialized_errors = []
    for error in exc.errors():
        serialized_error = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": str(error.get("input")) if error.get("input") is not None else None,
        }
        # Handle ctx field which may contain non-serializable objects
        if "ctx" in error:
            ctx = error["ctx"]
            if isinstance(ctx, dict):
                serialized_ctx = {}
                for key, value in ctx.items():
                    try:
                        # Try to serialize the value
                        import json
                        json.dumps(value)
                        serialized_ctx[key] = value
                    except (TypeError, ValueError):
                        # If not serializable, convert to string
                        serialized_ctx[key] = str(value)
                serialized_error["ctx"] = serialized_ctx
        serialized_errors.append(serialized_error)

    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "details": serialized_errors,
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.warning(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        url=str(request.url),
        method=request.method,
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "status_code": exc.status_code,
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(
        "Unexpected exception occurred",
        exception_type=type(exc).__name__,
        message=str(exc),
        url=str(request.url),
        method=request.method,
        exc_info=True,
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
        }
    )


# Health check endpoints
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint with basic information."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "description": "Kenya Market Payment Gateway",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status information
        
    Raises:
        HTTPException: If any service is unhealthy
    """
    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {}
    }
    
    # Check database connection
    try:
        db_healthy = await check_db_connection()
        health_status["services"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "response_time": None  # TODO: Add response time measurement
        }
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    # TODO: Add more service health checks
    # - Redis connection
    # - External API connectivity (M-Pesa, blockchain)
    # - File system access
    
    if health_status["status"] == "unhealthy":
        raise HTTPException(
            status_code=503,
            detail="One or more services are unhealthy"
        )
    
    return health_status


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """
    Get application metrics for monitoring.
    
    Returns:
        dict: Application metrics
    """
    # TODO: Implement proper metrics collection
    # This would typically integrate with Prometheus or similar
    
    return {
        "uptime": "unknown",
        "requests_total": "unknown",
        "requests_per_second": "unknown",
        "active_connections": "unknown",
        "memory_usage": "unknown",
        "cpu_usage": "unknown",
    }


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


# Event handlers have been moved to the lifespan context manager above


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=not settings.IS_PRODUCTION,
        log_level=settings.LOG_LEVEL.lower(),
    )