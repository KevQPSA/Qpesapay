"""
Wallet model for Qpesapay backend.
Handles cryptocurrency wallets for Bitcoin and USDT.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum, Index, ForeignKey, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Dict, Any

from app.models.base import Base


class WalletNetwork(str, enum.Enum):
    """Supported blockchain networks."""
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    TRON = "tron"


class WalletStatus(str, enum.Enum):
    """Wallet status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FROZEN = "frozen"
    COMPROMISED = "compromised"


class CurrencyType(str, enum.Enum):
    """Supported currencies."""
    BTC = "BTC"
    USDT = "USDT"
    KES = "KES"


class Wallet(Base):
    """
    Cryptocurrency wallet model.
    
    Supports Bitcoin and USDT wallets with secure private key storage
    and balance tracking.
    """
    __tablename__ = "wallets"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign key to user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Wallet identification
    network = Column(Enum(WalletNetwork), nullable=False)
    currency = Column(Enum(CurrencyType), nullable=False)
    address = Column(String(255), nullable=False, unique=True, index=True)
    
    # Security - encrypted private key
    encrypted_private_key = Column(Text, nullable=False)
    public_key = Column(Text, nullable=True)
    
    # HD Wallet information
    derivation_path = Column(String(100), nullable=True)  # e.g., "m/44'/0'/0'/0/0"
    master_key_id = Column(String(100), nullable=True)    # Reference to master key
    
    # Balance tracking (using NUMERIC for precise decimal handling)
    balance_crypto = Column(NUMERIC(20, 8), default=0, nullable=False)  # 8 decimals for crypto
    balance_kes = Column(NUMERIC(20, 2), default=0, nullable=False)     # 2 decimals for KES
    
    # Balance update tracking
    last_balance_update = Column(DateTime, nullable=True)
    balance_sync_block = Column(String(100), nullable=True)  # Last synced block number/hash
    
    # Wallet status and settings
    status = Column(Enum(WalletStatus), nullable=False, default=WalletStatus.ACTIVE)
    is_default = Column(Boolean, default=False, nullable=False)  # Default wallet for user
    is_watch_only = Column(Boolean, default=False, nullable=False)  # Watch-only wallet
    
    # Transaction limits
    daily_limit_crypto = Column(NUMERIC(20, 8), nullable=True)
    daily_limit_kes = Column(NUMERIC(20, 2), nullable=True)
    daily_spent_crypto = Column(NUMERIC(20, 8), default=0, nullable=False)
    daily_spent_kes = Column(NUMERIC(20, 2), default=0, nullable=False)
    daily_limit_reset_date = Column(DateTime, nullable=True)
    
    # Metadata
    label = Column(String(100), nullable=True)  # User-defined wallet label
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_used = Column(DateTime, nullable=True)
    
    # Soft delete
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_wallets_user_network', 'user_id', 'network'),
        Index('idx_wallets_user_currency', 'user_id', 'currency'),
        Index('idx_wallets_address', 'address'),
        Index('idx_wallets_status', 'status'),
        Index('idx_wallets_network_currency', 'network', 'currency'),
        Index('idx_wallets_user_default', 'user_id', 'is_default'),
    )
    
    def __repr__(self):
        return f"<Wallet(id={self.id}, network={self.network}, currency={self.currency}, address={self.address[:10]}...)>"
    
    @property
    def balance_crypto_decimal(self) -> Decimal:
        """Get crypto balance as Decimal."""
        return Decimal(str(self.balance_crypto)) if self.balance_crypto else Decimal('0')
    
    @property
    def balance_kes_decimal(self) -> Decimal:
        """Get KES balance as Decimal."""
        return Decimal(str(self.balance_kes)) if self.balance_kes else Decimal('0')
    
    @property
    def daily_spent_crypto_decimal(self) -> Decimal:
        """Get daily spent crypto as Decimal."""
        return Decimal(str(self.daily_spent_crypto)) if self.daily_spent_crypto else Decimal('0')
    
    @property
    def daily_spent_kes_decimal(self) -> Decimal:
        """Get daily spent KES as Decimal."""
        return Decimal(str(self.daily_spent_kes)) if self.daily_spent_kes else Decimal('0')
    
    @property
    def is_bitcoin_wallet(self) -> bool:
        """Check if this is a Bitcoin wallet."""
        return self.network == WalletNetwork.BITCOIN and self.currency == CurrencyType.BTC
    
    @property
    def is_usdt_wallet(self) -> bool:
        """Check if this is a USDT wallet."""
        return self.currency == CurrencyType.USDT
    
    @property
    def is_ethereum_usdt(self) -> bool:
        """Check if this is an Ethereum USDT wallet."""
        return self.network == WalletNetwork.ETHEREUM and self.currency == CurrencyType.USDT
    
    @property
    def is_tron_usdt(self) -> bool:
        """Check if this is a Tron USDT wallet."""
        return self.network == WalletNetwork.TRON and self.currency == CurrencyType.USDT
    
    @property
    def is_active(self) -> bool:
        """Check if wallet is active."""
        return self.status == WalletStatus.ACTIVE and not self.is_deleted
    
    @property
    def is_deleted(self) -> bool:
        """Check if wallet is soft deleted."""
        return self.deleted_at is not None
    
    @property
    def network_display_name(self) -> str:
        """Get display name for network."""
        network_names = {
            WalletNetwork.BITCOIN: "Bitcoin",
            WalletNetwork.ETHEREUM: "Ethereum",
            WalletNetwork.TRON: "Tron",
        }
        return network_names.get(self.network, self.network.value)
    
    @property
    def short_address(self) -> str:
        """Get shortened address for display."""
        if len(self.address) > 10:
            return f"{self.address[:6]}...{self.address[-4:]}"
        return self.address
    
    def update_balance(self, crypto_balance: Decimal, kes_balance: Decimal = None, block_info: str = None):
        """
        Update wallet balance.
        
        Args:
            crypto_balance: New crypto balance
            kes_balance: New KES balance (optional)
            block_info: Block number/hash for sync tracking
        """
        self.balance_crypto = crypto_balance
        if kes_balance is not None:
            self.balance_kes = kes_balance
        
        self.last_balance_update = datetime.utcnow()
        if block_info:
            self.balance_sync_block = block_info
    
    def can_spend(self, amount: Decimal, currency: str = None) -> tuple[bool, str]:
        """
        Check if wallet can spend the specified amount.
        
        Args:
            amount: Amount to spend
            currency: Currency type (crypto or kes)
            
        Returns:
            tuple: (can_spend, reason)
        """
        if not self.is_active:
            return False, "Wallet is not active"
        
        if currency == "crypto" or currency == self.currency.value:
            if amount > self.balance_crypto_decimal:
                return False, "Insufficient crypto balance"
            
            # Check daily limits
            if self.daily_limit_crypto:
                daily_limit = Decimal(str(self.daily_limit_crypto))
                if self.daily_spent_crypto_decimal + amount > daily_limit:
                    return False, "Daily spending limit exceeded"
        
        elif currency == "KES":
            if amount > self.balance_kes_decimal:
                return False, "Insufficient KES balance"
            
            # Check daily limits
            if self.daily_limit_kes:
                daily_limit = Decimal(str(self.daily_limit_kes))
                if self.daily_spent_kes_decimal + amount > daily_limit:
                    return False, "Daily spending limit exceeded"
        
        return True, "OK"
    
    def add_to_daily_spent(self, amount: Decimal, currency: str):
        """
        Add amount to daily spending tracker.
        
        Args:
            amount: Amount spent
            currency: Currency type
        """
        # Reset daily spending if it's a new day
        today = datetime.utcnow().date()
        if not self.daily_limit_reset_date or self.daily_limit_reset_date.date() != today:
            self.daily_spent_crypto = Decimal('0')
            self.daily_spent_kes = Decimal('0')
            self.daily_limit_reset_date = datetime.utcnow()
        
        if currency == "crypto" or currency == self.currency.value:
            self.daily_spent_crypto = self.daily_spent_crypto_decimal + amount
        elif currency == "KES":
            self.daily_spent_kes = self.daily_spent_kes_decimal + amount
    
    def set_as_default(self):
        """Set this wallet as the default for the user."""
        self.is_default = True
    
    def freeze(self, reason: str = None):
        """Freeze the wallet."""
        self.status = WalletStatus.FROZEN
        # TODO: Log the freeze action with reason
    
    def unfreeze(self):
        """Unfreeze the wallet."""
        self.status = WalletStatus.ACTIVE
    
    def mark_compromised(self):
        """Mark wallet as compromised."""
        self.status = WalletStatus.COMPROMISED
        # TODO: Trigger security alerts
    
    def soft_delete(self):
        """Soft delete the wallet."""
        self.deleted_at = datetime.now(timezone.utc)
        self.status = WalletStatus.INACTIVE
    
    def restore(self):
        """Restore soft deleted wallet."""
        self.deleted_at = None
        self.status = WalletStatus.ACTIVE
    
    def update_last_used(self):
        """Update last used timestamp."""
        self.last_used = datetime.now(timezone.utc)
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert wallet to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            dict: Wallet data
        """
        data = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "network": self.network.value,
            "currency": self.currency.value,
            "address": self.address,
            "balance_crypto": str(self.balance_crypto_decimal),
            "balance_kes": str(self.balance_kes_decimal),
            "status": self.status.value,
            "is_default": self.is_default,
            "is_watch_only": self.is_watch_only,
            "label": self.label,
            "description": self.description,
            "network_display_name": self.network_display_name,
            "short_address": self.short_address,
            "last_balance_update": self.last_balance_update.isoformat() if self.last_balance_update else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
        }
        
        if include_sensitive:
            data.update({
                "public_key": self.public_key,
                "derivation_path": self.derivation_path,
                "daily_limit_crypto": str(self.daily_limit_crypto) if self.daily_limit_crypto else None,
                "daily_limit_kes": str(self.daily_limit_kes) if self.daily_limit_kes else None,
                "daily_spent_crypto": str(self.daily_spent_crypto_decimal),
                "daily_spent_kes": str(self.daily_spent_kes_decimal),
                "balance_sync_block": self.balance_sync_block,
            })
        
        return data
    
    def get_balance_info(self) -> Dict[str, Any]:
        """
        Get comprehensive balance information.
        
        Returns:
            dict: Balance information
        """
        return {
            "crypto": {
                "amount": str(self.balance_crypto_decimal),
                "currency": self.currency.value,
                "network": self.network.value,
            },
            "fiat": {
                "amount": str(self.balance_kes_decimal),
                "currency": "KES",
            },
            "daily_limits": {
                "crypto_limit": str(self.daily_limit_crypto) if self.daily_limit_crypto else None,
                "crypto_spent": str(self.daily_spent_crypto_decimal),
                "kes_limit": str(self.daily_limit_kes) if self.daily_limit_kes else None,
                "kes_spent": str(self.daily_spent_kes_decimal),
            },
            "last_updated": self.last_balance_update.isoformat() if self.last_balance_update else None,
        }