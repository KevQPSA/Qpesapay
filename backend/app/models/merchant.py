"""
Merchant model for Qpesapay backend.
Handles merchant business information and payment settings.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum, Index, ForeignKey, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any, List

from app.models.base import Base


class MerchantStatus(str, enum.Enum):
    """Merchant account status."""
    PENDING = "pending"                    # Application pending
    ACTIVE = "active"                      # Active merchant
    SUSPENDED = "suspended"                # Temporarily suspended
    DEACTIVATED = "deactivated"           # Permanently deactivated
    UNDER_REVIEW = "under_review"         # Under compliance review


class VerificationLevel(str, enum.Enum):
    """Merchant verification levels."""
    BASIC = "basic"                        # Basic verification
    STANDARD = "standard"                  # Standard verification
    PREMIUM = "premium"                    # Premium verification
    ENTERPRISE = "enterprise"              # Enterprise verification


class SettlementMethod(str, enum.Enum):
    """Settlement methods."""
    MPESA = "mpesa"                        # M-Pesa settlement
    BANK_TRANSFER = "bank_transfer"        # Bank transfer
    CRYPTO_WALLET = "crypto_wallet"        # Keep in crypto
    MIXED = "mixed"                        # Mixed settlement


class SettlementFrequency(str, enum.Enum):
    """Settlement frequency options."""
    INSTANT = "instant"                    # Instant settlement
    DAILY = "daily"                        # Daily settlement
    WEEKLY = "weekly"                      # Weekly settlement
    MONTHLY = "monthly"                    # Monthly settlement


class BusinessType(str, enum.Enum):
    """Business type categories."""
    RETAIL = "retail"
    ECOMMERCE = "ecommerce"
    RESTAURANT = "restaurant"
    SERVICES = "services"
    DIGITAL = "digital"
    MARKETPLACE = "marketplace"
    OTHER = "other"


class Merchant(Base):
    """
    Merchant model for business accounts.
    
    Stores business information, payment settings, and settlement preferences
    for merchants accepting crypto payments.
    """
    __tablename__ = "merchants"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Business information
    business_name = Column(String(255), nullable=False, index=True)
    business_registration_number = Column(String(100), nullable=True, unique=True)
    tax_identification_number = Column(String(100), nullable=True, unique=True)
    business_type = Column(Enum(BusinessType), nullable=False)
    
    # Business address
    business_address = Column(Text, nullable=True)
    business_city = Column(String(100), nullable=True)
    business_county = Column(String(100), nullable=True)
    business_postal_code = Column(String(20), nullable=True)
    business_country = Column(String(100), default="Kenya", nullable=False)
    
    # Contact information
    business_phone = Column(String(20), nullable=True)
    business_email = Column(String(255), nullable=True)
    website_url = Column(String(500), nullable=True)
    
    # Merchant status and verification
    status = Column(Enum(MerchantStatus), nullable=False, default=MerchantStatus.PENDING, index=True)
    verification_level = Column(Enum(VerificationLevel), nullable=False, default=VerificationLevel.BASIC)
    
    # Verification documents
    business_license_url = Column(String(500), nullable=True)
    tax_certificate_url = Column(String(500), nullable=True)
    bank_statement_url = Column(String(500), nullable=True)
    additional_documents = Column(Text, nullable=True)  # JSON string of document URLs
    
    # Settlement configuration
    settlement_method = Column(Enum(SettlementMethod), nullable=False, default=SettlementMethod.MPESA)
    settlement_frequency = Column(Enum(SettlementFrequency), nullable=False, default=SettlementFrequency.DAILY)
    auto_settlement_enabled = Column(Boolean, default=True, nullable=False)
    
    # Settlement account details
    mpesa_phone_number = Column(String(20), nullable=True)
    bank_name = Column(String(100), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_account_name = Column(String(255), nullable=True)
    bank_branch = Column(String(100), nullable=True)
    
    # Crypto wallet for settlements
    settlement_wallet_address = Column(String(255), nullable=True)
    settlement_wallet_network = Column(String(50), nullable=True)
    
    # Transaction limits and fees
    daily_transaction_limit = Column(NUMERIC(20, 2), nullable=True)
    monthly_transaction_limit = Column(NUMERIC(20, 2), nullable=True)
    minimum_settlement_amount = Column(NUMERIC(20, 2), default=100.00, nullable=False)  # Minimum 100 KES
    
    # Fee structure (as percentages)
    transaction_fee_percentage = Column(NUMERIC(5, 4), default=0.015, nullable=False)  # 1.5% default
    settlement_fee_percentage = Column(NUMERIC(5, 4), default=0.005, nullable=False)   # 0.5% default
    
    # API configuration
    api_key_hash = Column(String(255), nullable=True, unique=True)
    webhook_url = Column(String(500), nullable=True)
    webhook_secret = Column(String(255), nullable=True)
    webhook_events = Column(Text, nullable=True)  # JSON array of subscribed events
    
    # Business metrics
    total_transactions = Column(NUMERIC(20, 0), default=0, nullable=False)
    total_volume_kes = Column(NUMERIC(20, 2), default=0, nullable=False)
    total_volume_crypto = Column(NUMERIC(20, 8), default=0, nullable=False)
    average_transaction_size = Column(NUMERIC(20, 2), default=0, nullable=False)
    
    # Risk management
    risk_score = Column(NUMERIC(3, 2), default=0, nullable=False)  # 0.00 to 1.00
    risk_level = Column(String(20), default="low", nullable=False)  # low, medium, high
    compliance_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    verified_at = Column(DateTime, nullable=True)
    last_transaction_at = Column(DateTime, nullable=True)
    
    # Soft delete
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="merchant_profile")
    transactions = relationship("Transaction", back_populates="merchant", cascade="all, delete-orphan")
    settlements = relationship("Settlement", back_populates="merchant", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_merchants_user_id', 'user_id'),
        Index('idx_merchants_business_name', 'business_name'),
        Index('idx_merchants_status', 'status'),
        Index('idx_merchants_verification_level', 'verification_level'),
        Index('idx_merchants_business_type', 'business_type'),
        Index('idx_merchants_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Merchant(id={self.id}, business_name={self.business_name}, status={self.status})>"
    
    @property
    def daily_transaction_limit_decimal(self) -> Optional[Decimal]:
        """Get daily transaction limit as Decimal."""
        return Decimal(str(self.daily_transaction_limit)) if self.daily_transaction_limit else None
    
    @property
    def monthly_transaction_limit_decimal(self) -> Optional[Decimal]:
        """Get monthly transaction limit as Decimal."""
        return Decimal(str(self.monthly_transaction_limit)) if self.monthly_transaction_limit else None
    
    @property
    def minimum_settlement_amount_decimal(self) -> Decimal:
        """Get minimum settlement amount as Decimal."""
        return Decimal(str(self.minimum_settlement_amount))
    
    @property
    def transaction_fee_percentage_decimal(self) -> Decimal:
        """Get transaction fee percentage as Decimal."""
        return Decimal(str(self.transaction_fee_percentage))
    
    @property
    def settlement_fee_percentage_decimal(self) -> Decimal:
        """Get settlement fee percentage as Decimal."""
        return Decimal(str(self.settlement_fee_percentage))
    
    @property
    def total_volume_kes_decimal(self) -> Decimal:
        """Get total volume KES as Decimal."""
        return Decimal(str(self.total_volume_kes))
    
    @property
    def total_volume_crypto_decimal(self) -> Decimal:
        """Get total volume crypto as Decimal."""
        return Decimal(str(self.total_volume_crypto))
    
    @property
    def is_active(self) -> bool:
        """Check if merchant is active."""
        return self.status == MerchantStatus.ACTIVE and not self.is_deleted
    
    @property
    def is_verified(self) -> bool:
        """Check if merchant is verified."""
        return self.verified_at is not None
    
    @property
    def is_deleted(self) -> bool:
        """Check if merchant is soft deleted."""
        return self.deleted_at is not None
    
    @property
    def can_accept_payments(self) -> bool:
        """Check if merchant can accept payments."""
        return (
            self.is_active and
            self.verification_level != VerificationLevel.BASIC and
            self.has_settlement_method_configured
        )
    
    @property
    def has_settlement_method_configured(self) -> bool:
        """Check if settlement method is properly configured."""
        if self.settlement_method == SettlementMethod.MPESA:
            return bool(self.mpesa_phone_number)
        elif self.settlement_method == SettlementMethod.BANK_TRANSFER:
            return bool(self.bank_account_number and self.bank_name)
        elif self.settlement_method == SettlementMethod.CRYPTO_WALLET:
            return bool(self.settlement_wallet_address)
        return False
    
    @property
    def verification_level_display(self) -> str:
        """Get display name for verification level."""
        level_names = {
            VerificationLevel.BASIC: "Basic",
            VerificationLevel.STANDARD: "Standard",
            VerificationLevel.PREMIUM: "Premium",
            VerificationLevel.ENTERPRISE: "Enterprise",
        }
        return level_names.get(self.verification_level, self.verification_level.value)
    
    @property
    def transaction_limits(self) -> Dict[str, Any]:
        """Get transaction limits information."""
        return {
            "daily_limit": str(self.daily_transaction_limit_decimal) if self.daily_transaction_limit_decimal else None,
            "monthly_limit": str(self.monthly_transaction_limit_decimal) if self.monthly_transaction_limit_decimal else None,
            "minimum_settlement": str(self.minimum_settlement_amount_decimal),
        }
    
    @property
    def fee_structure(self) -> Dict[str, str]:
        """Get fee structure information."""
        return {
            "transaction_fee": f"{float(self.transaction_fee_percentage_decimal) * 100:.2f}%",
            "settlement_fee": f"{float(self.settlement_fee_percentage_decimal) * 100:.2f}%",
        }
    
    def calculate_transaction_fee(self, amount: Decimal) -> Decimal:
        """
        Calculate transaction fee for given amount.
        
        Args:
            amount: Transaction amount
            
        Returns:
            Decimal: Transaction fee
        """
        return amount * self.transaction_fee_percentage_decimal
    
    def calculate_settlement_fee(self, amount: Decimal) -> Decimal:
        """
        Calculate settlement fee for given amount.
        
        Args:
            amount: Settlement amount
            
        Returns:
            Decimal: Settlement fee
        """
        return amount * self.settlement_fee_percentage_decimal
    
    def update_business_metrics(self, transaction_amount: Decimal, crypto_amount: Decimal = None):
        """
        Update business metrics after a transaction.
        
        Args:
            transaction_amount: Transaction amount in KES
            crypto_amount: Transaction amount in crypto
        """
        self.total_transactions = int(self.total_transactions) + 1
        self.total_volume_kes = self.total_volume_kes_decimal + transaction_amount
        
        if crypto_amount:
            self.total_volume_crypto = self.total_volume_crypto_decimal + crypto_amount
        
        # Update average transaction size
        if self.total_transactions > 0:
            self.average_transaction_size = self.total_volume_kes_decimal / Decimal(str(self.total_transactions))
        
        self.last_transaction_at = datetime.utcnow()
    
    def verify_merchant(self, verification_level: VerificationLevel):
        """
        Verify merchant account.
        
        Args:
            verification_level: Verification level to set
        """
        self.verification_level = verification_level
        self.verified_at = datetime.utcnow()
        if self.status == MerchantStatus.PENDING:
            self.status = MerchantStatus.ACTIVE
    
    def suspend_merchant(self, reason: str = None):
        """
        Suspend merchant account.
        
        Args:
            reason: Reason for suspension
        """
        self.status = MerchantStatus.SUSPENDED
        if reason:
            self.compliance_notes = f"{datetime.utcnow().isoformat()}: Suspended - {reason}\n{self.compliance_notes or ''}"
    
    def reactivate_merchant(self):
        """Reactivate suspended merchant account."""
        self.status = MerchantStatus.ACTIVE
        self.compliance_notes = f"{datetime.utcnow().isoformat()}: Reactivated\n{self.compliance_notes or ''}"
    
    def soft_delete(self):
        """Soft delete the merchant account."""
        self.deleted_at = datetime.utcnow()
        self.status = MerchantStatus.DEACTIVATED
    
    def restore(self):
        """Restore soft deleted merchant account."""
        self.deleted_at = None
        self.status = MerchantStatus.ACTIVE
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert merchant to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            dict: Merchant data
        """
        data = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "business_name": self.business_name,
            "business_type": self.business_type.value,
            "status": self.status.value,
            "verification_level": self.verification_level.value,
            "verification_level_display": self.verification_level_display,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "can_accept_payments": self.can_accept_payments,
            "settlement_method": self.settlement_method.value,
            "settlement_frequency": self.settlement_frequency.value,
            "auto_settlement_enabled": self.auto_settlement_enabled,
            "transaction_limits": self.transaction_limits,
            "fee_structure": self.fee_structure,
            "total_transactions": str(self.total_transactions),
            "total_volume_kes": str(self.total_volume_kes_decimal),
            "average_transaction_size": str(self.average_transaction_size),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "last_transaction_at": self.last_transaction_at.isoformat() if self.last_transaction_at else None,
        }
        
        if include_sensitive:
            data.update({
                "business_registration_number": self.business_registration_number,
                "tax_identification_number": self.tax_identification_number,
                "business_address": self.business_address,
                "business_phone": self.business_phone,
                "business_email": self.business_email,
                "website_url": self.website_url,
                "mpesa_phone_number": self.mpesa_phone_number,
                "bank_name": self.bank_name,
                "bank_account_number": self.bank_account_number,
                "bank_account_name": self.bank_account_name,
                "settlement_wallet_address": self.settlement_wallet_address,
                "webhook_url": self.webhook_url,
                "risk_score": str(self.risk_score),
                "risk_level": self.risk_level,
                "compliance_notes": self.compliance_notes,
            })
        
        return data
    
    def get_settlement_info(self) -> Dict[str, Any]:
        """
        Get settlement configuration information.
        
        Returns:
            dict: Settlement information
        """
        info = {
            "method": self.settlement_method.value,
            "frequency": self.settlement_frequency.value,
            "auto_enabled": self.auto_settlement_enabled,
            "minimum_amount": str(self.minimum_settlement_amount_decimal),
            "configured": self.has_settlement_method_configured,
        }
        
        if self.settlement_method == SettlementMethod.MPESA:
            info["mpesa_phone"] = self.mpesa_phone_number
        elif self.settlement_method == SettlementMethod.BANK_TRANSFER:
            info["bank_name"] = self.bank_name
            info["account_number"] = self.bank_account_number
        elif self.settlement_method == SettlementMethod.CRYPTO_WALLET:
            info["wallet_address"] = self.settlement_wallet_address
            info["wallet_network"] = self.settlement_wallet_network
        
        return info