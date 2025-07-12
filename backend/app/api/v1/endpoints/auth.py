"""
Authentication endpoints for QPesaPay backend.
Handles user registration, login, and token management.
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.schemas.user import (
    UserCreate, UserResponse, UserLogin, TokenResponse,
    RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm,
    EmailVerificationRequest, PhoneVerificationRequest,
    PasswordChange
)
from app.models.user import User
from app.core.security import (
    create_access_token, create_refresh_token, verify_token,
    verify_password, get_password_hash, get_current_user,
    validate_password_strength
)
from app.core.exceptions import (
    HTTPAuthenticationError, HTTPValidationError, HTTPConflictError,
    HTTPNotFoundError
)
from app.core.logging import security_logger, audit_logger
from app.config import settings

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register_user(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Register a new user account.
    
    Args:
        request: HTTP request
        user_data: User registration data
        db: Database session
        
    Returns:
        UserResponse: Created user data
        
    Raises:
        HTTPConflictError: If email or phone already exists
        HTTPValidationError: If validation fails
    """
    client_ip = get_remote_address(request)
    
    try:
        # Check if user already exists
        existing_user = await User.get_by_email(db, user_data.email)
        if existing_user:
            security_logger.log_suspicious_activity(
                user_id="anonymous",
                activity_type="duplicate_registration_attempt",
                details={"email": user_data.email},
                ip_address=client_ip
            )
            raise HTTPConflictError("Email already registered")
        
        existing_phone = await User.get_by_phone(db, user_data.phone_number)
        if existing_phone:
            raise HTTPConflictError("Phone number already registered")
        
        # Validate password strength
        is_valid, errors = validate_password_strength(user_data.password)
        if not is_valid:
            raise HTTPValidationError(
                f"Password validation failed: {'; '.join(errors)}"
            )
        
        # Create user
        user_dict = user_data.dict(exclude={"password"})
        user_dict["hashed_password"] = get_password_hash(user_data.password)
        
        user = await User.create(db, user_dict)
        
        # Log successful registration
        security_logger.log_login_attempt(
            email=user.email,
            success=True,
            ip_address=client_ip,
            user_agent=request.headers.get("user-agent")
        )
        
        audit_logger.log_user_action(
            user_id=str(user.id),
            action="create",
            resource="user_account",
            details={"account_type": user.account_type.value}
        )
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        security_logger.log_suspicious_activity(
            user_id="anonymous",
            activity_type="registration_error",
            details={"error": str(e), "email": user_data.email},
            ip_address=client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login_user(
    request: Request,
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Authenticate user and return access tokens.
    
    Args:
        request: HTTP request
        user_credentials: Login credentials
        db: Database session
        
    Returns:
        TokenResponse: Access and refresh tokens with user data
        
    Raises:
        HTTPAuthenticationError: If authentication fails
    """
    client_ip = get_remote_address(request)
    user_agent = request.headers.get("user-agent")
    
    try:
        # Get user by email
        user = await User.get_by_email(db, user_credentials.email)
        if not user:
            security_logger.log_login_attempt(
                email=user_credentials.email,
                success=False,
                ip_address=client_ip,
                user_agent=user_agent
            )
            raise HTTPAuthenticationError("Invalid email or password")
        
        # Check if account is locked
        if user.is_locked:
            security_logger.log_suspicious_activity(
                user_id=str(user.id),
                activity_type="login_attempt_locked_account",
                details={"locked_until": user.locked_until.isoformat() if user.locked_until else None},
                ip_address=client_ip
            )
            raise HTTPAuthenticationError("Account is temporarily locked. Please try again later.")
        
        # Verify password
        if not verify_password(user_credentials.password, user.hashed_password):
            # Increment failed login attempts
            user.increment_failed_login_attempts()
            await db.commit()
            
            security_logger.log_login_attempt(
                email=user_credentials.email,
                success=False,
                ip_address=client_ip,
                user_agent=user_agent
            )
            raise HTTPAuthenticationError("Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            security_logger.log_login_attempt(
                email=user_credentials.email,
                success=False,
                ip_address=client_ip,
                user_agent=user_agent
            )
            raise HTTPAuthenticationError("Account is deactivated")
        
        # Update last login
        user.update_last_login(client_ip)
        await db.commit()
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
        refresh_token = create_refresh_token(subject=str(user.id))
        
        # Log successful login
        security_logger.log_login_attempt(
            email=user.email,
            success=True,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        audit_logger.log_user_action(
            user_id=str(user.id),
            action="login",
            resource="user_session",
            details={"ip_address": client_ip}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        security_logger.log_suspicious_activity(
            user_id="anonymous",
            activity_type="login_error",
            details={"error": str(e), "email": user_credentials.email},
            ip_address=client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
async def refresh_access_token(
    request: Request,
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token.
    
    Args:
        request: HTTP request
        refresh_data: Refresh token data
        db: Database session
        
    Returns:
        TokenResponse: New access and refresh tokens
        
    Raises:
        HTTPAuthenticationError: If refresh token is invalid
    """
    client_ip = get_remote_address(request)
    
    try:
        # Verify refresh token
        user_id = verify_token(refresh_data.refresh_token, "refresh")
        if not user_id:
            security_logger.log_suspicious_activity(
                user_id="anonymous",
                activity_type="invalid_refresh_token",
                details={},
                ip_address=client_ip
            )
            raise HTTPAuthenticationError("Invalid refresh token")
        
        # Get user
        from uuid import UUID
        user = await User.get_by_id(db, UUID(user_id))
        if not user or not user.is_active:
            raise HTTPAuthenticationError("User not found or inactive")
        
        # Create new tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
        refresh_token = create_refresh_token(subject=str(user.id))
        
        audit_logger.log_user_action(
            user_id=str(user.id),
            action="refresh_token",
            resource="user_session",
            details={"ip_address": client_ip}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        security_logger.log_suspicious_activity(
            user_id="anonymous",
            activity_type="refresh_token_error",
            details={"error": str(e)},
            ip_address=client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout_user(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Logout user (invalidate tokens).
    
    Args:
        request: HTTP request
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    client_ip = get_remote_address(request)
    
    # TODO: Implement token blacklisting
    # For now, we just log the logout event
    
    audit_logger.log_user_action(
        user_id=str(current_user.id),
        action="logout",
        resource="user_session",
        details={"ip_address": client_ip}
    )
    
    return {"message": "Successfully logged out"}


@router.post("/change-password")
async def change_password(
    request: Request,
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Change user password.
    
    Args:
        request: HTTP request
        password_data: Password change data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPAuthenticationError: If current password is incorrect
        HTTPValidationError: If new password is invalid
    """
    client_ip = get_remote_address(request)
    
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user.hashed_password):
            security_logger.log_suspicious_activity(
                user_id=str(current_user.id),
                activity_type="invalid_password_change_attempt",
                details={},
                ip_address=client_ip
            )
            raise HTTPAuthenticationError("Current password is incorrect")
        
        # Validate new password strength
        is_valid, errors = validate_password_strength(password_data.new_password)
        if not is_valid:
            raise HTTPValidationError(
                f"Password validation failed: {'; '.join(errors)}"
            )
        
        # Update password
        current_user.hashed_password = get_password_hash(password_data.new_password)
        current_user.password_changed_at = datetime.utcnow()
        await db.commit()
        
        # Log password change
        security_logger.log_password_change(
            user_id=str(current_user.id),
            ip_address=client_ip
        )
        
        audit_logger.log_user_action(
            user_id=str(current_user.id),
            action="change_password",
            resource="user_account",
            details={"ip_address": client_ip}
        )
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        security_logger.log_suspicious_activity(
            user_id=str(current_user.id),
            activity_type="password_change_error",
            details={"error": str(e)},
            ip_address=client_ip
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: User profile data
    """
    return UserResponse.from_orm(current_user)


# TODO: Implement additional endpoints
# - Password reset request
# - Password reset confirmation
# - Email verification
# - Phone verification
# - Two-factor authentication setup
# - Two-factor authentication verification