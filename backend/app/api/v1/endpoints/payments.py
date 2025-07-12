from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService
from app.services.blockchain_service import BlockchainService
from app.services.mpesa_service import MpesaService
from app.schemas.mpesa import MpesaSTKPushRequest

router = APIRouter()

# Initialize services (can be done via dependency injection in a larger app)
blockchain_service = BlockchainService()
payment_service = PaymentService(blockchain_service)
mpesa_service = MpesaService()

@router.post("/create", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_new_payment(payment_in: PaymentCreate, db: AsyncSession = Depends(get_db)):
    try:
        payment_response = await payment_service.create_payment(db, payment_in)
        return payment_response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/{transaction_id}", response_model=PaymentResponse)
async def get_payment_status(transaction_id: str, db: AsyncSession = Depends(get_db)):
    transaction = await payment_service.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    # For simplicity, converting model to schema directly. In a real app, you might have a dedicated mapper.
    return PaymentResponse(
        transaction_id=str(transaction.id),
        status=transaction.status.value,
        blockchain_hash=transaction.blockchain_hash,
        estimated_confirmation_time=300, # Placeholder
        gas_fee=transaction.network_fee if transaction.network_fee else 0
    )

@router.post("/mpesa/stkpush", status_code=status.HTTP_200_OK)
async def initiate_mpesa_stk_push(stk_push_request: MpesaSTKPushRequest):
    try:
        response = await mpesa_service.initiate_stk_push(
            phone_number=stk_push_request.phone_number,
            amount=stk_push_request.amount,
            account_reference=stk_push_request.account_reference,
            transaction_desc=stk_push_request.transaction_desc
        )
        return {"message": "STK Push initiated successfully", "data": response}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
