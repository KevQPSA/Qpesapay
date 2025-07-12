"""Settlement schemas for QPesaPay backend."""

from typing import Optional, Dict, Any, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, validator

from app.models.settlement import SettlementStatus, SettlementType


class SettlementBase(BaseModel):
    """Base settlement schema."""
    settlement_type: SettlementType = Field(..., description="Type of settlement")
    currency: str = Field(..., min_length=3, max_length=10, description="Settlement currency")
    description: Optional[str] = Field(None, max_length=500, description="Settlement description")
    
    class Config:
        use_enum_values = True


class SettlementCreate(SettlementBase):
    """Schema for creating a settlement."""
    merchant_id: UUID = Field(..., description="Merchant ID for the settlement")
    amount: Decimal = Field(..., gt=0, description="Settlement amount")
    fee: Decimal = Field(default=Decimal('0'), ge=0, description="Settlement fee")
    
    @validator('amount', 'fee')
    def validate_decimal_places(cls, v):
        if v.as_tuple().exponent < -8:
            raise ValueError('Maximum 8 decimal places allowed')
        return v


class SettlementUpdate(BaseModel):
    """Schema for updating a settlement."""
    description: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        use_enum_values = True


class SettlementResponse(SettlementBase):
    """Schema for settlement response."""
    id: UUID
    merchant_id: UUID
    settlement_id: str
    amount: Decimal
    fee: Decimal
    net_amount: Decimal
    status: SettlementStatus
    bank_reference: Optional[str] = None
    processed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class SettlementBatch(BaseModel):
    """Schema for settlement batch."""
    merchant_ids: List[UUID] = Field(..., description="List of merchant IDs to settle")
    settlement_type: SettlementType = Field(default=SettlementType.AUTOMATIC, description="Batch settlement type")
    description: Optional[str] = Field(None, max_length=500, description="Batch description")
    
    class Config:
        use_enum_values = True


class SettlementBatchResponse(BaseModel):
    """Schema for settlement batch response."""
    batch_id: str
    total_settlements: int
    total_amount: Decimal
    total_fee: Decimal
    total_net_amount: Decimal
    settlements: List[SettlementResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SettlementStats(BaseModel):
    """Schema for settlement statistics."""
    total_settlements: int
    successful_settlements: int
    failed_settlements: int
    pending_settlements: int
    total_amount: Decimal
    total_fee: Decimal
    total_net_amount: Decimal
    average_settlement_amount: Decimal
    success_rate: float
    
    class Config:
        from_attributes = True


class SettlementSchedule(BaseModel):
    """Schema for settlement schedule."""
    merchant_id: UUID
    schedule_type: str = Field(..., description="Schedule type (daily, weekly, monthly)")
    schedule_time: str = Field(..., description="Time for settlement (HH:MM format)")
    minimum_amount: Decimal = Field(default=Decimal('0'), ge=0, description="Minimum amount for settlement")
    is_active: bool = Field(default=True, description="Whether schedule is active")
    
    @validator('schedule_type')
    def validate_schedule_type(cls, v):
        allowed_types = ['daily', 'weekly', 'monthly']
        if v not in allowed_types:
            raise ValueError(f'Schedule type must be one of: {", ".join(allowed_types)}')
        return v
    
    @validator('schedule_time')
    def validate_schedule_time(cls, v):
        try:
            hour, minute = map(int, v.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError('Invalid time format')
        except (ValueError, AttributeError):
            raise ValueError('Time must be in HH:MM format (24-hour)')
        return v


class SettlementScheduleUpdate(BaseModel):
    """Schema for updating settlement schedule."""
    schedule_type: Optional[str] = None
    schedule_time: Optional[str] = None
    minimum_amount: Optional[Decimal] = None
    is_active: Optional[bool] = None
    
    @validator('schedule_type')
    def validate_schedule_type(cls, v):
        if v is not None:
            allowed_types = ['daily', 'weekly', 'monthly']
            if v not in allowed_types:
                raise ValueError(f'Schedule type must be one of: {", ".join(allowed_types)}')
        return v
    
    @validator('schedule_time')
    def validate_schedule_time(cls, v):
        if v is not None:
            try:
                hour, minute = map(int, v.split(':'))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError('Invalid time format')
            except (ValueError, AttributeError):
                raise ValueError('Time must be in HH:MM format (24-hour)')
        return v


class BankAccount(BaseModel):
    """Schema for bank account information."""
    account_name: str = Field(..., min_length=2, max_length=100, description="Account holder name")
    account_number: str = Field(..., min_length=5, max_length=50, description="Bank account number")
    bank_name: str = Field(..., min_length=2, max_length=100, description="Bank name")
    bank_code: str = Field(..., min_length=2, max_length=20, description="Bank code")
    branch_code: Optional[str] = Field(None, max_length=20, description="Branch code")
    swift_code: Optional[str] = Field(None, max_length=20, description="SWIFT code for international transfers")
    is_primary: bool = Field(default=False, description="Whether this is the primary account")


class BankAccountUpdate(BaseModel):
    """Schema for updating bank account information."""
    account_name: Optional[str] = Field(None, min_length=2, max_length=100)
    account_number: Optional[str] = Field(None, min_length=5, max_length=50)
    bank_name: Optional[str] = Field(None, min_length=2, max_length=100)
    bank_code: Optional[str] = Field(None, min_length=2, max_length=20)
    branch_code: Optional[str] = Field(None, max_length=20)
    swift_code: Optional[str] = Field(None, max_length=20)
    is_primary: Optional[bool] = None