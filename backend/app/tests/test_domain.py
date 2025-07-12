"""
Tests for Domain Layer.
Testing value objects and entities following Sandi Metz principles.
"""

import pytest
from decimal import Decimal
from uuid import uuid4

from app.domain import Money, Currency, PhoneNumber, EmailAddress, Address
from app.domain import PaymentRequest, TransactionRecord, UserProfile


class TestMoney:
    """Test Money value object."""

    def test_money_creation(self):
        """Test money creation with valid values."""
        money = Money(Decimal('100.50'), Currency.USD)
        assert money.amount == Decimal('100.50')
        assert money.currency == Currency.USD

    def test_money_negative_amount_raises_error(self):
        """Test that negative amounts raise ValueError."""
        with pytest.raises(ValueError, match="Money amount cannot be negative"):
            Money(Decimal('-10'), Currency.USD)

    def test_money_addition_same_currency(self):
        """Test adding money of same currency."""
        money1 = Money(Decimal('100'), Currency.USD)
        money2 = Money(Decimal('50'), Currency.USD)
        result = money1.add(money2)

        assert result.amount == Decimal('150')
        assert result.currency == Currency.USD

    def test_money_addition_different_currency_raises_error(self):
        """Test that adding different currencies raises error."""
        money1 = Money(Decimal('100'), Currency.USD)
        money2 = Money(Decimal('50'), Currency.KES)

        with pytest.raises(ValueError, match="Cannot add USD and KES"):
            money1.add(money2)

    def test_money_subtraction(self):
        """Test money subtraction."""
        money1 = Money(Decimal('100'), Currency.USD)
        money2 = Money(Decimal('30'), Currency.USD)
        result = money1.subtract(money2)

        assert result.amount == Decimal('70')
        assert result.currency == Currency.USD

    def test_money_subtraction_negative_result_raises_error(self):
        """Test that subtraction resulting in negative raises error."""
        money1 = Money(Decimal('50'), Currency.USD)
        money2 = Money(Decimal('100'), Currency.USD)

        with pytest.raises(ValueError, match="Subtraction would result in negative amount"):
            money1.subtract(money2)

    def test_money_multiplication(self):
        """Test money multiplication."""
        money = Money(Decimal('100'), Currency.USD)
        result = money.multiply(Decimal('1.5'))

        assert result.amount == Decimal('150')
        assert result.currency == Currency.USD

    def test_money_conversion(self):
        """Test currency conversion."""
        usd_money = Money(Decimal('100'), Currency.USD)
        kes_money = usd_money.convert_to(Currency.KES, Decimal('150'))  # 1 USD = 150 KES

        assert kes_money.amount == Decimal('15000.00')
        assert kes_money.currency == Currency.KES

    def test_money_formatting(self):
        """Test money formatting."""
        usd_money = Money(Decimal('100.50'), Currency.USD)
        btc_money = Money(Decimal('0.00123456'), Currency.BTC)

        assert str(usd_money) == "USD 100.50"
        assert str(btc_money) == "0.00123456 BTC"

    def test_money_is_zero(self):
        """Test zero amount detection."""
        zero_money = Money(Decimal('0'), Currency.USD)
        non_zero_money = Money(Decimal('1'), Currency.USD)

        assert zero_money.is_zero() is True
        assert non_zero_money.is_zero() is False


class TestPhoneNumber:
    """Test PhoneNumber value object."""

    def test_valid_kenyan_number_formats(self):
        """Test various valid Kenyan phone number formats."""
        # Test different input formats
        formats = [
            "0712345678",
            "+254712345678",
            "254712345678",
            "712345678"
        ]

        for format_input in formats:
            phone = PhoneNumber(format_input)
            assert phone.number == "+254712345678"

    def test_invalid_kenyan_number_raises_error(self):
        """Test that invalid numbers raise ValueError."""
        invalid_numbers = [
            "0612345678",  # Invalid prefix
            "071234567",   # Too short
            "07123456789", # Too long
            "+255712345678" # Wrong country code
        ]

        for invalid in invalid_numbers:
            with pytest.raises(ValueError, match="Invalid Kenyan phone number"):
                PhoneNumber(invalid)

    def test_phone_number_formatting(self):
        """Test phone number formatting methods."""
        phone = PhoneNumber("0712345678")

        assert phone.format_local() == "0712345678"
        assert phone.format_international() == "+254712345678"
        assert str(phone) == "+254712345678"


class TestEmailAddress:
    """Test EmailAddress value object."""

    def test_valid_email_creation(self):
        """Test creating valid email addresses."""
        email = EmailAddress("user@example.com")
        assert email.email == "user@example.com"

    def test_email_normalization(self):
        """Test email normalization (lowercase)."""
        email = EmailAddress("  USER@EXAMPLE.COM  ")
        assert email.email == "user@example.com"

    def test_invalid_email_raises_error(self):
        """Test that invalid emails raise ValueError."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@.com"
        ]

        for invalid in invalid_emails:
            with pytest.raises(ValueError, match="Invalid email address"):
                EmailAddress(invalid)

    def test_email_domain_extraction(self):
        """Test domain extraction."""
        email = EmailAddress("user@example.com")
        assert email.domain() == "example.com"

    def test_email_local_part_extraction(self):
        """Test local part extraction."""
        email = EmailAddress("user@example.com")
        assert email.local_part() == "user"