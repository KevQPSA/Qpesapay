"""
🟢 Production Ready: Domain Value Objects for Qpesapay

This example demonstrates proper value object implementation following
Domain-Driven Design principles and Sandi Metz guidelines for financial systems.

Key Patterns:
- Immutable value objects
- Proper validation in constructors
- Decimal precision for monetary values
- Currency-specific formatting
- Equality and hashing implementation
- Defensive programming for financial data
"""

from decimal import Decimal, ROUND_HALF_EVEN
from typing import Union, Optional
from dataclasses import dataclass
from enum import Enum
import re
from uuid import UUID, uuid4


class Currency(Enum):
    """Supported currencies in Qpesapay."""
    BTC = "BTC"
    USDT = "USDT"
    KES = "KES"
    USD = "USD"


@dataclass(frozen=True)
class Money:
    """
    🟢 Production Ready: Immutable money value object.
    
    Handles monetary values with proper decimal precision and currency validation.
    Never uses float for financial calculations - always Decimal.
    
    Key Features:
    - Immutable (frozen dataclass)
    - Decimal precision based on currency
    - Proper rounding for financial calculations
    - Currency-specific validation
    - Safe arithmetic operations
    """
    
    value: Decimal
    currency: Currency
    
    def __post_init__(self):
        """Validate money object after initialization."""
        if not isinstance(self.value, Decimal):
            # Convert to Decimal if not already
            object.__setattr__(self, 'value', Decimal(str(self.value)))
        
        if self.value < 0:
            raise ValueError("Money value cannot be negative")
        
        # Apply currency-specific precision
        precision = self._get_currency_precision()
        rounded_value = self.value.quantize(precision, rounding=ROUND_HALF_EVEN)
        object.__setattr__(self, 'value', rounded_value)
    
    def _get_currency_precision(self) -> Decimal:
        """Get decimal precision for currency."""
        precision_map = {
            Currency.BTC: Decimal('0.00000001'),    # 8 decimal places (satoshis)
            Currency.USDT: Decimal('0.000001'),     # 6 decimal places
            Currency.KES: Decimal('0.01'),          # 2 decimal places (cents)
            Currency.USD: Decimal('0.01'),          # 2 decimal places (cents)
        }
        return precision_map[self.currency]
    
    def add(self, other: 'Money') -> 'Money':
        """
        Add two money amounts with currency validation.
        
        Args:
            other: Money amount to add
            
        Returns:
            Money: Sum of the two amounts
            
        Raises:
            ValueError: If currencies don't match
        """
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        
        return Money(self.value + other.value, self.currency)
    
    def subtract(self, other: 'Money') -> 'Money':
        """Subtract two money amounts with currency validation."""
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {other.currency} from {self.currency}")
        
        result_value = self.value - other.value
        if result_value < 0:
            raise ValueError("Subtraction would result in negative amount")
        
        return Money(result_value, self.currency)
    
    def multiply(self, factor: Union[Decimal, int, float]) -> 'Money':
        """Multiply money by a factor."""
        if not isinstance(factor, Decimal):
            factor = Decimal(str(factor))
        
        return Money(self.value * factor, self.currency)
    
    def divide(self, divisor: Union[Decimal, int, float]) -> 'Money':
        """Divide money by a divisor."""
        if not isinstance(divisor, Decimal):
            divisor = Decimal(str(divisor))
        
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        
        return Money(self.value / divisor, self.currency)
    
    def is_zero(self) -> bool:
        """Check if money amount is zero."""
        return self.value == 0
    
    def is_positive(self) -> bool:
        """Check if money amount is positive."""
        return self.value > 0
    
    def format(self) -> str:
        """Format money for display."""
        if self.currency == Currency.BTC:
            return f"₿{self.value:.8f}"
        elif self.currency == Currency.USDT:
            return f"${self.value:.6f} USDT"
        elif self.currency == Currency.KES:
            return f"KSh {self.value:.2f}"
        elif self.currency == Currency.USD:
            return f"${self.value:.2f}"
        else:
            return f"{self.value} {self.currency.value}"
    
    def __str__(self) -> str:
        return self.format()


@dataclass(frozen=True)
class PhoneNumber:
    """
    🟢 Production Ready: Phone number value object for Kenyan market.
    
    Validates and formats Kenyan phone numbers according to Safaricom standards.
    Provides masking for privacy and logging.
    """
    
    value: str
    
    def __post_init__(self):
        """Validate phone number format."""
        if not self._is_valid_kenyan_phone(self.value):
            raise ValueError(f"Invalid Kenyan phone number: {self.value}")
    
    @staticmethod
    def _is_valid_kenyan_phone(phone: str) -> bool:
        """Validate Kenyan phone number format."""
        # Kenyan phone pattern: +254XXXXXXXXX
        pattern = r'^\+254[17]\d{8}$'
        return bool(re.match(pattern, phone))
    
    @property
    def masked(self) -> str:
        """Return masked phone number for logging/display."""
        if len(self.value) >= 8:
            return f"{self.value[:4]}****{self.value[-4:]}"
        return "****"
    
    @property
    def local_format(self) -> str:
        """Return phone number in local format (0XXXXXXXXX)."""
        return f"0{self.value[4:]}"
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Address:
    """
    🟢 Production Ready: Address value object for KYC and compliance.
    
    Handles address validation and formatting for Kenyan addresses.
    """
    
    street: str
    city: str
    county: str
    postal_code: Optional[str] = None
    country: str = "Kenya"
    
    def __post_init__(self):
        """Validate address components."""
        if not self.street.strip():
            raise ValueError("Street address is required")
        
        if not self.city.strip():
            raise ValueError("City is required")
        
        if not self.county.strip():
            raise ValueError("County is required")
        
        # Validate Kenyan postal code format if provided
        if self.postal_code and not self._is_valid_postal_code(self.postal_code):
            raise ValueError(f"Invalid postal code: {self.postal_code}")
    
    @staticmethod
    def _is_valid_postal_code(postal_code: str) -> bool:
        """Validate Kenyan postal code format."""
        # Kenyan postal codes are typically 5 digits
        return bool(re.match(r'^\d{5}$', postal_code))
    
    def format_single_line(self) -> str:
        """Format address as single line."""
        parts = [self.street, self.city, self.county]
        if self.postal_code:
            parts.append(self.postal_code)
        parts.append(self.country)
        return ", ".join(parts)
    
    def __str__(self) -> str:
        return self.format_single_line()


@dataclass(frozen=True)
class EmailAddress:
    """
    🟢 Production Ready: Email address value object with validation.
    
    Validates email format and provides normalized access.
    """
    
    value: str
    
    def __post_init__(self):
        """Validate email address format."""
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email address: {self.value}")
        
        # Normalize email (lowercase)
        object.__setattr__(self, 'value', self.value.lower().strip())
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email address format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @property
    def domain(self) -> str:
        """Extract domain from email address."""
        return self.value.split('@')[1]
    
    @property
    def local_part(self) -> str:
        """Extract local part from email address."""
        return self.value.split('@')[0]
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class TransactionId:
    """
    🟢 Production Ready: Transaction ID value object.
    
    Ensures transaction IDs are valid UUIDs for uniqueness and consistency.
    """
    
    value: str
    
    def __post_init__(self):
        """Validate transaction ID format."""
        try:
            # Validate as UUID
            UUID(self.value)
        except ValueError:
            raise ValueError(f"Invalid transaction ID format: {self.value}")
    
    @classmethod
    def generate(cls) -> 'TransactionId':
        """Generate a new transaction ID."""
        return cls(str(uuid4()))
    
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class WalletAddress:
    """
    🟢 Production Ready: Cryptocurrency wallet address value object.
    
    Validates wallet addresses for different blockchain networks.
    """
    
    address: str
    network: str  # "bitcoin", "ethereum", "tron"
    
    def __post_init__(self):
        """Validate wallet address format."""
        if not self._is_valid_address():
            raise ValueError(f"Invalid {self.network} address: {self.address}")
    
    def _is_valid_address(self) -> bool:
        """Validate address format based on network."""
        if self.network == "bitcoin":
            return self._is_valid_bitcoin_address()
        elif self.network == "ethereum":
            return self._is_valid_ethereum_address()
        elif self.network == "tron":
            return self._is_valid_tron_address()
        else:
            raise ValueError(f"Unsupported network: {self.network}")
    
    def _is_valid_bitcoin_address(self) -> bool:
        """Validate Bitcoin address format."""
        # Bitcoin addresses start with 1, 3, or bc1
        patterns = [
            r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',  # Legacy and P2SH
            r'^bc1[a-z0-9]{39,59}$'                # Bech32
        ]
        return any(re.match(pattern, self.address) for pattern in patterns)
    
    def _is_valid_ethereum_address(self) -> bool:
        """Validate Ethereum address format."""
        # Ethereum addresses are 42 characters starting with 0x
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, self.address))
    
    def _is_valid_tron_address(self) -> bool:
        """Validate Tron address format."""
        # Tron addresses start with T and are 34 characters
        pattern = r'^T[a-zA-Z0-9]{33}$'
        return bool(re.match(pattern, self.address))
    
    @property
    def short_format(self) -> str:
        """Return shortened address for display."""
        if len(self.address) > 12:
            return f"{self.address[:6]}...{self.address[-6:]}"
        return self.address
    
    def __str__(self) -> str:
        return self.address


# Example usage patterns
def example_value_object_usage():
    """
    Example of how to use value objects in Qpesapay.
    This demonstrates proper patterns for financial value objects.
    """
    # Money calculations with proper decimal precision
    usdt_amount = Money(Decimal("100.123456"), Currency.USDT)
    kes_amount = Money(Decimal("13500.50"), Currency.KES)
    
    # Phone number validation
    phone = PhoneNumber("+254712345678")
    print(f"Phone: {phone}, Masked: {phone.masked}")
    
    # Address for KYC
    address = Address(
        street="123 Kenyatta Avenue",
        city="Nairobi",
        county="Nairobi",
        postal_code="00100"
    )
    
    # Email validation
    email = EmailAddress("user@example.com")
    
    # Transaction ID generation
    tx_id = TransactionId.generate()
    
    # Wallet address validation
    btc_address = WalletAddress(
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "bitcoin"
    )
    
    return {
        "usdt_amount": usdt_amount,
        "kes_amount": kes_amount,
        "phone": phone,
        "address": address,
        "email": email,
        "transaction_id": tx_id,
        "btc_address": btc_address
    }
