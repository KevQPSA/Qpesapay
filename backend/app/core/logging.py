"""
Logging configuration for Qpesapay backend.
Sets up structured logging with proper formatting and handlers.
"""

import logging
import logging.config
import sys
from typing import Dict, Any
import structlog

from app.config import settings


def setup_logging():
    """
    Configure structured logging for the application.
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    )
    
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
            add_request_id,
            add_user_context,
            # Final processor for output format
            structlog.dev.ConsoleRenderer() if not settings.IS_PRODUCTION else structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def add_request_id(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add request ID to log entries if available.
    
    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary
        
    Returns:
        Dict: Updated event dictionary
    """
    # TODO: Extract request ID from context
    # This would typically come from middleware that sets request ID
    request_id = getattr(logger, '_request_id', None)
    if request_id:
        event_dict['request_id'] = request_id
    
    return event_dict


def add_user_context(logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add user context to log entries if available.
    
    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary
        
    Returns:
        Dict: Updated event dictionary
    """
    # TODO: Extract user context from request
    # This would typically come from authentication middleware
    user_id = getattr(logger, '_user_id', None)
    if user_id:
        event_dict['user_id'] = user_id
    
    return event_dict


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