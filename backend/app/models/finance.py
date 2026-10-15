from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from app.database.session import Base

class TransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    DONATION = "DONATION"
    WELFARE_DISBURSEMENT = "WELFARE_DISBURSEMENT"

class TransactionStatus(str, enum.Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    voucher_no = Column(String(50), unique=True, index=True, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False)  # Welfare, Education, Office Expense, Event, Donation
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    
    payment_method = Column(String(50), default="CASH")  # CASH, BANK_TRANSFER, CHEQUE
    reference_number = Column(String(100), nullable=True)
    attachment_path = Column(String(255), nullable=True)
    
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.APPROVED, nullable=False)
    entered_by = Column(String(100), nullable=False)
    approved_by = Column(String(100), nullable=True)
    
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
