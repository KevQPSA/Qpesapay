"""
Fee Estimator Service.
Single responsibility: Calculate transaction fees.
Following Sandi Metz principles: small, focused, testable.
"""

from decimal import Decimal
from typing import Protocol
from app.domain import Money, Currency, Address


class NetworkFeeProvider(Protocol):
    """Protocol for network fee providers."""

    def get_current_fee_rate(self, network: str) -> Decimal:
        """Get current fee rate for network."""
        ...


class FeeEstimator:
    """
    Estimates transaction fees for different networks.
    Single responsibility: fee calculation only.
    """

    def __init__(self, fee_provider: NetworkFeeProvider):
        self.fee_provider = fee_provider

    def estimate_fee(self, amount: Money, recipient_address: Address) -> Money:
        """
        Estimate transaction fee.
        Returns fee in the same currency as the amount.
        """
        network = recipient_address.network.lower()

        if network == 'ethereum':
            return self._estimate_ethereum_fee(amount)
        elif network == 'tron':
            return self._estimate_tron_fee(amount)
        elif network == 'bitcoin':
            return self._estimate_bitcoin_fee(amount)
        else:
            return Money(Decimal('0'), amount.currency)

    def _estimate_ethereum_fee(self, amount: Money) -> Money:
        """Estimate Ethereum network fee."""
        base_fee = self.fee_provider.get_current_fee_rate('ethereum')
        gas_limit = Decimal('21000')  # Standard transfer

        # Convert to USD if needed
        if amount.currency == Currency.USDT:
            fee_amount = (base_fee * gas_limit) / Decimal('1000000000')  # Convert from Gwei
            return Money(fee_amount, Currency.USD)

        return Money(Decimal('0.001'), Currency.USD)  # Fallback

    def _estimate_tron_fee(self, amount: Money) -> Money:
        """Estimate Tron network fee."""
        # Tron fees are typically very low
        return Money(Decimal('1.0'), Currency.USD)  # ~1 TRX

    def _estimate_bitcoin_fee(self, amount: Money) -> Money:
        """Estimate Bitcoin network fee."""
        fee_rate = self.fee_provider.get_current_fee_rate('bitcoin')
        estimated_size = Decimal('250')  # Average transaction size in bytes

        fee_btc = (fee_rate * estimated_size) / Decimal('100000000')  # Convert from satoshis
        return Money(fee_btc, Currency.BTC)


class StaticFeeProvider:
    """
    Static fee provider for testing/development.
    Returns fixed fee rates.
    """

    def get_current_fee_rate(self, network: str) -> Decimal:
        """Get static fee rate for network."""
        rates = {
            'ethereum': Decimal('20'),  # 20 Gwei
            'tron': Decimal('1'),       # 1 TRX
            'bitcoin': Decimal('10'),   # 10 sat/byte
        }
        return rates.get(network, Decimal('0'))


class DynamicFeeProvider:
    """
    Dynamic fee provider that fetches real-time rates.
    Single responsibility: fetch current network fees.
    """

    def __init__(self, api_client):
        self.api_client = api_client

    def get_current_fee_rate(self, network: str) -> Decimal:
        """Get current fee rate from external API."""
        try:
            return self.api_client.get_fee_rate(network)
        except Exception:
            # Fallback to static rates if API fails
            fallback = StaticFeeProvider()
            return fallback.get_current_fee_rate(network)