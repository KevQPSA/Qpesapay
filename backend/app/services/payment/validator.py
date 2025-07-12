"""
Payment Validator Service.
Single responsibility: Validate payment requests.
Following Sandi Metz principles: small, focused, testable.
"""

from typing import List
from decimal import Decimal
from app.domain import PaymentRequest, Money, Currency


class ValidationError(ValueError):
    """Simple validation error for payment validation."""
    pass


class PaymentValidator:
    """
    Validates payment requests according to business rules.
    Single responsibility: payment validation only.
    """

    def validate(self, payment_request: PaymentRequest) -> None:
        """
        Validate payment request.
        Raises ValidationError if invalid.
        """
        self._validate_amount(payment_request.amount)
        self._validate_address(payment_request.recipient_address)
        self._validate_description(payment_request.description)

    def _validate_amount(self, amount: Money) -> None:
        """Validate payment amount."""
        if amount.is_zero():
            raise ValidationError("Payment amount cannot be zero")

        min_amount = self._minimum_amount(amount.currency)
        if amount.amount < min_amount.amount:
            raise ValidationError(f"Amount below minimum for {amount.currency}")

        max_amount = self._maximum_amount(amount.currency)
        if amount.amount > max_amount.amount:
            raise ValidationError(f"Amount exceeds maximum for {amount.currency}")

    def _validate_address(self, address) -> None:
        """Validate recipient address."""
        # Address validation is handled by the Address value object
        # This method can add additional business rules
        pass

    def _validate_description(self, description: str) -> None:
        """Validate payment description."""
        if description and len(description) > 500:
            raise ValidationError("Description too long (max 500 characters)")

    def _minimum_amount(self, currency: Currency) -> Money:
        """Get minimum amount for currency."""
        minimums = {
            Currency.USD: Money(Decimal('0.01'), Currency.USD),
            Currency.KES: Money(Decimal('1.00'), Currency.KES),
            Currency.BTC: Money(Decimal('0.00001'), Currency.BTC),
            Currency.USDT: Money(Decimal('0.01'), Currency.USDT),
        }
        return minimums.get(currency, Money(Decimal('0'), currency))

    def _maximum_amount(self, currency: Currency) -> Money:
        """Get maximum amount for currency."""
        maximums = {
            Currency.USD: Money(Decimal('10000.00'), Currency.USD),
            Currency.KES: Money(Decimal('1000000.00'), Currency.KES),
            Currency.BTC: Money(Decimal('1.0'), Currency.BTC),
            Currency.USDT: Money(Decimal('10000.00'), Currency.USDT),
        }
        return maximums.get(currency, Money(Decimal('999999'), currency))


class BalanceValidator:
    """
    Validates user has sufficient balance for payment.
    Single responsibility: balance validation only.
    """

    def __init__(self, balance_checker):
        self.balance_checker = balance_checker

    def validate_sufficient_balance(self, user_id: str, amount: Money) -> None:
        """
        Validate user has sufficient balance.
        Raises ValidationError if insufficient.
        """
        current_balance = self.balance_checker.get_balance(user_id, amount.currency)

        if current_balance.amount < amount.amount:
            raise ValidationError(
                f"Insufficient balance. Required: {amount}, Available: {current_balance}"
            )