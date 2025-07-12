"""
Payment Orchestrator.
Coordinates payment services following Sandi Metz principles.
Single responsibility: orchestrate payment flow.
"""

from typing import Protocol
from app.domain import PaymentRequest, TransactionRecord
from .validator import PaymentValidator, BalanceValidator
from .fee_estimator import FeeEstimator
from .transaction_creator import TransactionCreator


class BlockchainExecutor(Protocol):
    """Protocol for blockchain execution."""

    async def execute_transaction(self, transaction_record: TransactionRecord) -> str:
        """Execute transaction on blockchain. Returns transaction hash."""
        ...


class PaymentOrchestrator:
    """
    Orchestrates the payment process.
    Single responsibility: coordinate payment services.
    Follows Sandi's composition over inheritance principle.
    """

    def __init__(
        self,
        payment_validator: PaymentValidator,
        balance_validator: BalanceValidator,
        fee_estimator: FeeEstimator,
        transaction_creator: TransactionCreator,
        blockchain_executor: BlockchainExecutor
    ):
        self.payment_validator = payment_validator
        self.balance_validator = balance_validator
        self.fee_estimator = fee_estimator
        self.transaction_creator = transaction_creator
        self.blockchain_executor = blockchain_executor

    async def process_payment(self, payment_request: PaymentRequest) -> TransactionRecord:
        """
        Process payment request through the complete flow.
        Each step is handled by a focused service.
        """
        # Step 1: Validate payment request
        self.payment_validator.validate(payment_request)

        # Step 2: Validate sufficient balance
        self.balance_validator.validate_sufficient_balance(
            str(payment_request.user_id),
            payment_request.amount
        )

        # Step 3: Estimate fees
        estimated_fee = self.fee_estimator.estimate_fee(
            payment_request.amount,
            payment_request.recipient_address
        )

        # Step 4: Create pending transaction
        transaction_record = await self.transaction_creator.create_pending_transaction(
            payment_request,
            estimated_fee
        )

        # Step 5: Execute on blockchain
        blockchain_hash = await self.blockchain_executor.execute_transaction(transaction_record)

        # Step 6: Update transaction with blockchain hash
        return transaction_record.mark_confirmed()


class PaymentResult:
    """
    Value object for payment results.
    Encapsulates payment outcome information.
    """

    def __init__(
        self,
        transaction_id: str,
        status: str,
        blockchain_hash: str = None,
        estimated_confirmation_time: int = 300,
        fees_paid: str = "0"
    ):
        self.transaction_id = transaction_id
        self.status = status
        self.blockchain_hash = blockchain_hash
        self.estimated_confirmation_time = estimated_confirmation_time
        self.fees_paid = fees_paid

    def to_dict(self) -> dict:
        """Convert to dictionary for API response."""
        return {
            "transaction_id": self.transaction_id,
            "status": self.status,
            "blockchain_hash": self.blockchain_hash,
            "estimated_confirmation_time": self.estimated_confirmation_time,
            "gas_fee": self.fees_paid
        }