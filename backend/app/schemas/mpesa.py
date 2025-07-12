from pydantic import BaseModel, Field
from decimal import Decimal

class MpesaSTKPushRequest(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15, description="Customer's M-Pesa phone number (e.g., 2547XXXXXXXX)")
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="Amount to be paid in KES")
    account_reference: str = Field(..., max_length=12, description="Account reference for the transaction")
    transaction_desc: str = Field(..., max_length=100, description="Description of the transaction")
