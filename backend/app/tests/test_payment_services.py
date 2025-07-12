"""
Tests for Payment Services.
Testing Sandi Metz-style focused services.
"""

import pytest
from decimal import Decimal
from uuid import uuid4

from app.domain import Money, Currency, Address, PaymentRequest
from app.services.payment import PaymentValidator, FeeEstimator, StaticFeeProvider
from app.services.payment.validator import ValidationError


class TestPaymentValidator:
    """Test PaymentValidator service."""

    def test_valid_payment_passes_validation(self):
        """Test that valid payment passes validation."""
        validator = PaymentValidator()

        payment_request = PaymentRequest(
            id=uuid4(),
            user_id=uuid4(),
            amount=Money(Decimal('100'), Currency.USD),
            recipient_address=Address("0x1234567890123456789012345678901234567890", "ethereum"),
            description="Test payment"
        )

        # Should not raise any exception
        validator.validate(payment_request)

    def test_zero_amount_fails_validation(self):
        """Test that zero amount fails validation."""
        validator = PaymentValidator()

        payment_request = PaymentRequest(
            id=uuid4(),
            user_id=uuid4(),
            amount=Money(Decimal('0'), Currency.USD),
            recipient_address=Address("0x1234567890123456789012345678901234567890", "ethereum"),
            description="Test payment"
        )

        with pytest.raises(ValidationError, match="Payment amount cannot be zero"):
            validator.validate(payment_request)

    def test_amount_below_minimum_fails_validation(self):
        """Test that amount below minimum fails validation."""
        validator = PaymentValidator()

        payment_request = PaymentRequest(
            id=uuid4(),
            user_id=uuid4(),
            amount=Money(Decimal('0.001'), Currency.USD),  # Below minimum
            recipient_address=Address("0x1234567890123456789012345678901234567890", "ethereum"),
            description="Test payment"
        )

        with pytest.raises(ValidationError, match="Amount below minimum"):
            validator.validate(payment_request)

    def test_amount_above_maximum_fails_validation(self):
        """Test that amount above maximum fails validation."""
        validator = PaymentValidator()

        payment_request = PaymentRequest(
            id=uuid4(),
            user_id=uuid4(),
            amount=Money(Decimal('20000'), Currency.USD),  # Above maximum
            recipient_address=Address("0x1234567890123456789012345678901234567890", "ethereum"),
            description="Test payment"
        )

        with pytest.raises(ValidationError, match="Amount exceeds maximum"):
            validator.validate(payment_request)

    def test_long_description_fails_validation(self):
        """Test that overly long description fails validation."""
        validator = PaymentValidator()

        payment_request = PaymentRequest(
            id=uuid4(),
            user_id=uuid4(),
            amount=Money(Decimal('100'), Currency.USD),
            recipient_address=Address("0x1234567890123456789012345678901234567890", "ethereum"),
            description="x" * 501  # Too long
        )

        with pytest.raises(ValidationError, match="Description too long"):
            validator.validate(payment_request)


class TestFeeEstimator:
    """Test FeeEstimator service."""

    def test_ethereum_fee_estimation(self):
        """Test Ethereum fee estimation."""
        fee_provider = StaticFeeProvider()
        estimator = FeeEstimator(fee_provider)

        amount = Money(Decimal('100'), Currency.USDT)
        address = Address("0x1234567890123456789012345678901234567890", "ethereum")

        fee = estimator.estimate_fee(amount, address)

        assert fee.currency == Currency.USD
        assert fee.amount > Decimal('0')

    def test_tron_fee_estimation(self):
        """Test Tron fee estimation."""
        fee_provider = StaticFeeProvider()
        estimator = FeeEstimator(fee_provider)

        amount = Money(Decimal('100'), Currency.USDT)
        address = Address("TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH", "tron")

        fee = estimator.estimate_fee(amount, address)

        assert fee.currency == Currency.USD
        assert fee.amount == Decimal('1.0')  # Static fee for Tron

    def test_bitcoin_fee_estimation(self):
        """Test Bitcoin fee estimation."""
        fee_provider = StaticFeeProvider()
        estimator = FeeEstimator(fee_provider)

        amount = Money(Decimal('1'), Currency.BTC)
        address = Address("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "bitcoin")

        fee = estimator.estimate_fee(amount, address)

        assert fee.currency == Currency.BTC
        assert fee.amount > Decimal('0')

    def test_unknown_network_returns_zero_fee(self):
        """Test that unknown network returns zero fee."""
        fee_provider = StaticFeeProvider()
        estimator = FeeEstimator(fee_provider)

        amount = Money(Decimal('100'), Currency.USD)
        # Use a valid Ethereum address but with unknown network type
        address = Address("0x1234567890123456789012345678901234567890", "ethereum")

        # Mock the network to be unknown for this test
        address = type('MockAddress', (), {
            'address': "0x1234567890123456789012345678901234567890",
            'network': 'unknown_network'
        })()

        fee = estimator.estimate_fee(amount, address)

        assert fee.amount == Decimal('0')
        assert fee.currency == Currency.USD


class TestStaticFeeProvider:
    """Test StaticFeeProvider."""

    def test_ethereum_fee_rate(self):
        """Test Ethereum fee rate."""
        provider = StaticFeeProvider()
        rate = provider.get_current_fee_rate('ethereum')
        assert rate == Decimal('20')  # 20 Gwei

    def test_tron_fee_rate(self):
        """Test Tron fee rate."""
        provider = StaticFeeProvider()
        rate = provider.get_current_fee_rate('tron')
        assert rate == Decimal('1')  # 1 TRX

    def test_bitcoin_fee_rate(self):
        """Test Bitcoin fee rate."""
        provider = StaticFeeProvider()
        rate = provider.get_current_fee_rate('bitcoin')
        assert rate == Decimal('10')  # 10 sat/byte

    def test_unknown_network_returns_zero(self):
        """Test unknown network returns zero."""
        provider = StaticFeeProvider()
        rate = provider.get_current_fee_rate('unknown')
        assert rate == Decimal('0')