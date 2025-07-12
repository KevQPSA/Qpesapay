"""
Payment API Endpoints.
Refactored to use Sandi Metz-style architecture with dependency injection.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from decimal import Decimal

from app.database import get_db
from app.container import container
from app.commands.payment_commands import CreatePaymentCommand
from app.queries.payment_queries import GetTransactionQuery
from app.domain import Currency
from app.core.exceptions import ValidationError

router = APIRouter()

# Request/Response Models (keeping existing for compatibility)
from pydantic import BaseModel
from typing import Optional

class CreatePaymentRequest(BaseModel):
    """Request model for creating payments."""
    user_id: str
    amount: str
    currency: str
    recipient_address: str
    recipient_network: str
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    """Response model for payment operations."""
    transaction_id: str
    status: str
    blockchain_hash: Optional[str] = None
    estimated_confirmation_time: int = 300
    gas_fee: str = "0"


@router.post("/create", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    request: CreatePaymentRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new payment using Sandi Metz-style architecture.
    Clean, focused endpoint that delegates to command handler.
    """
    try:
        # Create command from request
        command = CreatePaymentCommand(
            user_id=UUID(request.user_id),
            amount=Decimal(request.amount),
            currency=Currency(request.currency.upper()),
            recipient_address=request.recipient_address,
            recipient_network=request.recipient_network,
            description=request.description
        )

        # Get command handler from container
        handler = container.get_with_db('create_payment_handler', db)

        # Execute command
        transaction_record = await handler.handle(command)

        # Return response
        return PaymentResponse(
            transaction_id=str(transaction_record.id),
            status=transaction_record.status,
            blockchain_hash=transaction_record.blockchain_hash,
            estimated_confirmation_time=300,
            gas_fee=str(transaction_record.fees_paid.amount)
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{transaction_id}", response_model=PaymentResponse)
async def get_payment_status(
    transaction_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get payment status using query handler.
    Clean separation between commands and queries.
    """
    try:
        # Create query
        query = GetTransactionQuery(transaction_id=UUID(transaction_id))

        # Get query handler from container
        handler = container.get_with_db('get_transaction_handler', db)

        # Execute query
        transaction_view = await handler.handle(query)

        if not transaction_view:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

        # Return response
        return PaymentResponse(
            transaction_id=transaction_view.id,
            status=transaction_view.status,
            blockchain_hash=transaction_view.blockchain_hash,
            estimated_confirmation_time=300,
            gas_fee=transaction_view.fees_paid
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/user/{user_id}/transactions")
async def get_user_transactions(
    user_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user transaction history using query handler.
    Demonstrates pagination and filtering.
    """
    try:
        from app.queries.payment_queries import GetUserTransactionsQuery

        # Create query
        query = GetUserTransactionsQuery(
            user_id=UUID(user_id),
            limit=limit,
            offset=offset
        )

        # Get query handler from container
        handler = container.get_with_db('get_user_transactions_handler', db)

        # Execute query
        transactions = await handler.handle(query)

        return {
            "transactions": [
                {
                    "id": t.id,
                    "amount": t.amount,
                    "currency": t.currency,
                    "status": t.status,
                    "created_at": t.created_at.isoformat(),
                    "recipient_address": t.recipient_address,
                    "fees_paid": t.fees_paid
                }
                for t in transactions
            ],
            "pagination": {
                "limit": limit,
                "offset": offset,
                "count": len(transactions)
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
