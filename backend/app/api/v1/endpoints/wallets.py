"""Wallet management endpoints for QPesaPay backend."""

from typing import Any, List
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.wallet import Wallet
from app.schemas.wallet import WalletResponse, WalletCreate, WalletUpdate
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[WalletResponse])
async def get_user_wallets(
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get all wallets for the current user."""
    try:
        wallets = await Wallet.get_by_user_id(db, current_user.id)
        
        logger.info("User wallets retrieved", extra={
            "user_id": str(current_user.id),
            "wallet_count": len(wallets)
        })
        
        return wallets
        
    except Exception as e:
        logger.error("Failed to get user wallets", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get wallets"
        )


@router.post("/", response_model=WalletResponse, status_code=status.HTTP_201_CREATED)
async def create_wallet(
    wallet_data: WalletCreate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new wallet for the current user."""
    try:
        # Check if user already has a wallet for this currency
        existing_wallet = await Wallet.get_by_user_and_currency(
            db, current_user.id, wallet_data.currency
        )
        if existing_wallet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Wallet for {wallet_data.currency} already exists"
            )
        
        # Create wallet data with user_id
        wallet_create_data = wallet_data.dict()
        wallet_create_data["user_id"] = current_user.id
        
        wallet = await Wallet.create(db, wallet_create_data)
        
        logger.info("Wallet created", extra={
            "user_id": str(current_user.id),
            "wallet_id": str(wallet.id),
            "currency": wallet.currency,
            "wallet_type": wallet.wallet_type.value
        })
        
        return wallet
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create wallet", extra={
            "user_id": str(current_user.id),
            "currency": wallet_data.currency,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create wallet"
        )


@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(
    wallet_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific wallet by ID."""
    try:
        wallet = await Wallet.get_by_id(db, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        # Check if wallet belongs to current user or user is admin
        if wallet.user_id != current_user.id and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        return wallet
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get wallet", extra={
            "wallet_id": str(wallet_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get wallet"
        )


@router.put("/{wallet_id}", response_model=WalletResponse)
async def update_wallet(
    wallet_id: UUID,
    wallet_update: WalletUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a wallet."""
    try:
        wallet = await Wallet.get_by_id(db, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        # Check if wallet belongs to current user
        if wallet.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        updated_wallet = await wallet.update(db, wallet_update)
        
        logger.info("Wallet updated", extra={
            "wallet_id": str(wallet_id),
            "user_id": str(current_user.id),
            "updated_fields": list(wallet_update.dict(exclude_unset=True).keys())
        })
        
        return updated_wallet
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update wallet", extra={
            "wallet_id": str(wallet_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update wallet"
        )


@router.get("/{wallet_id}/balance", response_model=dict)
async def get_wallet_balance(
    wallet_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get wallet balance."""
    try:
        wallet = await Wallet.get_by_id(db, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        # Check if wallet belongs to current user or user is admin
        if wallet.user_id != current_user.id and not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        balance = await wallet.get_balance(db)
        
        return {
            "wallet_id": str(wallet_id),
            "currency": wallet.currency,
            "balance": str(balance),
            "available_balance": str(wallet.available_balance),
            "pending_balance": str(wallet.pending_balance)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get wallet balance", extra={
            "wallet_id": str(wallet_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get wallet balance"
        )


@router.post("/{wallet_id}/freeze")
async def freeze_wallet(
    wallet_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Freeze a wallet (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        wallet = await Wallet.get_by_id(db, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        await wallet.freeze(db)
        
        logger.info("Wallet frozen", extra={
            "wallet_id": str(wallet_id),
            "admin_id": str(current_user.id)
        })
        
        return {"message": "Wallet frozen successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to freeze wallet", extra={
            "wallet_id": str(wallet_id),
            "admin_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to freeze wallet"
        )


@router.post("/{wallet_id}/unfreeze")
async def unfreeze_wallet(
    wallet_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Unfreeze a wallet (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        wallet = await Wallet.get_by_id(db, wallet_id)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        await wallet.unfreeze(db)
        
        logger.info("Wallet unfrozen", extra={
            "wallet_id": str(wallet_id),
            "admin_id": str(current_user.id)
        })
        
        return {"message": "Wallet unfrozen successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to unfreeze wallet", extra={
            "wallet_id": str(wallet_id),
            "admin_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unfreeze wallet"
        )