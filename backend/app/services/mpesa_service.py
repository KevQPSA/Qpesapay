import httpx
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime
import base64

from app.config import settings

class MpesaService:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.timeout_url = settings.MPESA_TIMEOUT_URL
        self.result_url = settings.MPESA_RESULT_URL

        # Base URL for Daraja API (use sandbox for development)
        self.base_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" # Example

    async def _get_access_token(self) -> str:
        # In a real application, this token would be cached and refreshed
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        headers = {
            "Authorization": f"Basic {base64.b64encode(f'{self.consumer_key}:{self.consumer_secret}'.encode()).decode()}"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(auth_url, headers=headers)
            response.raise_for_status()
            return response.json()["access_token"]

    async def initiate_stk_push(
        self,
        phone_number: str,
        amount: Decimal,
        account_reference: str,
        transaction_desc: str
    ) -> Dict[str, Any]:
        """Initiates an M-Pesa STK Push transaction."""
        access_token = await self._get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": str(int(amount)), # Amount must be an integer for STK Push
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    async def process_callback(self, callback_data: Dict[str, Any]) -> bool:
        """Processes the M-Pesa STK Push callback data."""
        # In a real application, you would validate the callback, update transaction status,
        # and potentially trigger further actions (e.g., credit user wallet).
        print("M-Pesa Callback Received:", callback_data)
        # Example: Check ResultCode
        result_code = callback_data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
        if result_code == 0:
            print("STK Push successful!")
            return True
        else:
            print(f"STK Push failed with ResultCode: {result_code}")
            return False
