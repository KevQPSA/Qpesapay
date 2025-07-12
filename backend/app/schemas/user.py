"""
User schemas for QPesaPay backend.
Pydantic models for user-related API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID
import re

from app.models.user import AccountType, KYCStatus
from app.core.validation import (
    validate_email_address, validate_phone_number,
    sanitize_string, validate_password, ValidationError
)


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email address")
    phone_number: str = Field(..., min_length=10, max_length=20, description="Phone number")
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name")
    
    @validator('email')
    def validate_email(cls, v):
        """Validate email address using secure validation."""
        try:
            return validate_email_address(v)
        except ValidationError as e:
            raise ValueError(str(e))

    @validator('phone_number')
    def validate_phone(cls, v):
        """Validate phone number using secure validation."""
        try:
            return validate_phone_number(v, "KE")
        except ValidationError as e:
            raise ValueError(str(e))
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Validate name fields using secure sanitization."""
        if v is None:
            return v
        try:
            return sanitize_string(v, max_length=100)
        except ValidationError as e:
            raise ValueError(str(e))
        
        # Remove extra whitespace
        name = v.strip()
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        
        return name


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=12, max_length=128, description="User password")
    account_type: AccountType = Field(default=AccountType.PERSONAL, description="Account type")
    preferred_language: str = Field(default="en", description="Preferred language")
    preferred_currency: str = Field(default="KES", description="Preferred currency")

    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password using secure validation."""
        try:
            return validate_password(v)
        except ValidationError as e:
            raise ValueError(str(e))
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', v):
            raise ValueError('Password must contain at least one special character')
        
        return v
    
    @validator('preferred_language')
    def validate_language(cls, v):
        """Validate language code."""
        valid_languages = ['en', 'sw']  # English, Swahili
        if v not in valid_languages:
            raise ValueError(f'Language must be one of: {", ".join(valid_languages)}')
        return v
    
    @validator('preferred_currency')
    def validate_currency(cls, v):
        """Validate currency code."""
        valid_currencies = ['KES', 'USD', 'BTC', 'USDT']
        if v not in valid_currencies:
            raise ValueError(f'Currency must be one of: {", ".join(valid_currencies)}')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    preferred_language: Optional[str] = None
    preferred_currency: Optional[str] = None
    notification_preferences: Optional[Dict[str, bool]] = None
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        if v is None:
            return v
        return UserBase.validate_phone_number(v)
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        """Validate date of birth."""
        if v is None:
            return v
        
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age < 18:
            raise ValueError('User must be at least 18 years old')
        
        if age > 120:
            raise ValueError('Invalid date of birth')
        
        return v


class UserKYCUpdate(BaseModel):
    """Schema for updating KYC information."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date = Field(..., description="Date of birth")
    nationality: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=10, max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    id_number: str = Field(..., min_length=5, max_length=50, description="National ID number")
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        """Validate date of birth for KYC."""
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age < 18:
            raise ValueError('Must be at least 18 years old for KYC verification')
        
        if age > 120:
            raise ValueError('Invalid date of birth')
        
        return v
    
    @validator('id_number')
    def validate_id_number(cls, v):
        """Validate ID number format."""
        # Remove any spaces or special characters
        id_num = re.sub(r'[^\d]', '', v)
        
        # Kenya national ID is typically 8 digits
        if len(id_num) < 7 or len(id_num) > 10:
            raise ValueError('Invalid ID number format')
        
        return id_num


class PasswordChange(BaseModel):
    """Schema for password change."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        return UserCreate.validate_password(v)
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        """Validate password confirmation."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")
    remember_me: bool = Field(default=False, description="Remember login")


class UserResponse(BaseModel):
    """Schema for user response data."""
    id: UUID
    email: EmailStr
    phone_number: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str
    account_type: str
    kyc_status: str
    is_active: bool
    is_verified: bool
    email_verified: bool
    phone_verified: bool
    is_fully_verified: bool
    profile_image_url: Optional[str]
    preferred_language: str
    preferred_currency: str
    country: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    """Extended user profile with additional information."""
    date_of_birth: Optional[date]
    nationality: Optional[str]
    address: Optional[str]
    city: Optional[str]
    two_factor_enabled: bool
    last_login_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserList(BaseModel):
    """Schema for paginated user list."""
    users: list[UserResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str = Field(..., description="Refresh token")


class EmailVerificationRequest(BaseModel):
    """Schema for email verification request."""
    email: EmailStr = Field(..., description="Email to verify")


class PhoneVerificationRequest(BaseModel):
    """Schema for phone verification request."""
    phone_number: str = Field(..., description="Phone number to verify")
    verification_code: str = Field(..., min_length=4, max_length=6, description="Verification code")


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr = Field(..., description="User email")


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        return UserCreate.validate_password(v)
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        """Validate password confirmation."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class TwoFactorSetup(BaseModel):
    """Schema for two-factor authentication setup."""
    password: str = Field(..., description="Current password for verification")


class TwoFactorConfirm(BaseModel):
    """Schema for two-factor authentication confirmation."""
    code: str = Field(..., min_length=6, max_length=6, description="2FA code")


class TwoFactorDisable(BaseModel):
    """Schema for disabling two-factor authentication."""
    password: str = Field(..., description="Current password for verification")
    code: str = Field(..., min_length=6, max_length=6, description="2FA code")