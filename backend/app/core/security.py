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


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token.

    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time

    Returns:
        str: JWT refresh token
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
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

    # Check if token is blacklisted
    if is_token_blacklisted(token):
        raise HTTPAuthenticationError("Token has been revoked")

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

    # Check if account is locked
    if user.is_locked:
        raise HTTPAuthenticationError("Account is temporarily locked due to failed login attempts")

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


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Validate password strength against security policy.

    Args:
        password: Password to validate

    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []

    # Check minimum length
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters long")

    # Check maximum length (prevent DoS)
    if len(password) > 128:
        errors.append("Password must not exceed 128 characters")

    # Check for uppercase letters
    if settings.REQUIRE_PASSWORD_UPPERCASE and not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    # Check for lowercase letters
    if settings.REQUIRE_PASSWORD_LOWERCASE and not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    # Check for numbers
    if settings.REQUIRE_PASSWORD_NUMBERS and not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")

    # Check for special characters
    if settings.REQUIRE_PASSWORD_SPECIAL:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?~`"
        if not any(c in special_chars for c in password):
            errors.append("Password must contain at least one special character")

    # Check for common weak passwords
    weak_passwords = [
        "password", "123456", "qwerty", "admin", "letmein",
        "welcome", "monkey", "dragon", "password123", "qwerty123"
    ]
    if password.lower() in weak_passwords:
        errors.append("Password is too common and easily guessable")

    # Check for sequential characters (only for simple sequences like 123, abc)
    if len(password) >= 4:  # Only check longer sequences
        sequential_found = False
        for i in range(len(password) - 3):  # Check 4+ character sequences
            if (ord(password[i+1]) == ord(password[i]) + 1 and
                ord(password[i+2]) == ord(password[i]) + 2 and
                ord(password[i+3]) == ord(password[i]) + 3):
                sequential_found = True
                break
        if sequential_found:
            errors.append("Password must not contain long sequential characters")

    return len(errors) == 0, errors


# Token blacklist (in production, use Redis)
_token_blacklist = set()


def blacklist_token(token: str) -> None:
    """Add token to blacklist."""
    _token_blacklist.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted."""
    return token in _token_blacklist


def create_tokens(user_id: str) -> dict[str, str]:
    """
    Create both access and refresh tokens.

    Args:
        user_id: User ID to encode in tokens

    Returns:
        dict: Contains access_token and refresh_token
    """
    access_token = create_access_token(
        subject=user_id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_refresh_token(
        subject=user_id,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


def verify_token_not_blacklisted(token: str) -> bool:
    """
    Verify token is not blacklisted.

    Args:
        token: JWT token to check

    Returns:
        bool: True if token is valid and not blacklisted
    """
    if is_token_blacklisted(token):
        return False

    # Verify token is valid
    user_id = verify_token(token, "access")
    return user_id is not None


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