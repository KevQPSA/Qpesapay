"""
Dependency Injection Container.
Following Sandi Metz principles: explicit dependencies, easy testing.
Manages object creation and wiring.
"""

from typing import Dict, Any, Callable
from sqlalchemy.ext.asyncio import AsyncSession

# Domain and Services
from app.services.payment import (
    PaymentValidator, BalanceValidator, FeeEstimator,
    TransactionCreator, PaymentOrchestrator,
    StaticFeeProvider, DatabaseTransactionRepository
)

# Commands and Queries
from app.commands.payment_commands import (
    CreatePaymentHandler, ConfirmPaymentHandler, CancelPaymentHandler
)
from app.queries.payment_queries import (
    GetTransactionHandler, GetUserTransactionsHandler
)


class Container:
    """
    Simple dependency injection container.
    Single responsibility: manage object creation and dependencies.
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._setup_services()

    def _setup_services(self):
        """Setup service factories."""
        # Core Services
        self._factories['fee_provider'] = lambda: StaticFeeProvider()
        self._factories['payment_validator'] = lambda: PaymentValidator()
        self._factories['fee_estimator'] = lambda: FeeEstimator(self.get('fee_provider'))

        # Repository factories (require database session)
        self._factories['transaction_repository'] = self._create_transaction_repository

        # Service factories
        self._factories['balance_validator'] = self._create_balance_validator
        self._factories['transaction_creator'] = self._create_transaction_creator
        self._factories['payment_orchestrator'] = self._create_payment_orchestrator

        # Command handlers
        self._factories['create_payment_handler'] = self._create_payment_handler
        self._factories['confirm_payment_handler'] = self._create_confirm_payment_handler
        self._factories['cancel_payment_handler'] = self._create_cancel_payment_handler

        # Query handlers
        self._factories['get_transaction_handler'] = self._create_get_transaction_handler
        self._factories['get_user_transactions_handler'] = self._create_get_user_transactions_handler

    def get(self, service_name: str) -> Any:
        """Get service instance."""
        if service_name not in self._services:
            if service_name not in self._factories:
                raise ValueError(f"Unknown service: {service_name}")
            self._services[service_name] = self._factories[service_name]()
        return self._services[service_name]

    def get_with_db(self, service_name: str, db_session: AsyncSession) -> Any:
        """Get service instance that requires database session."""
        # Don't cache database-dependent services
        if service_name == 'transaction_repository':
            return DatabaseTransactionRepository(db_session)
        elif service_name == 'transaction_creator':
            return TransactionCreator(self.get_with_db('transaction_repository', db_session))
        elif service_name == 'create_payment_handler':
            return CreatePaymentHandler(self._create_payment_orchestrator_with_db(db_session))
        elif service_name == 'confirm_payment_handler':
            return ConfirmPaymentHandler(self.get_with_db('transaction_repository', db_session))
        elif service_name == 'cancel_payment_handler':
            return CancelPaymentHandler(self.get_with_db('transaction_repository', db_session))
        elif service_name == 'get_transaction_handler':
            return GetTransactionHandler(self.get_with_db('transaction_repository', db_session))
        elif service_name == 'get_user_transactions_handler':
            return GetUserTransactionsHandler(self.get_with_db('transaction_repository', db_session))
        else:
            return self.get(service_name)

    # Factory methods

    def _create_transaction_repository(self):
        """Factory for transaction repository - requires DB session."""
        raise ValueError("Transaction repository requires database session - use get_with_db()")

    def _create_balance_validator(self):
        """Factory for balance validator."""
        # Mock balance checker for now
        class MockBalanceChecker:
            def get_balance(self, user_id: str, currency):
                from app.domain import Money, Currency
                from decimal import Decimal
                return Money(Decimal('1000'), Currency.USD)

        return BalanceValidator(MockBalanceChecker())

    def _create_transaction_creator(self):
        """Factory for transaction creator - requires DB session."""
        raise ValueError("Transaction creator requires database session - use get_with_db()")

    def _create_payment_orchestrator(self):
        """Factory for payment orchestrator - requires DB session."""
        raise ValueError("Payment orchestrator requires database session - use get_with_db()")

    def _create_payment_orchestrator_with_db(self, db_session: AsyncSession):
        """Create payment orchestrator with database session."""
        # Mock blockchain executor for now
        class MockBlockchainExecutor:
            async def execute_transaction(self, transaction_record):
                return "0x1234567890abcdef"

        return PaymentOrchestrator(
            payment_validator=self.get('payment_validator'),
            balance_validator=self.get('balance_validator'),
            fee_estimator=self.get('fee_estimator'),
            transaction_creator=self.get_with_db('transaction_creator', db_session),
            blockchain_executor=MockBlockchainExecutor()
        )

    def _create_payment_handler(self):
        """Factory for create payment handler - requires DB session."""
        raise ValueError("Create payment handler requires database session - use get_with_db()")

    def _create_confirm_payment_handler(self):
        """Factory for confirm payment handler - requires DB session."""
        raise ValueError("Confirm payment handler requires database session - use get_with_db()")

    def _create_cancel_payment_handler(self):
        """Factory for cancel payment handler - requires DB session."""
        raise ValueError("Cancel payment handler requires database session - use get_with_db()")

    def _create_get_transaction_handler(self):
        """Factory for get transaction handler - requires DB session."""
        raise ValueError("Get transaction handler requires database session - use get_with_db()")

    def _create_get_user_transactions_handler(self):
        """Factory for get user transactions handler - requires DB session."""
        raise ValueError("Get user transactions handler requires database session - use get_with_db()")


# Global container instance
container = Container()