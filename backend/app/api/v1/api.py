from fastapi import APIRouter
from app.api.v1.endpoints import auth, payments, webhooks
from app.api.v1 import webagent

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
api_router.include_router(webagent.router, tags=["webagent"])
