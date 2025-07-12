"""
Domain Entities for QPesaPay.
Following Sandi Metz principles: focused, single-responsibility entities.
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from .value_objects import Money, Address, PhoneNumber, EmailAddress


@dataclass
class PaymentRequest:
    """
    Domain entity representing a payment request.
    Encapsulates payment business rules and validation.
    """
    id: UUID
    user_id: UUID
    amount: Money
    recipient_address: Address
    description: Optional[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def is_valid(self) -> bool:
        """Validate payment request business rules."""
        return not self.amount.is_zero()

    def calculate_fees(self, fee_rate: Money) -> Money:
        """Calculate transaction fees."""
        return self.amount.multiply(fee_rate.amount)


@dataclass
class TransactionRecord:
    """
    Domain entity for transaction records.
    Immutable record of completed transactions.
    """
    id: UUID
    payment_request_id: UUID
    blockchain_hash: Optional[str]
    status: str
    fees_paid: Money
    confirmed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()

    def is_confirmed(self) -> bool:
        """Check if transaction is confirmed."""
        return self.confirmed_at is not None

    def mark_confirmed(self) -> 'TransactionRecord':
        """Mark transaction as confirmed."""
        return TransactionRecord(
            id=self.id,
            payment_request_id=self.payment_request_id,
            blockchain_hash=self.blockchain_hash,
            status="confirmed",
            fees_paid=self.fees_paid,
            confirmed_at=datetime.utcnow()
        )


@dataclass
class UserProfile:
    """
    Domain entity for user profile information.
    Encapsulates user-related business rules.
    """
    id: UUID
    email: EmailAddress
    phone: PhoneNumber
    first_name: str
    last_name: str
    is_verified: bool = False

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()

    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def can_make_payments(self) -> bool:
        """Check if user can make payments."""
        return self.is_verified

    def verify(self) -> 'UserProfile':
        """Mark user as verified."""
        return UserProfile(
            id=self.id,
            email=self.email,
            phone=self.phone,
            first_name=self.first_name,
            last_name=self.last_name,
            is_verified=True
        )