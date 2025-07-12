"""Transaction management endpoints for QPesaPay backend."""

from typing import Any, List, Optional
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.schemas.transaction import (
    TransactionResponse, 
    TransactionCreate, 
    TransactionUpdate,
    TransactionStatus
)
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[TransactionResponse])
async def get_user_transactions(
    skip: int = Query(0, ge=0, description="Number of transactions to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of transactions to return"),
    status: Optional[TransactionStatus] = Query(None, description="Filter by transaction status"),
    wallet_id: Optional[UUID] = Query(None, description="Filter by wallet ID"),
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get transactions for the current user."""
    try:
        # If wallet_id is provided, verify it belongs to the user
        if wallet_id:
            wallet = await Wallet.get_by_id(db, wallet_id)
            if not wallet or wallet.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Wallet not found"
                )
        
        transactions = await Transaction.get_by_user_id(
            db, 
            current_user.id, 
            skip=skip, 
            limit=limit,
            status=status,
            wallet_id=wallet_id
        )
        
        logger.info("User transactions retrieved", extra={
            "user_id": str(current_user.id),
            "transaction_count": len(transactions),
            "skip": skip,
            "limit": limit,
            "status_filter": status.value if status else None,
            "wallet_filter": str(wallet_id) if wallet_id else None
        })
        
        return transactions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get user transactions", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transactions"
        )


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new transaction."""
    try:
        # Verify source wallet belongs to current user
        source_wallet = await Wallet.get_by_id(db, transaction_data.source_wallet_id)
        if not source_wallet or source_wallet.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source wallet not found"
            )
        
        # Check if source wallet is active
        if not source_wallet.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source wallet is not active"
            )
        
        # Check if user has sufficient balance
        available_balance = await source_wallet.get_available_balance(db)
        if available_balance < transaction_data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )
        
        # If destination wallet is provided, verify it exists
        if transaction_data.destination_wallet_id:
            dest_wallet = await Wallet.get_by_id(db, transaction_data.destination_wallet_id)
            if not dest_wallet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Destination wallet not found"
                )
        
        # Create transaction
        transaction = await Transaction.create(db, transaction_data.dict())
        
        logger.info("Transaction created", extra={
            "user_id": str(current_user.id),
            "transaction_id": str(transaction.id),
            "transaction_type": transaction.transaction_type.value,
            "amount": str(transaction.amount),
            "currency": transaction.currency
        })
        
        return transaction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create transaction", extra={
            "user_id": str(current_user.id),
            "transaction_type": transaction_data.transaction_type.value,
            "amount": str(transaction_data.amount),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction"
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific transaction by ID."""
    try:
        transaction = await Transaction.get_by_id(db, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Check if transaction belongs to current user or user is admin
        source_wallet = await Wallet.get_by_id(db, transaction.source_wallet_id)
        dest_wallet = None
        if transaction.destination_wallet_id:
            dest_wallet = await Wallet.get_by_id(db, transaction.destination_wallet_id)
        
        user_owns_transaction = (
            (source_wallet and source_wallet.user_id == current_user.id) or
            (dest_wallet and dest_wallet.user_id == current_user.id)
        )
        
        if not user_owns_transaction and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        return transaction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get transaction", extra={
            "transaction_id": str(transaction_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transaction"
        )


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a transaction (admin only for most fields)."""
    try:
        transaction = await Transaction.get_by_id(db, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Check permissions
        source_wallet = await Wallet.get_by_id(db, transaction.source_wallet_id)
        user_owns_transaction = source_wallet and source_wallet.user_id == current_user.id
        
        # Users can only update their own transactions and only certain fields
        if not current_user.is_admin() and not user_owns_transaction:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Non-admin users can only update description and metadata
        if not current_user.is_admin():
            allowed_fields = {"description", "metadata"}
            update_fields = set(transaction_update.dict(exclude_unset=True).keys())
            if not update_fields.issubset(allowed_fields):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update description and metadata"
                )
        
        updated_transaction = await transaction.update(db, transaction_update)
        
        logger.info("Transaction updated", extra={
            "transaction_id": str(transaction_id),
            "user_id": str(current_user.id),
            "updated_fields": list(transaction_update.dict(exclude_unset=True).keys())
        })
        
        return updated_transaction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update transaction", extra={
            "transaction_id": str(transaction_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update transaction"
        )


@router.post("/{transaction_id}/cancel")
async def cancel_transaction(
    transaction_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Cancel a pending transaction."""
    try:
        transaction = await Transaction.get_by_id(db, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Check if transaction belongs to current user
        source_wallet = await Wallet.get_by_id(db, transaction.source_wallet_id)
        if not source_wallet or source_wallet.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Check if transaction can be cancelled
        if transaction.status != TransactionStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending transactions can be cancelled"
            )
        
        await transaction.cancel(db)
        
        logger.info("Transaction cancelled", extra={
            "transaction_id": str(transaction_id),
            "user_id": str(current_user.id)
        })
        
        return {"message": "Transaction cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to cancel transaction", extra={
            "transaction_id": str(transaction_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel transaction"
        )


@router.get("/{transaction_id}/status", response_model=dict)
async def get_transaction_status(
    transaction_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get transaction status and details."""
    try:
        transaction = await Transaction.get_by_id(db, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        # Check if transaction belongs to current user or user is admin
        source_wallet = await Wallet.get_by_id(db, transaction.source_wallet_id)
        dest_wallet = None
        if transaction.destination_wallet_id:
            dest_wallet = await Wallet.get_by_id(db, transaction.destination_wallet_id)
        
        user_owns_transaction = (
            (source_wallet and source_wallet.user_id == current_user.id) or
            (dest_wallet and dest_wallet.user_id == current_user.id)
        )
        
        if not user_owns_transaction and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        return {
            "transaction_id": str(transaction_id),
            "status": transaction.status.value,
            "created_at": transaction.created_at.isoformat(),
            "updated_at": transaction.updated_at.isoformat(),
            "blockchain_tx_hash": transaction.blockchain_tx_hash,
            "confirmation_count": transaction.confirmation_count,
            "estimated_completion": transaction.estimated_completion.isoformat() if transaction.estimated_completion else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get transaction status", extra={
            "transaction_id": str(transaction_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get transaction status"
        )