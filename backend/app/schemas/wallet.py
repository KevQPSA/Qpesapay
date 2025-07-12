"""
Wallet schemas for Qpesapay backend.
Pydantic models for wallet-related API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
import re

from app.models.wallet import WalletNetwork, WalletStatus


class WalletBase(BaseModel):
    """Base wallet schema with common fields."""
    wallet_type: WalletNetwork = Field(..., description="Type of wallet (bitcoin, ethereum, tron)")
    currency: str = Field(..., description="Currency code (BTC, USDT)")
    network: Optional[str] = Field(None, description="Blockchain network (mainnet, testnet)")
    
    @validator('currency')
    def validate_currency(cls, v):
        """Validate currency code."""
        valid_currencies = ['BTC', 'USDT', 'ETH']
        if v.upper() not in valid_currencies:
            raise ValueError(f'Currency must be one of: {", ".join(valid_currencies)}')
        return v.upper()
    
    @validator('network')
    def validate_network(cls, v, values):
        """Validate network based on wallet type."""
        if v is None:
            return v
        
        wallet_type = values.get('wallet_type')
        valid_networks = {
            WalletNetwork.BITCOIN: ['mainnet', 'testnet'],
            WalletNetwork.ETHEREUM: ['mainnet', 'goerli', 'sepolia'],
            WalletNetwork.TRON: ['mainnet', 'shasta', 'nile']
        }
        
        if wallet_type and v not in valid_networks.get(wallet_type, []):
            raise ValueError(f'Invalid network for {wallet_type.value} wallet')
        
        return v


class WalletCreate(WalletBase):
    """Schema for creating a new wallet."""
    label: Optional[str] = Field(None, max_length=100, description="Wallet label/name")
    
    @validator('label')
    def validate_label(cls, v):
        """Validate wallet label."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Label cannot be empty')
        return v.strip()


class WalletImport(BaseModel):
    """Schema for importing an existing wallet."""
    wallet_type: WalletNetwork = Field(..., description="Type of wallet")
    currency: str = Field(..., description="Currency code")
    private_key: str = Field(..., description="Private key to import")
    label: Optional[str] = Field(None, max_length=100, description="Wallet label")
    network: Optional[str] = Field(None, description="Blockchain network")
    
    @validator('private_key')
    def validate_private_key(cls, v):
        """Validate private key format."""
        if not v.strip():
            raise ValueError('Private key cannot be empty')
        
        # Remove any whitespace
        private_key = v.strip()
        
        # Basic validation for hex format (64 characters for most blockchains)
        if not re.match(r'^[0-9a-fA-F]{64}$', private_key):
            raise ValueError('Invalid private key format')
        
        return private_key


class WalletUpdate(BaseModel):
    """Schema for updating wallet information."""
    label: Optional[str] = Field(None, max_length=100, description="Wallet label")
    daily_spending_limit: Optional[Decimal] = Field(None, ge=0, description="Daily spending limit")
    
    @validator('label')
    def validate_label(cls, v):
        """Validate wallet label."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Label cannot be empty')
        return v.strip()


class WalletResponse(BaseModel):
    """Schema for wallet response data."""
    id: str = Field(..., description="Wallet ID")
    user_id: str = Field(..., description="Owner user ID")
    wallet_type: str = Field(..., description="Wallet type")
    currency: str = Field(..., description="Currency code")
    network: Optional[str] = Field(None, description="Blockchain network")
    address: str = Field(..., description="Wallet address")
    label: Optional[str] = Field(None, description="Wallet label")
    status: str = Field(..., description="Wallet status")
    balance: str = Field(..., description="Current balance")
    balance_usd: Optional[str] = Field(None, description="Balance in USD")
    balance_kes: Optional[str] = Field(None, description="Balance in KES")
    daily_spending_limit: Optional[str] = Field(None, description="Daily spending limit")
    daily_spent_amount: str = Field(..., description="Amount spent today")
    is_active: bool = Field(..., description="Whether wallet is active")
    is_default: bool = Field(..., description="Whether this is the default wallet")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_transaction_at: Optional[datetime] = Field(None, description="Last transaction timestamp")
    
    class Config:
        from_attributes = True


class WalletDetails(WalletResponse):
    """Extended wallet details with additional information."""
    derivation_path: Optional[str] = Field(None, description="HD wallet derivation path")
    address_index: Optional[int] = Field(None, description="Address index for HD wallets")
    transaction_count: int = Field(..., description="Total number of transactions")
    total_received: str = Field(..., description="Total amount received")
    total_sent: str = Field(..., description="Total amount sent")
    pending_balance: str = Field(..., description="Pending balance")
    confirmed_balance: str = Field(..., description="Confirmed balance")
    last_sync_at: Optional[datetime] = Field(None, description="Last blockchain sync timestamp")
    sync_height: Optional[int] = Field(None, description="Last synced block height")
    updated_at: datetime = Field(..., description="Last update timestamp")


class WalletBalance(BaseModel):
    """Schema for wallet balance information."""
    wallet_id: str = Field(..., description="Wallet ID")
    currency: str = Field(..., description="Currency code")
    balance: str = Field(..., description="Current balance")
    confirmed_balance: str = Field(..., description="Confirmed balance")
    pending_balance: str = Field(..., description="Pending balance")
    balance_usd: Optional[str] = Field(None, description="Balance in USD")
    balance_kes: Optional[str] = Field(None, description="Balance in KES")
    last_updated: datetime = Field(..., description="Last balance update")
    
    class Config:
        from_attributes = True


class WalletTransaction(BaseModel):
    """Schema for wallet transaction history."""
    id: str = Field(..., description="Transaction ID")
    wallet_id: str = Field(..., description="Wallet ID")
    transaction_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    transaction_type: str = Field(..., description="Transaction type")
    amount: str = Field(..., description="Transaction amount")
    fee: Optional[str] = Field(None, description="Transaction fee")
    from_address: Optional[str] = Field(None, description="Sender address")
    to_address: Optional[str] = Field(None, description="Recipient address")
    status: str = Field(..., description="Transaction status")
    confirmations: Optional[int] = Field(None, description="Number of confirmations")
    block_height: Optional[int] = Field(None, description="Block height")
    created_at: datetime = Field(..., description="Transaction timestamp")
    confirmed_at: Optional[datetime] = Field(None, description="Confirmation timestamp")
    
    class Config:
        from_attributes = True


class WalletSend(BaseModel):
    """Schema for sending crypto from wallet."""
    to_address: str = Field(..., description="Recipient address")
    amount: Decimal = Field(..., gt=0, description="Amount to send")
    fee_rate: Optional[Decimal] = Field(None, ge=0, description="Fee rate (satoshis per byte for BTC)")
    note: Optional[str] = Field(None, max_length=500, description="Transaction note")
    
    @validator('to_address')
    def validate_address(cls, v):
        """Validate recipient address format."""
        if not v.strip():
            raise ValueError('Recipient address cannot be empty')
        
        address = v.strip()
        
        # Basic validation - more specific validation would be done in the service layer
        if len(address) < 26 or len(address) > 62:
            raise ValueError('Invalid address format')
        
        return address
    
    @validator('amount')
    def validate_amount(cls, v):
        """Validate transaction amount."""
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        
        # Check for reasonable precision (8 decimal places max)
        if v.as_tuple().exponent < -8:
            raise ValueError('Amount has too many decimal places')
        
        return v


class WalletReceive(BaseModel):
    """Schema for generating receive address."""
    amount: Optional[Decimal] = Field(None, gt=0, description="Expected amount (optional)")
    label: Optional[str] = Field(None, max_length=100, description="Address label")
    expires_in: Optional[int] = Field(None, ge=300, le=86400, description="Expiration time in seconds")
    
    @validator('label')
    def validate_label(cls, v):
        """Validate address label."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Label cannot be empty')
        return v.strip()


class WalletAddress(BaseModel):
    """Schema for wallet address information."""
    address: str = Field(..., description="Wallet address")
    label: Optional[str] = Field(None, description="Address label")
    amount: Optional[str] = Field(None, description="Expected amount")
    qr_code_url: Optional[str] = Field(None, description="QR code image URL")
    expires_at: Optional[datetime] = Field(None, description="Address expiration time")
    created_at: datetime = Field(..., description="Address creation time")
    
    class Config:
        from_attributes = True


class WalletStats(BaseModel):
    """Schema for wallet statistics."""
    wallet_id: str = Field(..., description="Wallet ID")
    total_transactions: int = Field(..., description="Total number of transactions")
    total_received: str = Field(..., description="Total amount received")
    total_sent: str = Field(..., description="Total amount sent")
    total_fees_paid: str = Field(..., description="Total fees paid")
    average_transaction_size: str = Field(..., description="Average transaction size")
    largest_transaction: str = Field(..., description="Largest transaction amount")
    first_transaction_at: Optional[datetime] = Field(None, description="First transaction timestamp")
    last_transaction_at: Optional[datetime] = Field(None, description="Last transaction timestamp")
    days_active: int = Field(..., description="Number of days with transactions")
    
    class Config:
        from_attributes = True


class WalletList(BaseModel):
    """Schema for paginated wallet list."""
    wallets: List[WalletResponse] = Field(..., description="List of wallets")
    total: int = Field(..., description="Total number of wallets")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")


class WalletBackup(BaseModel):
    """Schema for wallet backup information."""
    wallet_id: str = Field(..., description="Wallet ID")
    mnemonic_phrase: Optional[str] = Field(None, description="Mnemonic phrase (if HD wallet)")
    private_key: str = Field(..., description="Private key")
    address: str = Field(..., description="Wallet address")
    derivation_path: Optional[str] = Field(None, description="Derivation path")
    created_at: datetime = Field(..., description="Backup creation time")
    
    class Config:
        from_attributes = True


class WalletRestore(BaseModel):
    """Schema for restoring wallet from backup."""
    wallet_type: WalletNetwork = Field(..., description="Wallet type")
    currency: str = Field(..., description="Currency code")
    mnemonic_phrase: Optional[str] = Field(None, description="Mnemonic phrase")
    private_key: Optional[str] = Field(None, description="Private key")
    derivation_path: Optional[str] = Field(None, description="Derivation path")
    label: Optional[str] = Field(None, description="Wallet label")
    
    @validator('mnemonic_phrase')
    def validate_mnemonic(cls, v):
        """Validate mnemonic phrase."""
        if v is None:
            return v
        
        words = v.strip().split()
        if len(words) not in [12, 15, 18, 21, 24]:
            raise ValueError('Mnemonic phrase must contain 12, 15, 18, 21, or 24 words')
        
        return v.strip()
    
    @validator('private_key')
    def validate_private_key(cls, v):
        """Validate private key."""
        if v is None:
            return v
        return WalletImport.validate_private_key(v)


class WalletSync(BaseModel):
    """Schema for wallet synchronization status."""
    wallet_id: str = Field(..., description="Wallet ID")
    is_syncing: bool = Field(..., description="Whether wallet is currently syncing")
    sync_progress: float = Field(..., ge=0, le=1, description="Sync progress (0.0 to 1.0)")
    current_height: Optional[int] = Field(None, description="Current block height")
    target_height: Optional[int] = Field(None, description="Target block height")
    last_sync_at: Optional[datetime] = Field(None, description="Last sync timestamp")
    sync_error: Optional[str] = Field(None, description="Sync error message if any")
    
    class Config:
        from_attributes = True


class WalletExchangeRate(BaseModel):
    """Schema for wallet currency exchange rates."""
    currency: str = Field(..., description="Currency code")
    usd_rate: Optional[Decimal] = Field(None, description="Rate to USD")
    kes_rate: Optional[Decimal] = Field(None, description="Rate to KES")
    last_updated: datetime = Field(..., description="Last rate update")
    source: str = Field(..., description="Rate source")
    
    class Config:
        from_attributes = True


class WalletSecurity(BaseModel):
    """Schema for wallet security settings."""
    wallet_id: str = Field(..., description="Wallet ID")
    two_factor_required: bool = Field(..., description="Whether 2FA is required for transactions")
    daily_limit_enabled: bool = Field(..., description="Whether daily spending limit is enabled")
    daily_spending_limit: Optional[str] = Field(None, description="Daily spending limit")
    whitelist_enabled: bool = Field(..., description="Whether address whitelist is enabled")
    whitelisted_addresses: List[str] = Field(..., description="List of whitelisted addresses")
    last_security_update: datetime = Field(..., description="Last security settings update")
    
    class Config:
        from_attributes = True


class WalletSecurityUpdate(BaseModel):
    """Schema for updating wallet security settings."""
    two_factor_required: Optional[bool] = Field(None, description="Require 2FA for transactions")
    daily_spending_limit: Optional[Decimal] = Field(None, ge=0, description="Daily spending limit")
    whitelist_addresses: Optional[List[str]] = Field(None, description="Whitelisted addresses")
    
    @validator('whitelist_addresses')
    def validate_addresses(cls, v):
        """Validate whitelisted addresses."""
        if v is None:
            return v
        
        for address in v:
            if not address.strip():
                raise ValueError('Address cannot be empty')
            if len(address.strip()) < 26 or len(address.strip()) > 62:
                raise ValueError(f'Invalid address format: {address}')
        
        return [addr.strip() for addr in v]