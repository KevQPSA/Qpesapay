"""
Transaction model for Qpesapay backend.
Handles all payment transactions with comprehensive tracking.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum, Index, ForeignKey, NUMERIC, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any

from app.models.base import Base


class TransactionType(str, enum.Enum):
    """Transaction types."""
    PAYMENT = "payment"                    # Crypto payment
    SETTLEMENT = "settlement"              # Fiat settlement
    DEPOSIT = "deposit"                    # Crypto deposit
    WITHDRAWAL = "withdrawal"              # Crypto withdrawal
    CONVERSION = "conversion"              # Currency conversion
    FEE = "fee"                           # Fee transaction
    REFUND = "refund"                     # Refund transaction
    BILL_PAYMENT = "bill_payment"         # Utility bill payment
    P2P_TRANSFER = "p2p_transfer"         # Peer-to-peer transfer


class TransactionStatus(str, enum.Enum):
    """Transaction status."""
    PENDING = "pending"                    # Transaction initiated
    PROCESSING = "processing"              # Being processed
    CONFIRMING = "confirming"              # Waiting for blockchain confirmations
    CONFIRMED = "confirmed"                # Transaction confirmed
    COMPLETED = "completed"                # Transaction completed
    FAILED = "failed"                      # Transaction failed
    CANCELLED = "cancelled"                # Transaction cancelled
    EXPIRED = "expired"                    # Transaction expired


class PaymentMethod(str, enum.Enum):
    """Payment methods."""
    BITCOIN = "bitcoin"
    USDT_ETHEREUM = "usdt_ethereum"
    USDT_TRON = "usdt_tron"
    MPESA = "mpesa"
    BANK_TRANSFER = "bank_transfer"


class Transaction(Base):
    """
    Transaction model for all payment operations.
    
    Tracks crypto payments, fiat settlements, and other financial operations
    with comprehensive audit trails and status tracking.
    """
    __tablename__ = "transactions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=True, index=True)
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=True, index=True)
    
    # Transaction identification
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING, index=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    
    # External references
    external_id = Column(String(255), nullable=True, unique=True, index=True)  # External system ID
    reference_number = Column(String(100), nullable=True, unique=True, index=True)  # User-facing reference
    
    # Blockchain information
    blockchain_hash = Column(String(255), nullable=True, unique=True, index=True)
    blockchain_network = Column(String(50), nullable=True)
    block_number = Column(String(100), nullable=True)
    confirmations = Column(Integer, default=0, nullable=False)
    required_confirmations = Column(Integer, default=3, nullable=False)
    
    # Amount information (using NUMERIC for precise decimal handling)
    amount_crypto = Column(NUMERIC(20, 8), nullable=True)      # Crypto amount (8 decimals)
    amount_kes = Column(NUMERIC(20, 2), nullable=True)         # KES amount (2 decimals)
    amount_usd = Column(NUMERIC(20, 2), nullable=True)         # USD amount (2 decimals)
    
    # Fee information
    network_fee = Column(NUMERIC(20, 8), nullable=True)        # Blockchain network fee
    platform_fee = Column(NUMERIC(20, 2), nullable=True)      # Platform fee
    total_fee = Column(NUMERIC(20, 2), nullable=True)         # Total fees
    
    # Exchange rate at time of transaction
    exchange_rate_usd_kes = Column(NUMERIC(10, 4), nullable=True)
    exchange_rate_crypto_usd = Column(NUMERIC(15, 8), nullable=True)
    
    # Address information
    from_address = Column(String(255), nullable=True, index=True)
    to_address = Column(String(255), nullable=True, index=True)
    
    # M-Pesa specific fields
    mpesa_reference = Column(String(100), nullable=True, unique=True, index=True)
    mpesa_phone_number = Column(String(20), nullable=True)
    mpesa_receipt_number = Column(String(100), nullable=True)
    
    # Bill payment specific fields
    bill_provider = Column(String(100), nullable=True)        # KPLC, Water, DSTV, etc.
    bill_account_number = Column(String(100), nullable=True)
    bill_reference = Column(String(100), nullable=True)
    
    # Transaction metadata
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    extra_data = Column(Text, nullable=True)                     # JSON string for additional data
    
    # Timing information
    initiated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Error handling
    error_code = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String(100), nullable=True)           # System, API, User, etc.
    
    # IP and device tracking
    client_ip = Column(String(45), nullable=True)             # IPv4/IPv6
    user_agent = Column(Text, nullable=True)
    device_fingerprint = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    wallet = relationship("Wallet", back_populates="transactions")
    merchant = relationship("Merchant", back_populates="transactions")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_transactions_user_status', 'user_id', 'status'),
        Index('idx_transactions_user_type', 'user_id', 'transaction_type'),
        Index('idx_transactions_status_created', 'status', 'created_at'),
        Index('idx_transactions_blockchain_hash', 'blockchain_hash'),
        Index('idx_transactions_reference', 'reference_number'),
        Index('idx_transactions_mpesa_ref', 'mpesa_reference'),
        Index('idx_transactions_merchant_status', 'merchant_id', 'status'),
        Index('idx_transactions_created_at', 'created_at'),
        Index('idx_transactions_amount_kes', 'amount_kes'),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, status={self.status}, amount_kes={self.amount_kes})>"
    
    @property
    def amount_crypto_decimal(self) -> Optional[Decimal]:
        """Get crypto amount as Decimal."""
        return Decimal(str(self.amount_crypto)) if self.amount_crypto else None
    
    @property
    def amount_kes_decimal(self) -> Optional[Decimal]:
        """Get KES amount as Decimal."""
        return Decimal(str(self.amount_kes)) if self.amount_kes else None
    
    @property
    def amount_usd_decimal(self) -> Optional[Decimal]:
        """Get USD amount as Decimal."""
        return Decimal(str(self.amount_usd)) if self.amount_usd else None
    
    @property
    def network_fee_decimal(self) -> Optional[Decimal]:
        """Get network fee as Decimal."""
        return Decimal(str(self.network_fee)) if self.network_fee else None
    
    @property
    def platform_fee_decimal(self) -> Optional[Decimal]:
        """Get platform fee as Decimal."""
        return Decimal(str(self.platform_fee)) if self.platform_fee else None
    
    @property
    def total_fee_decimal(self) -> Optional[Decimal]:
        """Get total fee as Decimal."""
        return Decimal(str(self.total_fee)) if self.total_fee else None
    
    @property
    def is_pending(self) -> bool:
        """Check if transaction is pending."""
        return self.status == TransactionStatus.PENDING
    
    @property
    def is_processing(self) -> bool:
        """Check if transaction is processing."""
        return self.status in [TransactionStatus.PROCESSING, TransactionStatus.CONFIRMING]
    
    @property
    def is_completed(self) -> bool:
        """Check if transaction is completed."""
        return self.status in [TransactionStatus.CONFIRMED, TransactionStatus.COMPLETED]
    
    @property
    def is_failed(self) -> bool:
        """Check if transaction failed."""
        return self.status in [TransactionStatus.FAILED, TransactionStatus.CANCELLED, TransactionStatus.EXPIRED]
    
    @property
    def is_crypto_transaction(self) -> bool:
        """Check if this is a crypto transaction."""
        return self.payment_method in [
            PaymentMethod.BITCOIN,
            PaymentMethod.USDT_ETHEREUM,
            PaymentMethod.USDT_TRON
        ]
    
    @property
    def is_fiat_transaction(self) -> bool:
        """Check if this is a fiat transaction."""
        return self.payment_method in [PaymentMethod.MPESA, PaymentMethod.BANK_TRANSFER]
    
    @property
    def requires_blockchain_confirmation(self) -> bool:
        """Check if transaction requires blockchain confirmation."""
        return self.is_crypto_transaction and self.blockchain_hash is not None
    
    @property
    def is_fully_confirmed(self) -> bool:
        """Check if transaction has enough confirmations."""
        return self.confirmations >= self.required_confirmations
    
    @property
    def can_retry(self) -> bool:
        """Check if transaction can be retried."""
        return (
            self.status == TransactionStatus.FAILED and
            self.retry_count < self.max_retries
        )
    
    @property
    def is_expired(self) -> bool:
        """Check if transaction is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def short_hash(self) -> Optional[str]:
        """Get shortened blockchain hash for display."""
        if not self.blockchain_hash:
            return None
        if len(self.blockchain_hash) > 10:
            return f"{self.blockchain_hash[:6]}...{self.blockchain_hash[-4:]}"
        return self.blockchain_hash
    
    def update_status(self, new_status: TransactionStatus, error_message: str = None):
        """
        Update transaction status with timestamp tracking.
        
        Args:
            new_status: New transaction status
            error_message: Error message if status is failed
        """
        old_status = self.status
        self.status = new_status
        
        now = datetime.utcnow()
        
        if new_status == TransactionStatus.PROCESSING and old_status == TransactionStatus.PENDING:
            self.processed_at = now
        elif new_status == TransactionStatus.CONFIRMED and not self.is_completed:
            self.confirmed_at = now
        elif new_status == TransactionStatus.COMPLETED:
            self.completed_at = now
        elif new_status in [TransactionStatus.FAILED, TransactionStatus.CANCELLED]:
            if error_message:
                self.error_message = error_message
        
        self.updated_at = now
    
    def update_blockchain_info(self, tx_hash: str, block_number: str = None, confirmations: int = 0):
        """
        Update blockchain transaction information.
        
        Args:
            tx_hash: Blockchain transaction hash
            block_number: Block number
            confirmations: Number of confirmations
        """
        self.blockchain_hash = tx_hash
        if block_number:
            self.block_number = block_number
        self.confirmations = confirmations
        
        # Update status based on confirmations
        if confirmations > 0 and self.status == TransactionStatus.PROCESSING:
            self.update_status(TransactionStatus.CONFIRMING)
        elif self.is_fully_confirmed and self.status == TransactionStatus.CONFIRMING:
            self.update_status(TransactionStatus.CONFIRMED)
    
    def increment_retry_count(self):
        """Increment retry counter."""
        self.retry_count += 1
    
    def set_error(self, error_code: str, error_message: str):
        """
        Set transaction error information.
        
        Args:
            error_code: Error code
            error_message: Error message
        """
        self.error_code = error_code
        self.error_message = error_message
        self.update_status(TransactionStatus.FAILED, error_message)
    
    def calculate_total_amount_kes(self) -> Decimal:
        """
        Calculate total amount in KES including fees.
        
        Returns:
            Decimal: Total amount in KES
        """
        total = self.amount_kes_decimal or Decimal('0')
        if self.platform_fee_decimal:
            total += self.platform_fee_decimal
        return total
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert transaction to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            dict: Transaction data
        """
        data = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "wallet_id": str(self.wallet_id) if self.wallet_id else None,
            "merchant_id": str(self.merchant_id) if self.merchant_id else None,
            "transaction_type": self.transaction_type.value,
            "status": self.status.value,
            "payment_method": self.payment_method.value if self.payment_method else None,
            "reference_number": self.reference_number,
            "amount_crypto": str(self.amount_crypto_decimal) if self.amount_crypto_decimal else None,
            "amount_kes": str(self.amount_kes_decimal) if self.amount_kes_decimal else None,
            "amount_usd": str(self.amount_usd_decimal) if self.amount_usd_decimal else None,
            "network_fee": str(self.network_fee_decimal) if self.network_fee_decimal else None,
            "platform_fee": str(self.platform_fee_decimal) if self.platform_fee_decimal else None,
            "total_fee": str(self.total_fee_decimal) if self.total_fee_decimal else None,
            "blockchain_hash": self.blockchain_hash,
            "short_hash": self.short_hash,
            "confirmations": self.confirmations,
            "required_confirmations": self.required_confirmations,
            "is_fully_confirmed": self.is_fully_confirmed,
            "description": self.description,
            "initiated_at": self.initiated_at.isoformat() if self.initiated_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_sensitive:
            data.update({
                "from_address": self.from_address,
                "to_address": self.to_address,
                "mpesa_reference": self.mpesa_reference,
                "mpesa_phone_number": self.mpesa_phone_number,
                "bill_provider": self.bill_provider,
                "bill_account_number": self.bill_account_number,
                "error_code": self.error_code,
                "error_message": self.error_message,
                "retry_count": self.retry_count,
                "client_ip": self.client_ip,
                "extra_data": self.extra_data,
            })
        
        return data
    
    def get_status_history(self) -> Dict[str, Any]:
        """
        Get transaction status history with timestamps.
        
        Returns:
            dict: Status history
        """
        return {
            "initiated": self.initiated_at.isoformat() if self.initiated_at else None,
            "processed": self.processed_at.isoformat() if self.processed_at else None,
            "confirmed": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "completed": self.completed_at.isoformat() if self.completed_at else None,
            "current_status": self.status.value,
            "confirmations": f"{self.confirmations}/{self.required_confirmations}" if self.requires_blockchain_confirmation else None,
        }