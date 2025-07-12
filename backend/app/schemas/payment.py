from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
import uuid

from app.models.transaction import TransactionType, PaymentMethod

class PaymentCreate(BaseModel):
    user_id: uuid.UUID
    transaction_type: TransactionType
    payment_method: PaymentMethod
    amount_crypto: Optional[Decimal] = Field(None)
    amount_kes: Optional[Decimal] = Field(None)
    from_address: Optional[str] = None
    to_address: str
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    blockchain_hash: Optional[str]
    estimated_confirmation_time: int
    gas_fee: Decimal

    class Config:
        orm_mode = True
