"""Merchant management endpoints for QPesaPay backend."""

from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.merchant import Merchant
from app.schemas.merchant import (
    MerchantResponse, 
    MerchantCreate, 
    MerchantUpdate,
    MerchantSettings,
    MerchantSettingsUpdate,
    MerchantStats,
    APIKeyCreate,
    APIKeyResponse
)
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=List[MerchantResponse])
async def get_user_merchants(
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get all merchants for the current user."""
    try:
        merchants = await Merchant.get_by_user_id(db, current_user.id)
        
        logger.info("User merchants retrieved", extra={
            "user_id": str(current_user.id),
            "merchant_count": len(merchants)
        })
        
        return merchants
        
    except Exception as e:
        logger.error("Failed to get user merchants", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get merchants"
        )


@router.post("/", response_model=MerchantResponse, status_code=status.HTTP_201_CREATED)
async def create_merchant(
    merchant_data: MerchantCreate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new merchant account."""
    try:
        # Check if user already has a merchant account with the same business name
        existing_merchant = await Merchant.get_by_user_and_business_name(
            db, current_user.id, merchant_data.business_name
        )
        if existing_merchant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Merchant account with this business name already exists"
            )
        
        # Create merchant data with user_id
        merchant_create_data = merchant_data.dict()
        merchant_create_data["user_id"] = current_user.id
        
        merchant = await Merchant.create(db, merchant_create_data)
        
        logger.info("Merchant created", extra={
            "user_id": str(current_user.id),
            "merchant_id": str(merchant.id),
            "business_name": merchant.business_name,
            "merchant_type": merchant.merchant_type.value
        })
        
        return merchant
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create merchant", extra={
            "user_id": str(current_user.id),
            "business_name": merchant_data.business_name,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create merchant"
        )


@router.get("/{merchant_id}", response_model=MerchantResponse)
async def get_merchant(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific merchant by ID."""
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
        
        return merchant
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get merchant", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get merchant"
        )


@router.put("/{merchant_id}", response_model=MerchantResponse)
async def update_merchant(
    merchant_id: UUID,
    merchant_update: MerchantUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a merchant."""
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
        
        updated_merchant = await merchant.update(db, merchant_update)
        
        logger.info("Merchant updated", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "updated_fields": list(merchant_update.dict(exclude_unset=True).keys())
        })
        
        return updated_merchant
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update merchant", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update merchant"
        )


@router.get("/{merchant_id}/stats", response_model=MerchantStats)
async def get_merchant_stats(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get merchant statistics."""
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
        
        stats = await merchant.get_stats(db)
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get merchant stats", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get merchant stats"
        )


@router.get("/{merchant_id}/settings", response_model=MerchantSettings)
async def get_merchant_settings(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get merchant settings."""
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
        
        settings = await merchant.get_settings(db)
        
        return settings
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get merchant settings", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get merchant settings"
        )


@router.put("/{merchant_id}/settings", response_model=MerchantSettings)
async def update_merchant_settings(
    merchant_id: UUID,
    settings_update: MerchantSettingsUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update merchant settings."""
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
        
        updated_settings = await merchant.update_settings(db, settings_update)
        
        logger.info("Merchant settings updated", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "updated_fields": list(settings_update.dict(exclude_unset=True).keys())
        })
        
        return updated_settings
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update merchant settings", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update merchant settings"
        )


@router.post("/{merchant_id}/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    merchant_id: UUID,
    api_key_data: APIKeyCreate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new API key for the merchant."""
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
        
        api_key = await merchant.create_api_key(db, api_key_data)
        
        logger.info("API key created", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "api_key_name": api_key_data.name
        })
        
        return api_key
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create API key", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key"
        )


@router.get("/{merchant_id}/api-keys", response_model=List[APIKeyResponse])
async def get_api_keys(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get all API keys for the merchant."""
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
        
        api_keys = await merchant.get_api_keys(db)
        
        return api_keys
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get API keys", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get API keys"
        )


@router.delete("/{merchant_id}/api-keys/{api_key_id}")
async def revoke_api_key(
    merchant_id: UUID,
    api_key_id: str,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Revoke an API key."""
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
        
        await merchant.revoke_api_key(db, api_key_id)
        
        logger.info("API key revoked", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "api_key_id": api_key_id
        })
        
        return {"message": "API key revoked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to revoke API key", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "api_key_id": api_key_id,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke API key"
        )


@router.post("/{merchant_id}/activate", response_model=MerchantResponse)
async def activate_merchant(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Activate a merchant account (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        merchant = await Merchant.get_by_id(db, merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found"
            )
        
        activated_merchant = await merchant.activate(db)
        
        logger.info("Merchant activated", extra={
            "merchant_id": str(merchant_id),
            "admin_id": str(current_user.id)
        })
        
        return activated_merchant
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to activate merchant", extra={
            "merchant_id": str(merchant_id),
            "admin_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate merchant"
        )


@router.post("/{merchant_id}/deactivate")
async def deactivate_merchant(
    merchant_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Deactivate a merchant account."""
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
        
        await merchant.deactivate(db)
        
        logger.info("Merchant deactivated", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id)
        })
        
        return {"message": "Merchant deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to deactivate merchant", extra={
            "merchant_id": str(merchant_id),
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate merchant"
        )