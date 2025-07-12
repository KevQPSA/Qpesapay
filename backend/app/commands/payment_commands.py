"""
Payment Commands.
Command objects following Sandi Metz principles and CQRS pattern.
Each command represents a single business operation.
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from decimal import Decimal

from app.domain import Money, Address, Currency


@dataclass(frozen=True)
class CreatePaymentCommand:
    """
    Command to create a new payment.
    Immutable command object with all required data.
    """
    user_id: UUID
    amount: Decimal
    currency: Currency
    recipient_address: str
    recipient_network: str
    description: Optional[str] = None

    def to_domain_objects(self):
        """Convert command to domain objects."""
        money = Money(self.amount, self.currency)
        address = Address(self.recipient_address, self.recipient_network)
        return money, address


@dataclass(frozen=True)
class ConfirmPaymentCommand:
    """
    Command to confirm a payment transaction.
    Used when blockchain transaction is confirmed.
    """
    transaction_id: UUID
    blockchain_hash: str
    confirmation_count: int = 1


@dataclass(frozen=True)
class CancelPaymentCommand:
    """
    Command to cancel a pending payment.
    Can only cancel payments that haven't been broadcast.
    """
    transaction_id: UUID
    user_id: UUID
    reason: str


@dataclass(frozen=True)
class RefundPaymentCommand:
    """
    Command to process a payment refund.
    Creates a new transaction for the refund.
    """
    original_transaction_id: UUID
    refund_amount: Decimal
    refund_reason: str
    initiated_by: UUID


# Command Handlers

class CreatePaymentHandler:
    """
    Handles CreatePaymentCommand.
    Single responsibility: process payment creation.
    """

    def __init__(self, payment_orchestrator):
        self.payment_orchestrator = payment_orchestrator

    async def handle(self, command: CreatePaymentCommand):
        """Handle payment creation command."""
        money, address = command.to_domain_objects()

        # Create domain payment request
        from app.domain import PaymentRequest
        payment_request = PaymentRequest(
            id=None,  # Will be generated
            user_id=command.user_id,
            amount=money,
            recipient_address=address,
            description=command.description
        )

        # Process through orchestrator
        return await self.payment_orchestrator.process_payment(payment_request)


class ConfirmPaymentHandler:
    """
    Handles ConfirmPaymentCommand.
    Single responsibility: confirm payment transactions.
    """

    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    async def handle(self, command: ConfirmPaymentCommand):
        """Handle payment confirmation command."""
        from app.models.transaction import TransactionStatus

        return await self.transaction_repository.update_status(
            str(command.transaction_id),
            TransactionStatus.CONFIRMED,
            command.blockchain_hash
        )


class CancelPaymentHandler:
    """
    Handles CancelPaymentCommand.
    Single responsibility: cancel pending payments.
    """

    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    async def handle(self, command: CancelPaymentCommand):
        """Handle payment cancellation command."""
        from app.models.transaction import TransactionStatus

        # Verify user owns the transaction
        transaction = await self.transaction_repository.find_by_id(str(command.transaction_id))
        if transaction.user_id != command.user_id:
            raise ValueError("User cannot cancel this transaction")

        # Only allow cancellation of pending transactions
        if transaction.status != TransactionStatus.PENDING:
            raise ValueError("Can only cancel pending transactions")

        return await self.transaction_repository.update_status(
            str(command.transaction_id),
            TransactionStatus.CANCELLED
        )