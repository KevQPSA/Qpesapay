"""User management endpoints for QPesaPay backend."""

from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserKYCUpdate
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(User.get_current_user)
) -> Any:
    """Get current user profile."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update current user profile."""
    try:
        updated_user = await current_user.update(db, user_update)
        
        logger.info("User profile updated", extra={
            "user_id": str(current_user.id),
            "updated_fields": list(user_update.dict(exclude_unset=True).keys())
        })
        
        return updated_user
        
    except Exception as e:
        logger.error("Failed to update user profile", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.put("/me/kyc", response_model=UserResponse)
async def update_kyc_information(
    kyc_update: UserKYCUpdate,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update user KYC information."""
    try:
        updated_user = await current_user.update_kyc(db, kyc_update)
        
        logger.info("User KYC information updated", extra={
            "user_id": str(current_user.id),
            "kyc_status": updated_user.kyc_status.value
        })
        
        return updated_user
        
    except Exception as e:
        logger.error("Failed to update KYC information", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update KYC information"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get user by ID (admin only or own profile)."""
    try:
        # Check if user is trying to access their own profile
        if user_id == current_user.id:
            return current_user
        
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        user = await User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get user by ID", extra={
            "user_id": str(user_id),
            "requester_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List users (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        users = await User.get_multi(db, skip=skip, limit=limit)
        
        logger.info("Users listed", extra={
            "requester_id": str(current_user.id),
            "count": len(users),
            "skip": skip,
            "limit": limit
        })
        
        return users
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list users", extra={
            "requester_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users"
        )


@router.delete("/me")
async def deactivate_current_user(
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Deactivate current user account."""
    try:
        await current_user.deactivate(db)
        
        logger.info("User account deactivated", extra={
            "user_id": str(current_user.id)
        })
        
        return {"message": "Account deactivated successfully"}
        
    except Exception as e:
        logger.error("Failed to deactivate user account", extra={
            "user_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate account"
        )


@router.put("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: UUID,
    current_user: User = Depends(User.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Activate user account (admin only)."""
    try:
        # Check if user has admin privileges
        if not current_user.is_admin():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        user = await User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        activated_user = await user.activate(db)
        
        logger.info("User account activated", extra={
            "user_id": str(user_id),
            "admin_id": str(current_user.id)
        })
        
        return activated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to activate user account", extra={
            "user_id": str(user_id),
            "admin_id": str(current_user.id),
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate user account"
        )