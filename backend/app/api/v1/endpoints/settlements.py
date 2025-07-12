"""Settlement management endpoints for QPesaPay backend."""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.merchant import Merchant
from app.models.settlement import Settlement
from app.schemas.settlement import (
    SettlementResponse, 
    SettlementCreate, 
    SettlementUpdate,
    SettlementBatch,
    SettlementBatchResponse,
    SettlementStats,
    SettlementSchedule,
    SettlementScheduleUpdate,
    BankAccount,
    BankAccountUpdate
)
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[SettlementResponse])
async def get_user_settlements(
    skip: int = Query(0, ge=0, description="Number of settlements to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of settlements to return"),
    merchant_id: Optional[UUID] = Query(None, description="Filter by merchant ID"),
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get settlements for the current user's merchants."""
    try:
        # If merchant_id is provided, verify it belongs to the user
        if merchant_id:
            merchant = await Merchant.get_by_id(db, merchant_id)
            if not merchant or merchant.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Merchant not found"
                )
        
        settlements = await Settlement.get_by_user_id(
            db, 
            current_user.id, 
            skip=skip, 
            limit=limit,
            merchant_id=merchant_id
        )
        
        logger.info("User settlements retrieved", extra={
            "user_id": str(current_user.id),
            "settlement_count": len(settlements),
            "skip": skip,
            "limit": limit,
            "merchant_filter": str(merchant_id) if merchant_id else None
        })
        
        return settlements
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get user settlements", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get settlements"
        )


@router.post("/", response_model=SettlementResponse, status_code=status.HTTP_201_CREATED)
async def create_settlement(
    settlement_data: SettlementCreate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new settlement."""
    try:
        # Verify merchant belongs to current user
        merchant = await Merchant.get_by_id(db, settlement_data.merchant_id)
        if not merchant or merchant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        # Check if merchant is active
        if not merchant.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Merchant is not active"
            )
        
        # Check if merchant has sufficient balance for settlement
        available_balance = await merchant.get_available_balance(db)
        total_amount = settlement_data.amount + settlement_data.fee
        if available_balance < total_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient merchant balance for settlement"
            )
        
        # Create settlement
        settlement = await Settlement.create(db, settlement_data.dict())
        
        logger.info("Settlement created", extra={
            "user_id": str(current_user.id),
            "settlement_id": str(settlement.id),
            "merchant_id": str(settlement.merchant_id),
            "amount": str(settlement.amount),
            "currency": settlement.currency
        })
        
        return settlement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create settlement", extra={
            "user_id": str(current_user.id),
            "merchant_id": str(settlement_data.merchant_id),
            "amount": str(settlement_data.amount),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create settlement"
        )


@router.get("/{settlement_id}", response_model=SettlementResponse)
async def get_settlement(
    settlement_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific settlement by ID."""
    try:
        settlement = await Settlement.get_by_id(db, settlement_id)
        if not settlement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settlement not found"
            )
        
        # Check if settlement belongs to current user's merchant or user is admin
        merchant = await Merchant.get_by_id(db, settlement.merchant_id)
        if not merchant or (merchant.user_id != current_user.id and not current_user.is_admin()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        return settlement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get settlement", extra={
            "settlement_id": str(settlement_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get settlement"
        )


@router.put("/{settlement_id}", response_model=SettlementResponse)
async def update_settlement(
    settlement_id: UUID,
    settlement_update: SettlementUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a settlement (limited fields)."""
    try:
        settlement = await Settlement.get_by_id(db, settlement_id)
        if not settlement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settlement not found"
            )
        
        # Check if settlement belongs to current user's merchant or user is admin
        merchant = await Merchant.get_by_id(db, settlement.merchant_id)
        if not merchant or (merchant.user_id != current_user.id and not current_user.is_admin()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Check if settlement can be updated
        if settlement.status not in ["PENDING", "PROCESSING"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Settlement cannot be updated in current status"
            )
        
        updated_settlement = await settlement.update(db, settlement_update)
        
        logger.info("Settlement updated", extra={
            "settlement_id": str(settlement_id),
            "user_id": str(current_user.id),
            "updated_fields": list(settlement_update.dict(exclude_unset=True).keys())
        })
        
        return updated_settlement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update settlement", extra={
            "settlement_id": str(settlement_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update settlement"
        )


@router.post("/batch", response_model=SettlementBatchResponse, status_code=status.HTTP_201_CREATED)
async def create_settlement_batch(
    batch_data: SettlementBatch,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a batch of settlements (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Verify all merchants exist and are active
        merchants = []
        for merchant_id in batch_data.merchant_ids:
            merchant = await Merchant.get_by_id(db, merchant_id)
            if not merchant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Merchant {merchant_id} not found"
                )
            if not merchant.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Merchant {merchant_id} is not active"
                )
            merchants.append(merchant)
        
        # Create batch settlements
        batch_result = await Settlement.create_batch(db, batch_data, merchants)
        
        logger.info("Settlement batch created", extra={
            "admin_id": str(current_user.id),
            "batch_id": batch_result.batch_id,
            "merchant_count": len(batch_data.merchant_ids),
            "total_settlements": batch_result.total_settlements
        })
        
        return batch_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create settlement batch", extra={
            "admin_id": str(current_user.id),
            "merchant_count": len(batch_data.merchant_ids),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create settlement batch"
        )


@router.get("/merchant/{merchant_id}/stats", response_model=SettlementStats)
async def get_merchant_settlement_stats(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get settlement statistics for a merchant."""
    try:
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        # Check if merchant belongs to current user or user is admin
        if merchant.user_id != current_user.id and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        stats = await Settlement.get_merchant_stats(db, merchant_id)
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get merchant settlement stats", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get settlement stats"
        )


@router.get("/merchant/{merchant_id}/schedule", response_model=SettlementSchedule)
async def get_settlement_schedule(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get settlement schedule for a merchant."""
    try:
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        # Check if merchant belongs to current user
        if merchant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        schedule = await merchant.get_settlement_schedule(db)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settlement schedule not found"
            )
        
        return schedule
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get settlement schedule", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get settlement schedule"
        )


@router.put("/merchant/{merchant_id}/schedule", response_model=SettlementSchedule)
async def update_settlement_schedule(
    merchant_id: UUID,
    schedule_update: SettlementScheduleUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update settlement schedule for a merchant."""
    try:
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        # Check if merchant belongs to current user
        if merchant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        updated_schedule = await merchant.update_settlement_schedule(db, schedule_update)
        
        logger.info("Settlement schedule updated", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "updated_fields": list(schedule_update.dict(exclude_unset=True).keys())
        })
        
        return updated_schedule
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update settlement schedule", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update settlement schedule"
        )


@router.get("/merchant/{merchant_id}/bank-account", response_model=BankAccount)
async def get_bank_account(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get bank account information for a merchant."""
    try:
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        # Check if merchant belongs to current user
        if merchant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        bank_account = await merchant.get_bank_account(db)
        if not bank_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank account not found"
            )
        
        return bank_account
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get bank account", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get bank account"
        )


@router.put("/merchant/{merchant_id}/bank-account", response_model=BankAccount)
async def update_bank_account(
    merchant_id: UUID,
    bank_account_update: BankAccountUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update bank account information for a merchant."""
    try:
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        # Check if merchant belongs to current user
        if merchant.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        updated_bank_account = await merchant.update_bank_account(db, bank_account_update)
        
        logger.info("Bank account updated", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "updated_fields": list(bank_account_update.dict(exclude_unset=True).keys())
        })
        
        return updated_bank_account
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update bank account", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update bank account"
        )


@router.post("/{settlement_id}/process")
async def process_settlement(
    settlement_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Process a pending settlement (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        settlement = await Settlement.get_by_id(db, settlement_id)
        if not settlement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settlement not found"
            )
        
        # Check if settlement can be processed
        if settlement.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending settlements can be processed"
            )
        
        await settlement.process(db)
        
        logger.info("Settlement processed", extra={
            "settlement_id": str(settlement_id),
            "admin_id": str(current_user.id)
        })
        
        return {"message": "Settlement processing initiated"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to process settlement", extra={
            "settlement_id": str(settlement_id),
            "admin_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process settlement"
        )


@router.post("/{settlement_id}/cancel")
async def cancel_settlement(
    settlement_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Cancel a pending settlement."""
    try:
        settlement = await Settlement.get_by_id(db, settlement_id)
        if not settlement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settlement not found"
            )
        
        # Check if settlement belongs to current user's merchant or user is admin
        merchant = await Merchant.get_by_id(db, settlement.merchant_id)
        if not merchant or (merchant.user_id != current_user.id and not current_user.is_admin()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        # Check if settlement can be cancelled
        if settlement.status not in ["PENDING", "PROCESSING"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Settlement cannot be cancelled in current status"
            )
        
        await settlement.cancel(db)
        
        logger.info("Settlement cancelled", extra={
            "settlement_id": str(settlement_id),
            "user_id": str(current_user.id)
        })
        
        return {"message": "Settlement cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to cancel settlement", extra={
            "settlement_id": str(settlement_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel settlement"
        )