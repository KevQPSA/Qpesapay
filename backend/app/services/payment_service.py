from decimal import Decimal
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction, TransactionStatus, PaymentMethod
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.blockchain_service import BlockchainService

class PaymentService:
    def __init__(self, blockchain_service: BlockchainService):
        self.blockchain_service = blockchain_service

    async def create_payment(self, db: AsyncSession, payment_in: PaymentCreate) -> PaymentResponse:
        # 1. Validate payment request (e.g., sufficient balance, valid addresses)
        # This would typically involve checking user's wallet balance, recipient address validity, etc.
        # For now, we'll assume validation passes.

        # 2. Estimate gas fees for blockchain transactions
        gas_fee = Decimal('0') # Placeholder
        if payment_in.payment_method in [PaymentMethod.USDT_ETHEREUM, PaymentMethod.USDT_TRON, PaymentMethod.BITCOIN]:
            # In a real scenario, this would call blockchain_service to estimate fees
            gas_fee = await self.blockchain_service.estimate_gas_fee(payment_in.payment_method)

        # 3. Create a pending transaction record in the database
        new_transaction = Transaction(
            user_id=payment_in.user_id,
            transaction_type=payment_in.transaction_type,
            status=TransactionStatus.PENDING,
            payment_method=payment_in.payment_method,
            amount_crypto=payment_in.amount_crypto,
            amount_kes=payment_in.amount_kes,
            to_address=payment_in.to_address,
            network_fee=gas_fee,
            # Add other fields as necessary from payment_in
        )
        db.add(new_transaction)
        await db.commit()
        await db.refresh(new_transaction)

        # 4. Execute the blockchain transaction (if applicable)
        blockchain_hash = None
        if payment_in.payment_method in [PaymentMethod.USDT_ETHEREUM, PaymentMethod.USDT_TRON, PaymentMethod.BITCOIN]:
            blockchain_hash = await self.blockchain_service.send_transaction(
                payment_in.from_address, # Assuming from_address is provided for sending
                payment_in.to_address,
                payment_in.amount_crypto,
                payment_in.payment_method
            )
            new_transaction.blockchain_hash = blockchain_hash
            new_transaction.status = TransactionStatus.PROCESSING # Update status after sending
            await db.commit()
            await db.refresh(new_transaction)

        # 5. Return a response
        return PaymentResponse(
            transaction_id=str(new_transaction.id),
            status=new_transaction.status.value,
            blockchain_hash=blockchain_hash,
            estimated_confirmation_time=300, # Example: 5 minutes
            gas_fee=gas_fee
        )

    async def get_transaction_by_id(self, db: AsyncSession, transaction_id: str) -> Optional[Transaction]:
        return await db.get(Transaction, transaction_id)

    async def update_transaction_status(self, db: AsyncSession, transaction_id: str, new_status: TransactionStatus, blockchain_hash: Optional[str] = None) -> Transaction:
        transaction = await self.get_transaction_by_id(db, transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        transaction.status = new_status
        if blockchain_hash:
            transaction.blockchain_hash = blockchain_hash
        await db.commit()
        await db.refresh(transaction)
        return transaction
