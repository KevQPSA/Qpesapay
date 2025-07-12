"""
User model for QPesaPay backend.
Handles user accounts with proper relationships and validation.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum, Index, Text, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid
import enum
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any

from app.models.base import Base


class AccountType(str, enum.Enum):
    """User account types."""
    PERSONAL = "personal"
    MERCHANT = "merchant"
    ADMIN = "admin"


class KYCStatus(str, enum.Enum):
    """KYC verification status."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class User(Base):
    """
    User model for authentication and account management.
    
    Supports both personal and merchant accounts with proper KYC tracking.
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Contact information
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    
    # Account configuration
    account_type = Column(Enum(AccountType), nullable=False, default=AccountType.PERSONAL)
    kyc_status = Column(Enum(KYCStatus), nullable=False, default=KYCStatus.PENDING)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    
    # Security settings
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(32), nullable=True)
    
    # Profile information
    profile_image_url = Column(String(500), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    nationality = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), default="Kenya", nullable=False)
    
    # Preferences
    preferred_language = Column(String(10), default="en", nullable=False)
    preferred_currency = Column(String(10), default="KES", nullable=False)
    notification_preferences = Column(Text, nullable=True)  # JSON string
    
    # Security tracking
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(45), nullable=True)  # IPv6 compatible
    failed_login_attempts = Column(Integer, default=0, nullable=False)  # FIXED: Was String, now Integer
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)

    # Additional security fields
    login_attempts_reset_at = Column(DateTime(timezone=True), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    email_verification_token = Column(String(255), nullable=True)
    email_verification_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    merchant_profile = relationship("Merchant", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Indexes and constraints for performance and security
    __table_args__ = (
        # Performance indexes
        Index('idx_users_email_active', 'email', 'is_active'),
        Index('idx_users_phone_active', 'phone_number', 'is_active'),
        Index('idx_users_account_type', 'account_type'),
        Index('idx_users_kyc_status', 'kyc_status'),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_last_login', 'last_login_at'),

        # Security indexes
        Index('idx_users_failed_attempts', 'failed_login_attempts'),
        Index('idx_users_locked_until', 'locked_until'),
        Index('idx_users_password_reset', 'password_reset_token'),
        Index('idx_users_email_verification', 'email_verification_token'),

        # Security constraints
        CheckConstraint('failed_login_attempts >= 0', name='check_failed_attempts_positive'),
        CheckConstraint('failed_login_attempts <= 10', name='check_failed_attempts_max'),
        CheckConstraint("email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name='check_email_format'),
        CheckConstraint("phone_number ~ '^(\\+254|254|0)[17]\\d{8}$'", name='check_kenya_phone_format'),
        CheckConstraint("LENGTH(hashed_password) >= 60", name='check_password_hash_length'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, account_type={self.account_type})>"

    # Security properties
    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if self.locked_until is None:
            return False
        return datetime.now(timezone.utc) < self.locked_until

    @property
    def is_fully_verified(self) -> bool:
        """Check if user is fully verified (email + phone + KYC)."""
        return (
            self.email_verified and
            self.phone_verified and
            self.kyc_status == KYCStatus.APPROVED
        )

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return "Unknown User"

    # Security methods
    def increment_failed_login_attempts(self) -> None:
        """Increment failed login attempts and lock account if necessary."""
        self.failed_login_attempts += 1

        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            # Progressive lockout: 15 min, 30 min, 1 hour, 2 hours, 24 hours
            lockout_minutes = min(15 * (2 ** (self.failed_login_attempts - 5)), 1440)  # Max 24 hours
            self.locked_until = datetime.now(timezone.utc) + timedelta(minutes=lockout_minutes)

    def reset_failed_login_attempts(self) -> None:
        """Reset failed login attempts after successful login."""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.login_attempts_reset_at = datetime.now(timezone.utc)

    def update_last_login(self, ip_address: str) -> None:
        """Update last login information."""
        self.last_login_at = datetime.now(timezone.utc)
        self.last_login_ip = ip_address
        self.reset_failed_login_attempts()

    def set_password_reset_token(self, token: str, expires_in_minutes: int = 30) -> None:
        """Set password reset token with expiration."""
        self.password_reset_token = token
        self.password_reset_expires = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)

    def clear_password_reset_token(self) -> None:
        """Clear password reset token after use."""
        self.password_reset_token = None
        self.password_reset_expires = None
        self.password_changed_at = datetime.now(timezone.utc)

    def is_password_reset_token_valid(self, token: str) -> bool:
        """Check if password reset token is valid and not expired."""
        if not self.password_reset_token or not self.password_reset_expires:
            return False
        if datetime.now(timezone.utc) > self.password_reset_expires:
            return False
        return self.password_reset_token == token
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email.split('@')[0]
    
    @property
    def is_deleted(self) -> bool:
        """Check if user is soft deleted."""
        return self.deleted_at is not None
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is locked."""
        if not self.locked_until:
            return False
        return datetime.now(datetime.timezone.utc) < self.locked_until
    
    @property
    def is_fully_verified(self) -> bool:
        """Check if user is fully verified."""
        return (
            self.is_verified and
            self.email_verified and
            self.phone_verified and
            self.kyc_status == KYCStatus.APPROVED
        )
    
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.account_type == AccountType.ADMIN
    
    def is_merchant(self) -> bool:
        """Check if user is a merchant."""
        return self.account_type == AccountType.MERCHANT
    
    def is_personal(self) -> bool:
        """Check if user is a personal account."""
        return self.account_type == AccountType.PERSONAL
    
    def can_access_admin_panel(self) -> bool:
        """Check if user can access admin panel."""
        return self.is_admin() and self.is_active and not self.is_deleted
    
    def can_create_merchant_account(self) -> bool:
        """Check if user can create merchant account."""
        return (
            self.is_personal() and
            self.is_fully_verified and
            self.is_active and
            not self.is_deleted
        )
    
    def increment_failed_login_attempts(self):
        """Increment failed login attempts and lock if necessary."""
        current_attempts = int(self.failed_login_attempts)
        current_attempts += 1
        self.failed_login_attempts = str(current_attempts)
        
        # Lock account after 5 failed attempts for 30 minutes
        if current_attempts >= 5:
            self.locked_until = datetime.now(datetime.timezone.utc) + timedelta(minutes=30)
    
    def reset_failed_login_attempts(self):
        """Reset failed login attempts after successful login."""
        self.failed_login_attempts = "0"
        self.locked_until = None
        self.last_login_at = datetime.now(datetime.timezone.utc)
    
    def update_last_login(self, ip_address: str):
        """Update last login information."""
        self.last_login_at = datetime.now(datetime.timezone.utc)
        self.last_login_ip = ip_address
        self.reset_failed_login_attempts()
    
    def soft_delete(self):
        """Soft delete the user account."""
        self.deleted_at = datetime.now(datetime.timezone.utc)
        self.is_active = False
    
    def restore(self):
        """Restore soft deleted user account."""
        self.deleted_at = None
        self.is_active = True
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert user to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            dict: User data
        """
        data = {
            "id": str(self.id),
            "email": self.email,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "account_type": self.account_type.value,
            "kyc_status": self.kyc_status.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "email_verified": self.email_verified,
            "phone_verified": self.phone_verified,
            "is_fully_verified": self.is_fully_verified,
            "profile_image_url": self.profile_image_url,
            "preferred_language": self.preferred_language,
            "preferred_currency": self.preferred_currency,
            "country": self.country,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_sensitive:
            data.update({
                "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
                "nationality": self.nationality,
                "address": self.address,
                "city": self.city,
                "two_factor_enabled": self.two_factor_enabled,
                "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
                "last_login_ip": self.last_login_ip,
                "failed_login_attempts": self.failed_login_attempts,
                "is_locked": self.is_locked,
                "locked_until": self.locked_until.isoformat() if self.locked_until else None,
            })
        
        return data
    
    # Class methods for database operations
    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: uuid.UUID) -> Optional["User"]:
        """Get user by ID."""
        result = await db.execute(select(cls).filter(cls.id == user_id, cls.deleted_at.is_(None)))
        return result.scalars().first()
    
    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> Optional["User"]:
        """Get user by email."""
        result = await db.execute(select(cls).filter(cls.email == email, cls.deleted_at.is_(None)))
        return result.scalars().first()
    
    @classmethod
    async def get_by_phone(cls, db: AsyncSession, phone_number: str) -> Optional["User"]:
        """Get user by phone number."""
        result = await db.execute(select(cls).filter(cls.phone_number == phone_number, cls.deleted_at.is_(None)))
        return result.scalars().first()
    
    @classmethod
    async def create(cls, db: AsyncSession, user_data: Dict[str, Any]) -> "User":
        """Create new user."""
        user = cls(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @classmethod
    async def get_multi(
        cls, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        account_type: Optional[AccountType] = None,
        kyc_status: Optional[KYCStatus] = None,
        is_active: Optional[bool] = None
    ) -> List["User"]:
        """Get multiple users with filters."""
        query = select(cls).filter(cls.deleted_at.is_(None))
        
        if account_type:
            query = query.filter(cls.account_type == account_type)
        if kyc_status:
            query = query.filter(cls.kyc_status == kyc_status)
        if is_active is not None:
            query = query.filter(cls.is_active == is_active)
        
        query = query.offset(skip).limit(limit).order_by(cls.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, update_data: Dict[str, Any]) -> "User":
        """Update user data."""
        for field, value in update_data.items():
            if hasattr(self, field):
                setattr(self, field, value)
        
        self.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(self)
        return self
    
    async def delete(self, db: AsyncSession) -> None:
        """Hard delete user."""
        await db.delete(self)
        await db.commit()