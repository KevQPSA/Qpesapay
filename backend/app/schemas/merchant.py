"""Merchant schemas for QPesaPay backend."""

from typing import Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.merchant import MerchantStatus


class MerchantBase(BaseModel):
    """Base merchant schema."""
    business_name: str = Field(..., min_length=2, max_length=200, description="Business name")
    business_type: str = Field(..., min_length=2, max_length=100, description="Type of business")
    description: Optional[str] = Field(None, max_length=1000, description="Business description")
    website_url: Optional[str] = Field(None, description="Business website URL")
    support_email: Optional[str] = Field(None, description="Support email address")
    support_phone: Optional[str] = Field(None, description="Support phone number")
    
    class Config:
        use_enum_values = True


class MerchantCreate(MerchantBase):
    """Schema for creating a merchant."""
    pass


class MerchantUpdate(BaseModel):
    """Schema for updating a merchant."""
    business_name: Optional[str] = Field(None, min_length=2, max_length=200)
    business_type: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    website_url: Optional[str] = None
    support_email: Optional[str] = None
    support_phone: Optional[str] = None
    
    class Config:
        use_enum_values = True


class MerchantResponse(MerchantBase):
    """Schema for merchant response."""
    id: UUID
    user_id: UUID
    merchant_id: str
    api_key_id: Optional[str] = None
    status: MerchantStatus
    commission_rate: Decimal
    monthly_volume: Decimal
    total_volume: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class MerchantSettings(BaseModel):
    """Schema for merchant settings."""
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")
    webhook_secret: Optional[str] = Field(None, description="Webhook secret for verification")
    auto_settlement: bool = Field(default=False, description="Enable automatic settlements")
    settlement_schedule: Optional[str] = Field(None, description="Settlement schedule (daily, weekly, monthly)")
    notification_preferences: Dict[str, bool] = Field(default_factory=dict, description="Notification preferences")
    
    @field_validator('webhook_url')
    @classmethod
    def validate_webhook_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Webhook URL must start with http:// or https://')
        return v


class MerchantSettingsUpdate(BaseModel):
    """Schema for updating merchant settings."""
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    auto_settlement: Optional[bool] = None
    settlement_schedule: Optional[str] = None
    notification_preferences: Optional[Dict[str, bool]] = None
    
    @field_validator('webhook_url')
    @classmethod
    def validate_webhook_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Webhook URL must start with http:// or https://')
        return v


class MerchantStats(BaseModel):
    """Schema for merchant statistics."""
    total_transactions: int
    successful_transactions: int
    failed_transactions: int
    pending_transactions: int
    total_volume: Decimal
    monthly_volume: Decimal
    average_transaction_amount: Decimal
    commission_earned: Decimal
    success_rate: float
    
    class Config:
        from_attributes = True


class APIKeyCreate(BaseModel):
    """Schema for creating API key."""
    name: str = Field(..., min_length=1, max_length=100, description="API key name")
    permissions: list[str] = Field(default_factory=list, description="API key permissions")


class APIKeyResponse(BaseModel):
    """Schema for API key response."""
    id: str
    name: str
    permissions: list[str]
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True