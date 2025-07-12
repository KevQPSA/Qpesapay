"""
Payment Queries.
Query objects following Sandi Metz principles and CQRS pattern.
Each query represents a single data retrieval operation.
"""

from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.domain import Currency


@dataclass(frozen=True)
class GetTransactionQuery:
    """
    Query to get a single transaction by ID.
    Simple, focused query object.
    """
    transaction_id: UUID
    user_id: Optional[UUID] = None  # For authorization


@dataclass(frozen=True)
class GetUserTransactionsQuery:
    """
    Query to get user's transaction history.
    Supports pagination and filtering.
    """
    user_id: UUID
    limit: int = 50
    offset: int = 0
    status_filter: Optional[str] = None
    currency_filter: Optional[Currency] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


@dataclass(frozen=True)
class GetTransactionStatsQuery:
    """
    Query to get transaction statistics.
    Focused on aggregated data.
    """
    user_id: UUID
    period: str = "month"  # day, week, month, year


@dataclass(frozen=True)
class GetPendingTransactionsQuery:
    """
    Query to get pending transactions.
    Used for monitoring and processing.
    """
    limit: int = 100
    older_than_minutes: Optional[int] = None


# Query Result Objects (Read Models)

@dataclass(frozen=True)
class TransactionView:
    """
    Read model for transaction display.
    Optimized for UI consumption.
    """
    id: str
    amount: str
    currency: str
    recipient_address: str
    status: str
    created_at: datetime
    confirmed_at: Optional[datetime]
    blockchain_hash: Optional[str]
    fees_paid: str
    description: Optional[str]


@dataclass(frozen=True)
class TransactionStatsView:
    """
    Read model for transaction statistics.
    Aggregated data for dashboards.
    """
    total_transactions: int
    total_amount: str
    currency: str
    successful_transactions: int
    failed_transactions: int
    pending_transactions: int
    average_amount: str


# Query Handlers

class GetTransactionHandler:
    """
    Handles GetTransactionQuery.
    Single responsibility: retrieve single transaction.
    """

    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    async def handle(self, query: GetTransactionQuery) -> Optional[TransactionView]:
        """Handle single transaction query."""
        transaction = await self.transaction_repository.find_by_id(str(query.transaction_id))

        if not transaction:
            return None

        # Authorization check
        if query.user_id and transaction.user_id != query.user_id:
            return None

        return self._to_view(transaction)

    def _to_view(self, transaction) -> TransactionView:
        """Convert database model to view model."""
        return TransactionView(
            id=str(transaction.id),
            amount=str(transaction.amount_crypto or transaction.amount_kes or 0),
            currency=self._determine_currency(transaction),
            recipient_address=transaction.to_address or "",
            status=transaction.status.value,
            created_at=transaction.created_at,
            confirmed_at=transaction.confirmed_at,
            blockchain_hash=transaction.blockchain_hash,
            fees_paid=str(transaction.network_fee or 0),
            description=transaction.description
        )

    def _determine_currency(self, transaction) -> str:
        """Determine currency from transaction."""
        if transaction.amount_crypto:
            return "CRYPTO"
        elif transaction.amount_kes:
            return "KES"
        return "UNKNOWN"


class GetUserTransactionsHandler:
    """
    Handles GetUserTransactionsQuery.
    Single responsibility: retrieve user transaction list.
    """

    def __init__(self, transaction_repository):
        self.transaction_repository = transaction_repository

    async def handle(self, query: GetUserTransactionsQuery) -> List[TransactionView]:
        """Handle user transactions query."""
        transactions = await self.transaction_repository.find_by_user(
            user_id=query.user_id,
            limit=query.limit,
            offset=query.offset,
            status_filter=query.status_filter,
            from_date=query.from_date,
            to_date=query.to_date
        )

        return [self._to_view(t) for t in transactions]

    def _to_view(self, transaction) -> TransactionView:
        """Convert database model to view model."""
        return TransactionView(
            id=str(transaction.id),
            amount=str(transaction.amount_crypto or transaction.amount_kes or 0),
            currency=self._determine_currency(transaction),
            recipient_address=transaction.to_address or "",
            status=transaction.status.value,
            created_at=transaction.created_at,
            confirmed_at=transaction.confirmed_at,
            blockchain_hash=transaction.blockchain_hash,
            fees_paid=str(transaction.network_fee or 0),
            description=transaction.description
        )

    def _determine_currency(self, transaction) -> str:
        """Determine currency from transaction."""
        if transaction.amount_crypto:
            return "CRYPTO"
        elif transaction.amount_kes:
            return "KES"
        return "UNKNOWN"