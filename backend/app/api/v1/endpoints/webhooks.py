from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import json

from app.database import get_db
from app.services.mpesa_service import MpesaService
from app.core.security_audit import WebhookSecurityValidator, EndpointSecurityEnforcer
from app.core.logging import security_logger, get_logger
from app.core.exceptions import SecurityAwareHTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
mpesa_service = MpesaService()
limiter = Limiter(key_func=get_remote_address)
logger = get_logger(__name__)

@router.post("/mpesa/callback")
@limiter.limit("100/minute")  # High limit for legitimate webhooks
async def mpesa_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_signature: Optional[str] = Header(None, alias="X-Signature"),
    x_timestamp: Optional[str] = Header(None, alias="X-Timestamp")
):
    """
    Secure M-Pesa callback endpoint with signature validation.

    Args:
        request: HTTP request
        db: Database session
        x_signature: Webhook signature header
        x_timestamp: Webhook timestamp header

    Returns:
        Dict: Callback response

    Raises:
        SecurityAwareHTTPException: If security validation fails
    """
    client_ip = get_remote_address(request)

    try:
        # Get raw payload for signature validation
        raw_payload = await request.body()
        callback_data = json.loads(raw_payload.decode('utf-8'))

        # Validate webhook signature
        if x_signature:
            is_valid_signature = WebhookSecurityValidator.validate_mpesa_signature(
                payload=raw_payload,
                signature=x_signature
            )
            if not is_valid_signature:
                security_logger.log_suspicious_activity(
                    user_id="webhook",
                    activity_type="invalid_webhook_signature",
                    details={"endpoint": "/webhooks/mpesa/callback"},
                    ip_address=client_ip
                )
                raise SecurityAwareHTTPException(
                    status_code=401,
                    detail="Invalid webhook signature",
                    log_security_event=True
                )

        # Validate timestamp to prevent replay attacks
        if x_timestamp:
            is_valid_timestamp = WebhookSecurityValidator.validate_webhook_timestamp(x_timestamp)
            if not is_valid_timestamp:
                security_logger.log_suspicious_activity(
                    user_id="webhook",
                    activity_type="webhook_replay_attack",
                    details={"endpoint": "/webhooks/mpesa/callback", "timestamp": x_timestamp},
                    ip_address=client_ip
                )
                raise SecurityAwareHTTPException(
                    status_code=400,
                    detail="Invalid or expired timestamp",
                    log_security_event=True
                )

        # Sanitize webhook payload
        sanitized_data = EndpointSecurityEnforcer.sanitize_webhook_payload(callback_data)

        # Process the callback
        success = await mpesa_service.process_callback(sanitized_data)

        if success:
            logger.info(
                "M-Pesa callback processed successfully",
                callback_type="mpesa_callback",
                ip_address=client_ip
            )
            return {"ResultCode": 0, "ResultDesc": "Callback received successfully"}
        else:
            logger.error(
                "M-Pesa callback processing failed",
                callback_data=sanitized_data,
                ip_address=client_ip
            )
            raise HTTPException(status_code=400, detail="M-Pesa callback processing failed")

    except SecurityAwareHTTPException:
        raise
    except json.JSONDecodeError:
        security_logger.log_suspicious_activity(
            user_id="webhook",
            activity_type="invalid_webhook_payload",
            details={"endpoint": "/webhooks/mpesa/callback", "error": "invalid_json"},
            ip_address=client_ip
        )
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        logger.error(
            "Unexpected error in M-Pesa callback",
            error=str(e),
            ip_address=client_ip
        )
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/mpesa/timeout")
async def mpesa_timeout(request: Request):
    timeout_data = await request.json()
    print("M-Pesa Timeout Received:", timeout_data)
    # Handle timeout logic here (e.g., update transaction status to expired/failed)
    return {"ResultCode": 0, "ResultDesc": "Timeout received successfully"}

@router.post("/mpesa/result")
async def mpesa_result(request: Request):
    result_data = await request.json()
    print("M-Pesa Result Received:", result_data)
    # Handle result logic here (e.g., final transaction status update)
    return {"ResultCode": 0, "ResultDesc": "Result received successfully"}
