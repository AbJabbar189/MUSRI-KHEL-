from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.finance import TransactionType, TransactionStatus

class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    category: str
    amount: float
    description: str
    payment_method: str = "CASH"
    reference_number: Optional[str] = None
    entered_by: str

class TransactionResponse(TransactionCreate):
    id: int
    voucher_no: str
    status: TransactionStatus
    approved_by: Optional[str] = None
    transaction_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FinanceSummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float
    total_vouchers: int
