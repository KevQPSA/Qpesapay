"""
Value Objects for QPesaPay domain.
Following Sandi Metz principles: small, focused, immutable objects.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional
import re
from dataclasses import dataclass
from enum import Enum


class Currency(str, Enum):
    """Supported currencies."""
    USD = "USD"
    KES = "KES"
    BTC = "BTC"
    USDT = "USDT"


@dataclass(frozen=True)
class Money:
    """
    Value object for monetary amounts.
    Immutable, handles currency conversion and formatting.
    """
    amount: Decimal
    currency: Currency

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))

    def add(self, other: 'Money') -> 'Money':
        """Add two Money objects of the same currency."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency.value} and {other.currency.value}")
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: 'Money') -> 'Money':
        """Subtract two Money objects of the same currency."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {other.currency.value} from {self.currency.value}")
        result_amount = self.amount - other.amount
        if result_amount < 0:
            raise ValueError("Subtraction would result in negative amount")
        return Money(result_amount, self.currency)

    def multiply(self, factor: Decimal) -> 'Money':
        """Multiply money by a factor."""
        if factor < 0:
            raise ValueError("Cannot multiply by negative factor")
        return Money(self.amount * factor, self.currency)

    def convert_to(self, target_currency: Currency, exchange_rate: Decimal) -> 'Money':
        """Convert to another currency using exchange rate."""
        if self.currency == target_currency:
            return self
        converted_amount = self.amount * exchange_rate
        return Money(converted_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), target_currency)

    def format(self) -> str:
        """Format money for display."""
        if self.currency in [Currency.USD, Currency.KES]:
            return f"{self.currency.value} {self.amount:.2f}"
        else:
            return f"{self.amount:.8f} {self.currency.value}"

    def is_zero(self) -> bool:
        """Check if amount is zero."""
        return self.amount == Decimal('0')

    def __str__(self) -> str:
        return self.format()


@dataclass(frozen=True)
class PhoneNumber:
    """
    Value object for Kenyan phone numbers.
    Validates and normalizes phone number format.
    """
    number: str

    def __post_init__(self):
        normalized = self._normalize(self.number)
        if not self._is_valid_kenyan_number(normalized):
            raise ValueError(f"Invalid Kenyan phone number: {self.number}")
        object.__setattr__(self, 'number', normalized)

    def _normalize(self, number: str) -> str:
        """Normalize phone number to +254 format."""
        # Remove all non-digits
        digits = re.sub(r'\D', '', number)

        # Handle different formats
        if digits.startswith('254'):
            return f"+{digits}"
        elif digits.startswith('0') and len(digits) == 10:
            return f"+254{digits[1:]}"
        elif len(digits) == 9:
            return f"+254{digits}"
        else:
            return f"+{digits}"

    def _is_valid_kenyan_number(self, number: str) -> bool:
        """Validate Kenyan phone number format."""
        pattern = r'^\+254[17]\d{8}$'
        return bool(re.match(pattern, number))

    def format_local(self) -> str:
        """Format as local number (0xxx xxx xxx)."""
        if self.number.startswith('+254'):
            return f"0{self.number[4:]}"
        return self.number

    def format_international(self) -> str:
        """Format as international number (+254 xxx xxx xxx)."""
        return self.number

    def __str__(self) -> str:
        return self.number


@dataclass(frozen=True)
class EmailAddress:
    """
    Value object for email addresses.
    Validates and normalizes email format.
    """
    email: str

    def __post_init__(self):
        normalized = self._normalize(self.email)
        if not self._is_valid_email(normalized):
            raise ValueError(f"Invalid email address: {self.email}")
        object.__setattr__(self, 'email', normalized)

    def _normalize(self, email: str) -> str:
        """Normalize email to lowercase."""
        return email.strip().lower()

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def domain(self) -> str:
        """Get email domain."""
        return self.email.split('@')[1]

    def local_part(self) -> str:
        """Get local part of email."""
        return self.email.split('@')[0]

    def __str__(self) -> str:
        return self.email


@dataclass(frozen=True)
class Address:
    """
    Value object for blockchain addresses.
    Validates address format for different networks.
    """
    address: str
    network: str

    def __post_init__(self):
        if not self._is_valid_address():
            raise ValueError(f"Invalid {self.network} address: {self.address}")

    def _is_valid_address(self) -> bool:
        """Validate address format based on network."""
        if self.network.lower() == 'ethereum':
            return self._is_valid_ethereum_address()
        elif self.network.lower() == 'tron':
            return self._is_valid_tron_address()
        elif self.network.lower() == 'bitcoin':
            return self._is_valid_bitcoin_address()
        return False

    def _is_valid_ethereum_address(self) -> bool:
        """Validate Ethereum address format."""
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, self.address))

    def _is_valid_tron_address(self) -> bool:
        """Validate Tron address format."""
        pattern = r'^T[A-Za-z1-9]{33}$'
        return bool(re.match(pattern, self.address))

    def _is_valid_bitcoin_address(self) -> bool:
        """Validate Bitcoin address format (simplified)."""
        # This is a simplified validation - in production use proper Bitcoin address validation
        return len(self.address) >= 26 and len(self.address) <= 35

    def format_short(self) -> str:
        """Format address for display (first 6 + ... + last 4)."""
        if len(self.address) <= 10:
            return self.address
        return f"{self.address[:6]}...{self.address[-4:]}"

    def __str__(self) -> str:
        return self.address