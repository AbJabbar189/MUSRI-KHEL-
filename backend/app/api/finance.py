from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from datetime import datetime
from app.database.session import get_db
from app.models.finance import FinancialTransaction, TransactionType, TransactionStatus
from app.schemas.finance import TransactionResponse, TransactionCreate, FinanceSummaryResponse
from app.models.user import User, UserRole
from app.api.auth import require_roles

router = APIRouter(prefix="/finance", tags=["Finance & Accounts"])

@router.get("/summary", response_model=FinanceSummaryResponse)
def get_finance_summary(
    current_user: User = Depends(require_roles(
        UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN, UserRole.FINANCE_OFFICER, UserRole.AUDITOR
    )),
    db: Session = Depends(get_db)
):
    income = db.query(func.sum(FinancialTransaction.amount)).filter(
        FinancialTransaction.transaction_type.in_([TransactionType.INCOME, TransactionType.DONATION]),
        FinancialTransaction.status == TransactionStatus.APPROVED
    ).scalar() or 0.0

    expense = db.query(func.sum(FinancialTransaction.amount)).filter(
        FinancialTransaction.transaction_type.in_([TransactionType.EXPENSE, TransactionType.WELFARE_DISBURSEMENT]),
        FinancialTransaction.status == TransactionStatus.APPROVED
    ).scalar() or 0.0

    total_count = db.query(FinancialTransaction).count()

    return FinanceSummaryResponse(
        total_income=float(income),
        total_expense=float(expense),
        net_balance=float(income - expense),
        total_vouchers=total_count
    )

@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    current_user: User = Depends(require_roles(
        UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN, UserRole.FINANCE_OFFICER, UserRole.AUDITOR
    )),
    db: Session = Depends(get_db)
):
    return db.query(FinancialTransaction).order_by(FinancialTransaction.transaction_date.desc()).all()

@router.post("/vouchers", response_model=TransactionResponse)
def create_voucher(
    payload: TransactionCreate,
    current_user: User = Depends(require_roles(
        UserRole.SUPER_ADMIN, UserRole.FINANCE_OFFICER
    )),
    db: Session = Depends(get_db)
):
    year = datetime.now().year
    count = db.query(FinancialTransaction).count() + 1
    voucher_no = f"VCH-{year}-{count:04d}"

    tx = FinancialTransaction(
        voucher_no=voucher_no,
        transaction_type=payload.transaction_type,
        category=payload.category,
        amount=payload.amount,
        description=payload.description,
        payment_method=payload.payment_method,
        reference_number=payload.reference_number,
        status=TransactionStatus.APPROVED,
        entered_by=current_user.username,
        approved_by=current_user.username
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx
