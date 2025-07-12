from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.mpesa_service import MpesaService

router = APIRouter()
mpesa_service = MpesaService()

@router.post("/mpesa/callback")
async def mpesa_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        callback_data = await request.json()
        # In a real application, you would validate the callback signature
        # For now, we'll just process the data
        success = await mpesa_service.process_callback(callback_data)
        if success:
            return {"ResultCode": 0, "ResultDesc": "Callback received successfully"}
        else:
            raise HTTPException(status_code=400, detail="M-Pesa callback processing failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@router.post("/mpesa/timeout")
async def mpesa_timeout(request: Request):
    timeout_data = await request.json()
    print("M-Pesa Timeout Received:", timeout_data)
    # Handle timeout logic here (e.g., update transaction status to expired/failed)
    return {"ResultCode": 0, "ResultDesc": "Timeout received successfully"}

@router.post("/mpesa/result")
async def mpesa_result(request: Request):
    result_data = await request.json()
    print("M-Pesa Result Received:", result_data)
    # Handle result logic here (e.g., final transaction status update)
    return {"ResultCode": 0, "ResultDesc": "Result received successfully"}
