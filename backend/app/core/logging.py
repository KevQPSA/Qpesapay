"""
Logging configuration for Qpesapay backend.
Sets up structured logging with proper formatting and handlers.
Includes security monitoring, audit trails, and performance tracking.
"""

import logging
import logging.config
import logging.handlers
import sys
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path
import structlog
from contextvars import ContextVar

from app.config import settings

# Context variables for request tracking
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)
ip_address_var: ContextVar[Optional[str]] = ContextVar('ip_address', default=None)


def setup_logging():
    """
    Configure comprehensive structured logging for the application.
    Sets up file handlers, security monitoring, and audit trails.
    """
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure file handlers
    handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'json' if settings.IS_PRODUCTION else 'console',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_dir / 'app.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
        'security': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_dir / 'security.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,  # Keep more security logs
            'formatter': 'json',
        },
        'audit': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_dir / 'audit.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 20,  # Keep many audit logs
            'formatter': 'json',
        },
        'transactions': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_dir / 'transactions.log',
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 15,  # Keep many transaction logs
            'formatter': 'json',
        },
    }

    # Configure formatters
    formatters = {
        'json': {
            'format': '%(message)s',
        },
        'console': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    }

    # Configure loggers
    loggers = {
        '': {  # Root logger
            'level': settings.LOG_LEVEL.upper(),
            'handlers': ['console', 'file'],
        },
        'security': {
            'level': 'INFO',
            'handlers': ['console', 'security'],
            'propagate': False,
        },
        'audit': {
            'level': 'INFO',
            'handlers': ['console', 'audit'],
            'propagate': False,
        },
        'transactions': {
            'level': 'INFO',
            'handlers': ['console', 'transactions'],
            'propagate': False,
        },
    }

    # Apply logging configuration
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': handlers,
        'loggers': loggers,
    })

    # Configure structlog
    structlog.configure(
        processors=[
            # Add log level and timestamp
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # Add custom processors
            add_request_context,
            add_security_context,
            # Final processor for output format
            structlog.dev.ConsoleRenderer() if not settings.IS_PRODUCTION else structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def add_request_context(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add request context to log entries.

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Dict: Updated event dictionary
    """
    # Add request ID from context
    request_id = request_id_var.get()
    if request_id:
        event_dict['request_id'] = request_id

    # Add user ID from context
    user_id = user_id_var.get()
    if user_id:
        event_dict['user_id'] = user_id

    # Add IP address from context
    ip_address = ip_address_var.get()
    if ip_address:
        event_dict['ip_address'] = ip_address

    return event_dict


def add_security_context(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add security context to log entries.

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Dict: Updated event dictionary
    """
    # Add timestamp in UTC
    event_dict['timestamp_utc'] = datetime.now(timezone.utc).isoformat()

    # Add environment info
    event_dict['environment'] = 'production' if settings.IS_PRODUCTION else 'development'

    # Add process info for debugging
    event_dict['process_id'] = os.getpid()

    return event_dict


def set_request_context(request_id: str, user_id: Optional[str] = None, ip_address: Optional[str] = None):
    """
    Set request context for logging.

    Args:
        request_id: Request ID
        user_id: User ID (optional)
        ip_address: IP address (optional)
    """
    request_id_var.set(request_id)
    if user_id:
        user_id_var.set(user_id)
    if ip_address:
        ip_address_var.set(ip_address)


def clear_request_context():
    """Clear request context."""
    request_id_var.set(None)
    user_id_var.set(None)
    ip_address_var.set(None)


class SecurityLogger:
    """
    Specialized logger for security events.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger("security")
    
    def log_login_attempt(self, email: str, success: bool, ip_address: str, user_agent: str = None):
        """
        Log login attempt.
        
        Args:
            email: User email
            success: Whether login was successful
            ip_address: Client IP address
            user_agent: User agent string
        """
        self.logger.info(
            "Login attempt",
            event_type="login_attempt",
            email=email,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    def log_password_change(self, user_id: str, ip_address: str):
        """
        Log password change event.
        
        Args:
            user_id: User ID
            ip_address: Client IP address
        """
        self.logger.info(
            "Password changed",
            event_type="password_change",
            user_id=user_id,
            ip_address=ip_address,
        )
    
    def log_suspicious_activity(self, user_id: str, activity_type: str, details: Dict[str, Any], ip_address: str):
        """
        Log suspicious activity.
        
        Args:
            user_id: User ID
            activity_type: Type of suspicious activity
            details: Additional details
            ip_address: Client IP address
        """
        self.logger.warning(
            "Suspicious activity detected",
            event_type="suspicious_activity",
            user_id=user_id,
            activity_type=activity_type,
            details=details,
            ip_address=ip_address,
        )
    
    def log_api_key_usage(self, api_key_id: str, endpoint: str, ip_address: str, success: bool):
        """
        Log API key usage.

        Args:
            api_key_id: API key ID
            endpoint: API endpoint accessed
            ip_address: Client IP address
            success: Whether request was successful
        """
        self.logger.info(
            "API key used",
            event_type="api_key_usage",
            api_key_id=api_key_id,
            endpoint=endpoint,
            ip_address=ip_address,
            success=success,
        )

    def log_account_lockout(self, user_id: str, email: str, failed_attempts: int, lockout_duration: int, ip_address: str):
        """
        Log account lockout event.

        Args:
            user_id: User ID
            email: User email
            failed_attempts: Number of failed attempts
            lockout_duration: Lockout duration in minutes
            ip_address: Client IP address
        """
        self.logger.warning(
            "Account locked due to failed login attempts",
            event_type="account_lockout",
            user_id=user_id,
            email=email,
            failed_attempts=failed_attempts,
            lockout_duration_minutes=lockout_duration,
            ip_address=ip_address,
        )

    def log_token_blacklisted(self, user_id: str, token_type: str, reason: str, ip_address: str):
        """
        Log token blacklisting event.

        Args:
            user_id: User ID
            token_type: Type of token (access/refresh)
            reason: Reason for blacklisting
            ip_address: Client IP address
        """
        self.logger.info(
            "Token blacklisted",
            event_type="token_blacklisted",
            user_id=user_id,
            token_type=token_type,
            reason=reason,
            ip_address=ip_address,
        )

    def log_rate_limit_exceeded(self, endpoint: str, ip_address: str, user_id: Optional[str] = None):
        """
        Log rate limit exceeded event.

        Args:
            endpoint: API endpoint
            ip_address: Client IP address
            user_id: User ID (if authenticated)
        """
        self.logger.warning(
            "Rate limit exceeded",
            event_type="rate_limit_exceeded",
            endpoint=endpoint,
            ip_address=ip_address,
            user_id=user_id,
        )

    def log_unauthorized_access(self, endpoint: str, ip_address: str, user_agent: str, attempted_action: str):
        """
        Log unauthorized access attempt.

        Args:
            endpoint: API endpoint
            ip_address: Client IP address
            user_agent: User agent string
            attempted_action: What the user tried to do
        """
        self.logger.warning(
            "Unauthorized access attempt",
            event_type="unauthorized_access",
            endpoint=endpoint,
            ip_address=ip_address,
            user_agent=user_agent,
            attempted_action=attempted_action,
        )

    def log_data_breach_attempt(self, user_id: str, attempted_data: str, ip_address: str, details: Dict[str, Any]):
        """
        Log potential data breach attempt.

        Args:
            user_id: User ID
            attempted_data: Type of data attempted to access
            ip_address: Client IP address
            details: Additional details
        """
        self.logger.critical(
            "Potential data breach attempt detected",
            event_type="data_breach_attempt",
            user_id=user_id,
            attempted_data=attempted_data,
            ip_address=ip_address,
            details=details,
        )


class TransactionLogger:
    """
    Specialized logger for transaction events.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger("transactions")
    
    def log_payment_initiated(self, transaction_id: str, user_id: str, amount: str, currency: str, recipient: str):
        """
        Log payment initiation.
        
        Args:
            transaction_id: Transaction ID
            user_id: User ID
            amount: Payment amount
            currency: Currency type
            recipient: Recipient address/identifier
        """
        self.logger.info(
            "Payment initiated",
            event_type="payment_initiated",
            transaction_id=transaction_id,
            user_id=user_id,
            amount=amount,
            currency=currency,
            recipient=recipient,
        )
    
    def log_payment_confirmed(self, transaction_id: str, blockchain_hash: str, confirmations: int):
        """
        Log payment confirmation.
        
        Args:
            transaction_id: Transaction ID
            blockchain_hash: Blockchain transaction hash
            confirmations: Number of confirmations
        """
        self.logger.info(
            "Payment confirmed",
            event_type="payment_confirmed",
            transaction_id=transaction_id,
            blockchain_hash=blockchain_hash,
            confirmations=confirmations,
        )
    
    def log_payment_failed(self, transaction_id: str, error: str, user_id: str):
        """
        Log payment failure.
        
        Args:
            transaction_id: Transaction ID
            error: Error message
            user_id: User ID
        """
        self.logger.error(
            "Payment failed",
            event_type="payment_failed",
            transaction_id=transaction_id,
            error=error,
            user_id=user_id,
        )
    
    def log_settlement_initiated(self, settlement_id: str, merchant_id: str, amount: str, method: str):
        """
        Log settlement initiation.
        
        Args:
            settlement_id: Settlement ID
            merchant_id: Merchant ID
            amount: Settlement amount
            method: Settlement method (mpesa, bank)
        """
        self.logger.info(
            "Settlement initiated",
            event_type="settlement_initiated",
            settlement_id=settlement_id,
            merchant_id=merchant_id,
            amount=amount,
            method=method,
        )
    
    def log_settlement_completed(self, settlement_id: str, reference: str):
        """
        Log settlement completion.
        
        Args:
            settlement_id: Settlement ID
            reference: External reference (M-Pesa, bank reference)
        """
        self.logger.info(
            "Settlement completed",
            event_type="settlement_completed",
            settlement_id=settlement_id,
            reference=reference,
        )


class AuditLogger:
    """
    Specialized logger for audit events.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger("audit")
    
    def log_user_action(self, user_id: str, action: str, resource: str, details: Dict[str, Any] = None):
        """
        Log user action for audit trail.
        
        Args:
            user_id: User ID
            action: Action performed (create, update, delete, view)
            resource: Resource affected
            details: Additional details
        """
        self.logger.info(
            "User action",
            event_type="user_action",
            user_id=user_id,
            action=action,
            resource=resource,
            details=details or {},
        )
    
    def log_admin_action(self, admin_id: str, action: str, target_user_id: str = None, details: Dict[str, Any] = None):
        """
        Log admin action for audit trail.
        
        Args:
            admin_id: Admin user ID
            action: Action performed
            target_user_id: Target user ID (if applicable)
            details: Additional details
        """
        self.logger.info(
            "Admin action",
            event_type="admin_action",
            admin_id=admin_id,
            action=action,
            target_user_id=target_user_id,
            details=details or {},
        )
    
    def log_system_event(self, event_type: str, details: Dict[str, Any]):
        """
        Log system event for audit trail.
        
        Args:
            event_type: Type of system event
            details: Event details
        """
        self.logger.info(
            "System event",
            event_type="system_event",
            system_event_type=event_type,
            details=details,
        )


class PerformanceLogger:
    """
    Specialized logger for performance monitoring.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger("performance")
    
    def log_slow_query(self, query: str, duration: float, params: Dict[str, Any] = None):
        """
        Log slow database query.
        
        Args:
            query: SQL query
            duration: Query duration in seconds
            params: Query parameters
        """
        self.logger.warning(
            "Slow query detected",
            event_type="slow_query",
            query=query,
            duration=duration,
            params=params or {},
        )
    
    def log_api_performance(self, endpoint: str, method: str, duration: float, status_code: int):
        """
        Log API endpoint performance.
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            duration: Request duration in seconds
            status_code: HTTP status code
        """
        level = "warning" if duration > 1.0 else "info"
        getattr(self.logger, level)(
            "API performance",
            event_type="api_performance",
            endpoint=endpoint,
            method=method,
            duration=duration,
            status_code=status_code,
        )
    
    def log_blockchain_performance(self, network: str, operation: str, duration: float, success: bool):
        """
        Log blockchain operation performance.
        
        Args:
            network: Blockchain network
            operation: Operation type
            duration: Operation duration in seconds
            success: Whether operation was successful
        """
        self.logger.info(
            "Blockchain performance",
            event_type="blockchain_performance",
            network=network,
            operation=operation,
            duration=duration,
            success=success,
        )


# Global logger instances
security_logger = SecurityLogger()
transaction_logger = TransactionLogger()
audit_logger = AuditLogger()
performance_logger = PerformanceLogger()


def get_logger(name: str):
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)