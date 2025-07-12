"""
Transaction schemas for Qpesapay backend.
Pydantic models for transaction-related API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
import re

from app.models.transaction import TransactionType, TransactionStatus, PaymentMethod


class TransactionBase(BaseModel):
    """Base transaction schema with common fields."""
    transaction_type: TransactionType = Field(..., description="Type of transaction")
    amount_crypto: Optional[Decimal] = Field(None, gt=0, description="Amount in cryptocurrency")
    amount_kes: Optional[Decimal] = Field(None, gt=0, description="Amount in KES")
    description: Optional[str] = Field(None, max_length=500, description="Transaction description")
    
    @validator('amount_crypto', 'amount_kes')
    def validate_amounts(cls, v):
        """Validate transaction amounts."""
        if v is not None and v <= 0:
            raise ValueError('Amount must be positive')
        
        # Check for reasonable precision
        if v is not None and v.as_tuple().exponent < -8:
            raise ValueError('Amount has too many decimal places')
        
        return v


class PaymentCreate(BaseModel):
    """Schema for creating a payment transaction."""
    payment_method: PaymentMethod = Field(..., description="Payment method")
    amount_crypto: Decimal = Field(..., gt=0, description="Amount in cryptocurrency")
    to_address: str = Field(..., description="Recipient address")
    merchant_id: Optional[str] = Field(None, description="Merchant ID (for merchant payments)")
    description: Optional[str] = Field(None, max_length=500, description="Payment description")
    fee_rate: Optional[Decimal] = Field(None, ge=0, description="Custom fee rate")
    
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
    
    @validator('amount_crypto')
    def validate_amount(cls, v):
        """Validate payment amount."""
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        
        # Check for reasonable precision (8 decimal places max)
        if v.as_tuple().exponent < -8:
            raise ValueError('Amount has too many decimal places')
        
        return v


class SettlementCreate(BaseModel):
    """Schema for creating a settlement transaction."""
    merchant_id: str = Field(..., description="Merchant ID")
    amount_kes: Decimal = Field(..., gt=0, description="Settlement amount in KES")
    settlement_method: str = Field(..., description="Settlement method (mpesa, bank_transfer)")
    description: Optional[str] = Field(None, max_length=500, description="Settlement description")
    
    @validator('settlement_method')
    def validate_settlement_method(cls, v):
        """Validate settlement method."""
        valid_methods = ['mpesa', 'bank_transfer', 'crypto_wallet']
        if v.lower() not in valid_methods:
            raise ValueError(f'Settlement method must be one of: {", ".join(valid_methods)}')
        return v.lower()


class BillPaymentCreate(BaseModel):
    """Schema for creating a bill payment transaction."""
    bill_provider: str = Field(..., description="Bill provider (KPLC, Water, DSTV, etc.)")
    bill_account_number: str = Field(..., description="Bill account number")
    amount_kes: Decimal = Field(..., gt=0, description="Bill amount in KES")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    description: Optional[str] = Field(None, max_length=500, description="Bill payment description")
    
    @validator('bill_provider')
    def validate_provider(cls, v):
        """Validate bill provider."""
        if not v.strip():
            raise ValueError('Bill provider cannot be empty')
        return v.strip().upper()
    
    @validator('bill_account_number')
    def validate_account_number(cls, v):
        """Validate bill account number."""
        if not v.strip():
            raise ValueError('Bill account number cannot be empty')
        
        # Remove any spaces or special characters
        account_number = re.sub(r'[^\w]', '', v.strip())
        
        if len(account_number) < 3:
            raise ValueError('Bill account number too short')
        
        return account_number


class TransactionResponse(BaseModel):
    """Schema for transaction response data."""
    id: str = Field(..., description="Transaction ID")
    user_id: str = Field(..., description="User ID")
    wallet_id: Optional[str] = Field(None, description="Wallet ID")
    merchant_id: Optional[str] = Field(None, description="Merchant ID")
    transaction_type: str = Field(..., description="Transaction type")
    status: str = Field(..., description="Transaction status")
    payment_method: Optional[str] = Field(None, description="Payment method")
    reference_number: Optional[str] = Field(None, description="Reference number")
    amount_crypto: Optional[str] = Field(None, description="Crypto amount")
    amount_kes: Optional[str] = Field(None, description="KES amount")
    amount_usd: Optional[str] = Field(None, description="USD amount")
    network_fee: Optional[str] = Field(None, description="Network fee")
    platform_fee: Optional[str] = Field(None, description="Platform fee")
    total_fee: Optional[str] = Field(None, description="Total fee")
    blockchain_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    confirmations: Optional[int] = Field(None, description="Number of confirmations")
    required_confirmations: Optional[int] = Field(None, description="Required confirmations")
    is_fully_confirmed: bool = Field(..., description="Whether transaction is fully confirmed")
    description: Optional[str] = Field(None, description="Transaction description")
    initiated_at: datetime = Field(..., description="Transaction initiation time")
    processed_at: Optional[datetime] = Field(None, description="Processing time")
    confirmed_at: Optional[datetime] = Field(None, description="Confirmation time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True


class TransactionDetails(TransactionResponse):
    """Extended transaction details with additional information."""
    from_address: Optional[str] = Field(None, description="Sender address")
    to_address: Optional[str] = Field(None, description="Recipient address")
    block_number: Optional[str] = Field(None, description="Block number")
    exchange_rate_usd_kes: Optional[str] = Field(None, description="USD to KES exchange rate")
    exchange_rate_crypto_usd: Optional[str] = Field(None, description="Crypto to USD exchange rate")
    mpesa_reference: Optional[str] = Field(None, description="M-Pesa reference")
    mpesa_phone_number: Optional[str] = Field(None, description="M-Pesa phone number")
    bill_provider: Optional[str] = Field(None, description="Bill provider")
    bill_account_number: Optional[str] = Field(None, description="Bill account number")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    retry_count: int = Field(..., description="Number of retry attempts")
    client_ip: Optional[str] = Field(None, description="Client IP address")
    updated_at: datetime = Field(..., description="Last update timestamp")


class TransactionStatusUpdate(BaseModel):
    """Schema for updating transaction status."""
    status: TransactionStatus = Field(..., description="New transaction status")
    blockchain_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    confirmations: Optional[int] = Field(None, ge=0, description="Number of confirmations")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class TransactionList(BaseModel):
    """Schema for paginated transaction list."""
    transactions: List[TransactionResponse] = Field(..., description="List of transactions")
    total: int = Field(..., description="Total number of transactions")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")


class TransactionStats(BaseModel):
    """Schema for transaction statistics."""
    total_transactions: int = Field(..., description="Total number of transactions")
    successful_transactions: int = Field(..., description="Number of successful transactions")
    failed_transactions: int = Field(..., description="Number of failed transactions")
    pending_transactions: int = Field(..., description="Number of pending transactions")
    total_volume_crypto: str = Field(..., description="Total volume in crypto")
    total_volume_kes: str = Field(..., description="Total volume in KES")
    total_fees_paid: str = Field(..., description="Total fees paid")
    average_transaction_size: str = Field(..., description="Average transaction size")
    success_rate: float = Field(..., description="Transaction success rate")
    
    class Config:
        from_attributes = True


class TransactionSearch(BaseModel):
    """Schema for transaction search filters."""
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    wallet_id: Optional[str] = Field(None, description="Filter by wallet ID")
    merchant_id: Optional[str] = Field(None, description="Filter by merchant ID")
    transaction_type: Optional[TransactionType] = Field(None, description="Filter by transaction type")
    status: Optional[TransactionStatus] = Field(None, description="Filter by status")
    payment_method: Optional[PaymentMethod] = Field(None, description="Filter by payment method")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Minimum amount filter")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Maximum amount filter")
    currency: Optional[str] = Field(None, description="Currency filter (crypto, kes, usd)")
    from_date: Optional[datetime] = Field(None, description="Start date filter")
    to_date: Optional[datetime] = Field(None, description="End date filter")
    blockchain_hash: Optional[str] = Field(None, description="Filter by blockchain hash")
    reference_number: Optional[str] = Field(None, description="Filter by reference number")
    
    @validator('max_amount')
    def validate_amount_range(cls, v, values):
        """Validate amount range."""
        min_amount = values.get('min_amount')
        if min_amount is not None and v is not None and v < min_amount:
            raise ValueError('Maximum amount must be greater than minimum amount')
        return v
    
    @validator('to_date')
    def validate_date_range(cls, v, values):
        """Validate date range."""
        from_date = values.get('from_date')
        if from_date is not None and v is not None and v < from_date:
            raise ValueError('End date must be after start date')
        return v


class TransactionExport(BaseModel):
    """Schema for transaction export request."""
    format: str = Field(..., description="Export format (csv, xlsx, pdf)")
    filters: Optional[TransactionSearch] = Field(None, description="Export filters")
    include_sensitive: bool = Field(False, description="Include sensitive data")
    
    @validator('format')
    def validate_format(cls, v):
        """Validate export format."""
        valid_formats = ['csv', 'xlsx', 'pdf']
        if v.lower() not in valid_formats:
            raise ValueError(f'Format must be one of: {", ".join(valid_formats)}')
        return v.lower()


class TransactionWebhook(BaseModel):
    """Schema for transaction webhook payload."""
    event_type: str = Field(..., description="Webhook event type")
    transaction_id: str = Field(..., description="Transaction ID")
    status: str = Field(..., description="Transaction status")
    amount: str = Field(..., description="Transaction amount")
    currency: str = Field(..., description="Currency")
    blockchain_hash: Optional[str] = Field(None, description="Blockchain hash")
    confirmations: Optional[int] = Field(None, description="Number of confirmations")
    timestamp: datetime = Field(..., description="Event timestamp")
    signature: str = Field(..., description="Webhook signature")
    
    class Config:
        from_attributes = True


class TransactionReceipt(BaseModel):
    """Schema for transaction receipt."""
    transaction_id: str = Field(..., description="Transaction ID")
    reference_number: str = Field(..., description="Reference number")
    transaction_type: str = Field(..., description="Transaction type")
    status: str = Field(..., description="Transaction status")
    amount: str = Field(..., description="Transaction amount")
    currency: str = Field(..., description="Currency")
    fee: Optional[str] = Field(None, description="Transaction fee")
    from_address: Optional[str] = Field(None, description="Sender address")
    to_address: Optional[str] = Field(None, description="Recipient address")
    blockchain_hash: Optional[str] = Field(None, description="Blockchain hash")
    timestamp: datetime = Field(..., description="Transaction timestamp")
    merchant_name: Optional[str] = Field(None, description="Merchant name")
    description: Optional[str] = Field(None, description="Transaction description")
    
    class Config:
        from_attributes = True


class TransactionCancel(BaseModel):
    """Schema for cancelling a transaction."""
    reason: str = Field(..., max_length=500, description="Cancellation reason")
    
    @validator('reason')
    def validate_reason(cls, v):
        """Validate cancellation reason."""
        if not v.strip():
            raise ValueError('Cancellation reason cannot be empty')
        return v.strip()


class TransactionRetry(BaseModel):
    """Schema for retrying a failed transaction."""
    fee_rate: Optional[Decimal] = Field(None, ge=0, description="New fee rate for retry")
    notes: Optional[str] = Field(None, max_length=500, description="Retry notes")


class TransactionUpdate(TransactionBase):
    """Schema for updating a transaction."""
    pass
