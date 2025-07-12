"""
Transaction Creator Service.
Single responsibility: Create transaction records in database.
Following Sandi Metz principles: small, focused, testable.
"""

from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain import PaymentRequest, TransactionRecord, Money
from app.models.transaction import Transaction, TransactionStatus, TransactionType


class TransactionRepository(Protocol):
    """Protocol for transaction repository."""

    async def save(self, transaction: Transaction) -> Transaction:
        """Save transaction to database."""
        ...

    async def find_by_id(self, transaction_id: str) -> Transaction:
        """Find transaction by ID."""
        ...


class TransactionCreator:
    """
    Creates transaction records in the database.
    Single responsibility: transaction persistence only.
    """

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def create_pending_transaction(
        self,
        payment_request: PaymentRequest,
        estimated_fee: Money
    ) -> TransactionRecord:
        """
        Create a pending transaction record.
        Returns domain TransactionRecord.
        """
        # Create database model
        db_transaction = Transaction(
            user_id=payment_request.user_id,
            transaction_type=self._map_transaction_type(payment_request),
            status=TransactionStatus.PENDING,
            amount_crypto=payment_request.amount.amount,
            to_address=payment_request.recipient_address.address,
            network_fee=estimated_fee.amount,
            description=payment_request.description
        )

        # Save to database
        saved_transaction = await self.repository.save(db_transaction)

        # Return domain object
        return TransactionRecord(
            id=saved_transaction.id,
            payment_request_id=payment_request.id,
            blockchain_hash=None,
            status=saved_transaction.status.value,
            fees_paid=Money(saved_transaction.network_fee, payment_request.amount.currency)
        )

    def _map_transaction_type(self, payment_request: PaymentRequest) -> TransactionType:
        """Map domain payment request to database transaction type."""
        # Simple mapping - could be more sophisticated
        return TransactionType.PAYMENT


class DatabaseTransactionRepository:
    """
    Database implementation of TransactionRepository.
    Single responsibility: database operations for transactions.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(self, transaction: Transaction) -> Transaction:
        """Save transaction to database."""
        self.db_session.add(transaction)
        await self.db_session.commit()
        await self.db_session.refresh(transaction)
        return transaction

    async def find_by_id(self, transaction_id: str) -> Transaction:
        """Find transaction by ID."""
        return await self.db_session.get(Transaction, transaction_id)

    async def update_status(
        self,
        transaction_id: str,
        new_status: TransactionStatus,
        blockchain_hash: str = None
    ) -> Transaction:
        """Update transaction status."""
        transaction = await self.find_by_id(transaction_id)
        if transaction:
            transaction.status = new_status
            if blockchain_hash:
                transaction.blockchain_hash = blockchain_hash
            await self.db_session.commit()
            await self.db_session.refresh(transaction)
        return transaction