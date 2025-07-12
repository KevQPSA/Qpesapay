"""
Security utilities for QPesaPay backend.
Handles JWT tokens, password hashing, and authentication.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from uuid import UUID

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.core.exceptions import HTTPAuthenticationError, HTTPAuthorizationError

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT algorithm
ALGORITHM = "HS256"

# HTTP Bearer token scheme
security = HTTPBearer()


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token.
    
    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time
        
    Returns:
        str: JWT token
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    Create JWT refresh token.
    
    Args:
        subject: Token subject (usually user ID)
        
    Returns:
        str: JWT refresh token
    """
    expire = datetime.now(timezone.utc) + timedelta(days=30)  # 30 days for refresh token
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    Verify JWT token and return subject.
    
    Args:
        token: JWT token
        token_type: Expected token type (access or refresh)
        
    Returns:
        str: Token subject if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        token_type_claim: str = payload.get("type")
        
        if user_id is None or token_type_claim != token_type:
            return None
            
        return user_id
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash password.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        User: Current user
        
    Raises:
        HTTPAuthenticationError: If authentication fails
    """
    token = credentials.credentials
    user_id = verify_token(token, "access")
    
    if user_id is None:
        raise HTTPAuthenticationError("Invalid authentication credentials")
    
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPAuthenticationError("Invalid user ID format")
    
    user = await User.get_by_id(db, user_uuid)
    if user is None:
        raise HTTPAuthenticationError("User not found")
    
    if not user.is_active:
        raise HTTPAuthenticationError("User account is inactive")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        User: Active user
        
    Raises:
        HTTPAuthenticationError: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPAuthenticationError("User account is inactive")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current admin user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        User: Admin user
        
    Raises:
        HTTPAuthorizationError: If user is not admin
    """
    if not current_user.is_admin():
        raise HTTPAuthorizationError("Admin privileges required")
    return current_user


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        bool: True if password is strong enough
    """
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    return has_upper and has_lower and has_digit and has_special


def generate_api_key() -> str:
    """
    Generate secure API key.
    
    Returns:
        str: API key
    """
    import secrets
    return f"qpay_{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str) -> str:
    """
    Hash API key for storage.
    
    Args:
        api_key: API key to hash
        
    Returns:
        str: Hashed API key
    """
    return pwd_context.hash(api_key)


def verify_api_key(api_key: str, hashed_api_key: str) -> bool:
    """
    Verify API key against hash.
    
    Args:
        api_key: Plain API key
        hashed_api_key: Hashed API key
        
    Returns:
        bool: True if API key matches
    """
    return pwd_context.verify(api_key, hashed_api_key)