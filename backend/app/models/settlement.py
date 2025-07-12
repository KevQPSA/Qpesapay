"""
Settlement model for Qpesapay backend.
Handles automatic settlement of merchant payments to fiat currency.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum, Index, ForeignKey, NUMERIC, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any, List

from app.models.base import Base


class SettlementStatus(str, enum.Enum):
    """Settlement status."""
    PENDING = "pending"                    # Settlement initiated
    PROCESSING = "processing"              # Being processed
    COMPLETED = "completed"                # Successfully completed
    FAILED = "failed"                      # Settlement failed
    CANCELLED = "cancelled"                # Settlement cancelled
    REFUNDED = "refunded"                  # Settlement refunded


class SettlementType(str, enum.Enum):
    """Settlement types."""
    AUTOMATIC = "automatic"                # Automatic settlement
    MANUAL = "manual"                      # Manual settlement
    BATCH = "batch"                        # Batch settlement
    INSTANT = "instant"                    # Instant settlement


class Settlement(Base):
    """
    Settlement model for merchant payment settlements.
    
    Handles the conversion and transfer of crypto payments to fiat currency
    for merchants via M-Pesa, bank transfers, or crypto wallets.
    """
    __tablename__ = "settlements"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    merchant_id = Column(UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False, index=True)
    
    # Settlement identification
    settlement_type = Column(Enum(SettlementType), nullable=False, default=SettlementType.AUTOMATIC)
    status = Column(Enum(SettlementStatus), nullable=False, default=SettlementStatus.PENDING, index=True)
    reference_number = Column(String(100), nullable=False, unique=True, index=True)
    
    # External references
    external_reference = Column(String(255), nullable=True, unique=True, index=True)  # M-Pesa/Bank reference
    batch_id = Column(String(100), nullable=True, index=True)  # For batch settlements
    
    # Amount information (using NUMERIC for precise decimal handling)
    gross_amount_kes = Column(NUMERIC(20, 2), nullable=False)      # Total amount before fees
    settlement_fee = Column(NUMERIC(20, 2), nullable=False)        # Settlement fee
    net_amount_kes = Column(NUMERIC(20, 2), nullable=False)        # Amount after fees
    
    # Original crypto amounts (for reference)
    original_crypto_amount = Column(NUMERIC(20, 8), nullable=True)
    original_crypto_currency = Column(String(10), nullable=True)   # BTC, USDT
    exchange_rate_used = Column(NUMERIC(15, 8), nullable=True)     # Exchange rate at settlement
    
    # Settlement method details
    settlement_method = Column(String(50), nullable=False)         # mpesa, bank_transfer, crypto_wallet
    
    # M-Pesa specific fields
    mpesa_phone_number = Column(String(20), nullable=True)
    mpesa_transaction_id = Column(String(100), nullable=True)
    mpesa_receipt_number = Column(String(100), nullable=True)
    
    # Bank transfer specific fields
    bank_name = Column(String(100), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_account_name = Column(String(255), nullable=True)
    bank_reference = Column(String(100), nullable=True)
    
    # Crypto wallet specific fields
    crypto_wallet_address = Column(String(255), nullable=True)
    crypto_network = Column(String(50), nullable=True)
    crypto_transaction_hash = Column(String(255), nullable=True)
    
    # Transaction aggregation (settlements can include multiple transactions)
    transaction_count = Column(Integer, default=1, nullable=False)
    transaction_ids = Column(Text, nullable=True)                  # JSON array of transaction IDs
    settlement_period_start = Column(DateTime, nullable=True)
    settlement_period_end = Column(DateTime, nullable=True)
    
    # Timing information
    scheduled_at = Column(DateTime, nullable=True)                 # When settlement was scheduled
    initiated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Error handling
    error_code = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    next_retry_at = Column(DateTime, nullable=True)
    
    # Metadata
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    extra_data = Column(Text, nullable=True)                         # JSON string for additional data
    
    # Audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String(100), nullable=True)               # System, Admin, etc.
    
    # Relationships
    merchant = relationship("Merchant", back_populates="settlements")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_settlements_merchant_status', 'merchant_id', 'status'),
        Index('idx_settlements_status_created', 'status', 'created_at'),
        Index('idx_settlements_reference', 'reference_number'),
        Index('idx_settlements_external_ref', 'external_reference'),
        Index('idx_settlements_scheduled', 'scheduled_at'),
        Index('idx_settlements_batch', 'batch_id'),
        Index('idx_settlements_method', 'settlement_method'),
    )
    
    def __repr__(self):
        return f"<Settlement(id={self.id}, merchant_id={self.merchant_id}, status={self.status}, amount={self.net_amount_kes})>"
    
    @property
    def gross_amount_kes_decimal(self) -> Decimal:
        """Get gross amount as Decimal."""
        return Decimal(str(self.gross_amount_kes))
    
    @property
    def settlement_fee_decimal(self) -> Decimal:
        """Get settlement fee as Decimal."""
        return Decimal(str(self.settlement_fee))
    
    @property
    def net_amount_kes_decimal(self) -> Decimal:
        """Get net amount as Decimal."""
        return Decimal(str(self.net_amount_kes))
    
    @property
    def original_crypto_amount_decimal(self) -> Optional[Decimal]:
        """Get original crypto amount as Decimal."""
        return Decimal(str(self.original_crypto_amount)) if self.original_crypto_amount else None
    
    @property
    def exchange_rate_used_decimal(self) -> Optional[Decimal]:
        """Get exchange rate as Decimal."""
        return Decimal(str(self.exchange_rate_used)) if self.exchange_rate_used else None
    
    @property
    def is_pending(self) -> bool:
        """Check if settlement is pending."""
        return self.status == SettlementStatus.PENDING
    
    @property
    def is_processing(self) -> bool:
        """Check if settlement is processing."""
        return self.status == SettlementStatus.PROCESSING
    
    @property
    def is_completed(self) -> bool:
        """Check if settlement is completed."""
        return self.status == SettlementStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        """Check if settlement failed."""
        return self.status in [SettlementStatus.FAILED, SettlementStatus.CANCELLED]
    
    @property
    def can_retry(self) -> bool:
        """Check if settlement can be retried."""
        return (
            self.status == SettlementStatus.FAILED and
            self.retry_count < self.max_retries
        )
    
    @property
    def is_mpesa_settlement(self) -> bool:
        """Check if this is an M-Pesa settlement."""
        return self.settlement_method == "mpesa"
    
    @property
    def is_bank_settlement(self) -> bool:
        """Check if this is a bank transfer settlement."""
        return self.settlement_method == "bank_transfer"
    
    @property
    def is_crypto_settlement(self) -> bool:
        """Check if this is a crypto wallet settlement."""
        return self.settlement_method == "crypto_wallet"
    
    @property
    def settlement_duration(self) -> Optional[int]:
        """Get settlement duration in seconds."""
        if self.completed_at and self.initiated_at:
            return int((self.completed_at - self.initiated_at).total_seconds())
        return None
    
    @property
    def fee_percentage(self) -> Decimal:
        """Calculate fee percentage."""
        if self.gross_amount_kes_decimal > 0:
            return (self.settlement_fee_decimal / self.gross_amount_kes_decimal) * Decimal('100')
        return Decimal('0')
    
    def update_status(self, new_status: SettlementStatus, error_message: str = None, external_ref: str = None):
        """
        Update settlement status with timestamp tracking.
        
        Args:
            new_status: New settlement status
            error_message: Error message if status is failed
            external_ref: External reference (M-Pesa/bank reference)
        """
        old_status = self.status
        self.status = new_status
        
        now = datetime.utcnow()
        
        if new_status == SettlementStatus.PROCESSING and old_status == SettlementStatus.PENDING:
            self.processed_at = now
        elif new_status == SettlementStatus.COMPLETED:
            self.completed_at = now
            if external_ref:
                self.external_reference = external_ref
        elif new_status == SettlementStatus.FAILED:
            if error_message:
                self.error_message = error_message
        
        self.updated_at = now
    
    def set_mpesa_details(self, phone_number: str, transaction_id: str = None, receipt_number: str = None):
        """
        Set M-Pesa settlement details.
        
        Args:
            phone_number: M-Pesa phone number
            transaction_id: M-Pesa transaction ID
            receipt_number: M-Pesa receipt number
        """
        self.mpesa_phone_number = phone_number
        if transaction_id:
            self.mpesa_transaction_id = transaction_id
        if receipt_number:
            self.mpesa_receipt_number = receipt_number
    
    def set_bank_details(self, bank_name: str, account_number: str, account_name: str, reference: str = None):
        """
        Set bank transfer settlement details.
        
        Args:
            bank_name: Bank name
            account_number: Account number
            account_name: Account holder name
            reference: Bank reference
        """
        self.bank_name = bank_name
        self.bank_account_number = account_number
        self.bank_account_name = account_name
        if reference:
            self.bank_reference = reference
    
    def set_crypto_details(self, wallet_address: str, network: str, transaction_hash: str = None):
        """
        Set crypto wallet settlement details.
        
        Args:
            wallet_address: Crypto wallet address
            network: Blockchain network
            transaction_hash: Transaction hash
        """
        self.crypto_wallet_address = wallet_address
        self.crypto_network = network
        if transaction_hash:
            self.crypto_transaction_hash = transaction_hash
    
    def increment_retry_count(self):
        """Increment retry counter and set next retry time."""
        self.retry_count += 1
        
        # Exponential backoff: 5 minutes, 15 minutes, 45 minutes
        retry_delays = [300, 900, 2700]  # seconds
        if self.retry_count <= len(retry_delays):
            delay = retry_delays[self.retry_count - 1]
            self.next_retry_at = datetime.utcnow() + datetime.timedelta(seconds=delay)
    
    def set_error(self, error_code: str, error_message: str):
        """
        Set settlement error information.
        
        Args:
            error_code: Error code
            error_message: Error message
        """
        self.error_code = error_code
        self.error_message = error_message
        self.update_status(SettlementStatus.FAILED, error_message)
    
    def add_transaction_ids(self, transaction_ids: List[str]):
        """
        Add transaction IDs to settlement.
        
        Args:
            transaction_ids: List of transaction IDs
        """
        import json
        self.transaction_ids = json.dumps(transaction_ids)
        self.transaction_count = len(transaction_ids)
    
    def get_transaction_ids(self) -> List[str]:
        """
        Get list of transaction IDs in this settlement.
        
        Returns:
            List of transaction IDs
        """
        if not self.transaction_ids:
            return []
        
        try:
            import json
            return json.loads(self.transaction_ids)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def calculate_effective_rate(self) -> Optional[Decimal]:
        """
        Calculate effective exchange rate including fees.
        
        Returns:
            Decimal: Effective rate (KES per crypto unit)
        """
        if not self.original_crypto_amount_decimal or self.original_crypto_amount_decimal == 0:
            return None
        
        return self.net_amount_kes_decimal / self.original_crypto_amount_decimal
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        Convert settlement to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive fields
            
        Returns:
            dict: Settlement data
        """
        data = {
            "id": str(self.id),
            "merchant_id": str(self.merchant_id),
            "settlement_type": self.settlement_type.value,
            "status": self.status.value,
            "reference_number": self.reference_number,
            "external_reference": self.external_reference,
            "gross_amount_kes": str(self.gross_amount_kes_decimal),
            "settlement_fee": str(self.settlement_fee_decimal),
            "net_amount_kes": str(self.net_amount_kes_decimal),
            "fee_percentage": f"{float(self.fee_percentage):.2f}%",
            "settlement_method": self.settlement_method,
            "transaction_count": self.transaction_count,
            "settlement_duration": self.settlement_duration,
            "initiated_at": self.initiated_at.isoformat() if self.initiated_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_sensitive:
            data.update({
                "original_crypto_amount": str(self.original_crypto_amount_decimal) if self.original_crypto_amount_decimal else None,
                "original_crypto_currency": self.original_crypto_currency,
                "exchange_rate_used": str(self.exchange_rate_used_decimal) if self.exchange_rate_used_decimal else None,
                "effective_rate": str(self.calculate_effective_rate()) if self.calculate_effective_rate() else None,
                "mpesa_phone_number": self.mpesa_phone_number,
                "mpesa_transaction_id": self.mpesa_transaction_id,
                "mpesa_receipt_number": self.mpesa_receipt_number,
                "bank_name": self.bank_name,
                "bank_account_number": self.bank_account_number,
                "bank_account_name": self.bank_account_name,
                "bank_reference": self.bank_reference,
                "crypto_wallet_address": self.crypto_wallet_address,
                "crypto_network": self.crypto_network,
                "crypto_transaction_hash": self.crypto_transaction_hash,
                "transaction_ids": self.get_transaction_ids(),
                "error_code": self.error_code,
                "error_message": self.error_message,
                "retry_count": self.retry_count,
                "next_retry_at": self.next_retry_at.isoformat() if self.next_retry_at else None,
                "extra_data": self.extra_data,
            })
        
        return data
    
    def get_settlement_details(self) -> Dict[str, Any]:
        """
        Get settlement method specific details.
        
        Returns:
            dict: Settlement details
        """
        details = {
            "method": self.settlement_method,
            "status": self.status.value,
            "reference": self.reference_number,
            "external_reference": self.external_reference,
        }
        
        if self.is_mpesa_settlement:
            details.update({
                "phone_number": self.mpesa_phone_number,
                "transaction_id": self.mpesa_transaction_id,
                "receipt_number": self.mpesa_receipt_number,
            })
        elif self.is_bank_settlement:
            details.update({
                "bank_name": self.bank_name,
                "account_number": self.bank_account_number,
                "account_name": self.bank_account_name,
                "bank_reference": self.bank_reference,
            })
        elif self.is_crypto_settlement:
            details.update({
                "wallet_address": self.crypto_wallet_address,
                "network": self.crypto_network,
                "transaction_hash": self.crypto_transaction_hash,
            })
        
        return details
    
    def get_status_history(self) -> Dict[str, Any]:
        """
        Get settlement status history with timestamps.
        
        Returns:
            dict: Status history
        """
        return {
            "initiated": self.initiated_at.isoformat() if self.initiated_at else None,
            "processed": self.processed_at.isoformat() if self.processed_at else None,
            "completed": self.completed_at.isoformat() if self.completed_at else None,
            "current_status": self.status.value,
            "duration_seconds": self.settlement_duration,
            "retry_count": self.retry_count,
            "can_retry": self.can_retry,
        }