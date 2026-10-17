from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database.session import get_db
from app.models.member import MembershipApplication, Member, MembershipStatus
from app.models.user import User, UserRole
from app.schemas.member import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationReview,
    MemberResponse
)
from app.api.auth import get_current_user, require_roles
from app.services.member_service import generate_application_number, approve_application

router = APIRouter(prefix="/members", tags=["Members & Applications"])

@router.post("/apply", response_model=ApplicationResponse)
def submit_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    # Duplicate check: check if same mobile or CNIC already has pending or approved application
    existing_query = db.query(MembershipApplication).filter(
        MembershipApplication.status.in_([MembershipStatus.PENDING, MembershipStatus.APPROVED])
    )
    if payload.cnic:
        existing = existing_query.filter(
            (MembershipApplication.mobile_number == payload.mobile_number) |
            (MembershipApplication.cnic == payload.cnic)
        ).first()
    else:
        existing = existing_query.filter(MembershipApplication.mobile_number == payload.mobile_number).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="اس موبائل نمبر یا شناختی کارڈ پر پہلے سے ایک فعال درخواست موجود ہے۔"
        )

    app_number = generate_application_number(db)
    application = MembershipApplication(
        application_number=app_number,
        full_name_ur=payload.full_name_ur,
        full_name_en=payload.full_name_en,
        father_name_ur=payload.father_name_ur,
        father_name_en=payload.father_name_en,
        cnic=payload.cnic,
        mobile_number=payload.mobile_number,
        emergency_contact=payload.emergency_contact,
        email=payload.email,
        current_city=payload.current_city,
        current_area=payload.current_area,
        ancestral_region=payload.ancestral_region,
        ancestral_village=payload.ancestral_village,
        clan_sub_tribe=payload.clan_sub_tribe,
        occupation=payload.occupation,
        education_level=payload.education_level,
        professional_category=payload.professional_category,
        declaration_accepted=payload.declaration_accepted,
        # Entry Fee PKR 300 & Receipt Details
        entry_fee=payload.entry_fee or 300.0,
        fee_status="PAID" if payload.transaction_reference else "PENDING",
        payment_method=payload.payment_method or "EasyPaisa",
        transaction_reference=payload.transaction_reference,
        receipt_slip_path=payload.receipt_slip_path or "images/sample_receipt.svg",
        status=MembershipStatus.PENDING
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/status/{identifier}")
def check_status(identifier: str, db: Session = Depends(get_db)):
    clean_id = identifier.strip().replace("-", "").replace(" ", "")
    raw_query = identifier.strip()

    # 1. Search in approved Members first
    member = db.query(Member).filter(
        (Member.membership_id.ilike(f"%{raw_query}%")) |
        (Member.mobile_number == raw_query) |
        (Member.cnic == raw_query) |
        (func.replace(Member.cnic, "-", "") == clean_id) |
        (Member.full_name_ur.ilike(f"%{raw_query}%")) |
        (Member.full_name_en.ilike(f"%{raw_query}%"))
    ).first()
    
    if member:
        card = member.cards[0] if member.cards else None
        return {
            "found": True,
            "type": "MEMBER",
            "membership_id": member.membership_id,
            "application_number": member.application.application_number if member.application else "-",
            "name": member.full_name_ur,
            "name_en": member.full_name_en,
            "father_name_ur": member.father_name_ur or "-",
            "father_name_en": member.father_name_en or "-",
            "cnic": member.cnic or "مصدقہ رکن",
            "mobile": member.mobile_number,
            "status": member.status.value,
            "current_city": member.current_city,
            "current_area": member.current_area,
            "ancestral_region": member.ancestral_region,
            "ancestral_village": member.ancestral_village or "-",
            "occupation": member.occupation or "-",
            "professional_category": member.professional_category or "معزز رکن",
            # Entry Fee & Financials
            "entry_fee": member.entry_fee or 300.0,
            "fee_status": member.fee_status or "PAID",
            "payment_method": member.payment_method or "EasyPaisa",
            "transaction_reference": member.transaction_reference or "TRX-VERIFIED-300",
            "receipt_slip_path": member.receipt_slip_path or "images/sample_receipt.svg",
            "entry_timestamp": member.joined_date.strftime("%d-%b-%Y %I:%M %p") if member.joined_date else "15-Oct-2026 05:22 PM",
            "card_issued": card is not None,
            "card_number": card.card_number if card else None,
            "card_pdf": card.pdf_path if card else None,
            "verification_token": card.verification_token if card else None
        }
    
    # 2. Search in Membership Applications
    app_record = db.query(MembershipApplication).filter(
        (MembershipApplication.application_number.ilike(f"%{raw_query}%")) |
        (MembershipApplication.mobile_number == raw_query) |
        (MembershipApplication.cnic == raw_query) |
        (func.replace(MembershipApplication.cnic, "-", "") == clean_id) |
        (MembershipApplication.full_name_ur.ilike(f"%{raw_query}%")) |
        (MembershipApplication.full_name_en.ilike(f"%{raw_query}%"))
    ).first()

    if not app_record:
        raise HTTPException(
            status_code=404, 
            detail="اس نام، شناختی کارڈ، ممبرشپ نمبر یا موبائل پر کوئی ریکارڈ یا درخواست نہیں ملی۔"
        )
    
    card_info = None
    if app_record.member and app_record.member.cards:
        c = app_record.member.cards[0]
        card_info = {
            "card_number": c.card_number,
            "pdf_path": c.pdf_path,
            "verification_token": c.verification_token
        }

    return {
        "found": True,
        "type": "APPLICATION",
        "application_number": app_record.application_number,
        "membership_id": app_record.member.membership_id if app_record.member else "زیرِ جائزہ",
        "name": app_record.full_name_ur,
        "name_en": app_record.full_name_en,
        "father_name_ur": app_record.father_name_ur or "-",
        "father_name_en": app_record.father_name_en or "-",
        "cnic": app_record.cnic or "درخواست میں درج",
        "mobile": app_record.mobile_number,
        "status": app_record.status.value,
        "current_city": app_record.current_city,
        "current_area": app_record.current_area,
        "ancestral_region": app_record.ancestral_region,
        "ancestral_village": app_record.ancestral_village or "-",
        "occupation": app_record.occupation or "-",
        "professional_category": app_record.professional_category or "درخواست گزار",
        # Entry Fee & Financials
        "entry_fee": app_record.entry_fee or 300.0,
        "fee_status": app_record.fee_status or "PAID",
        "payment_method": app_record.payment_method or "EasyPaisa",
        "transaction_reference": app_record.transaction_reference or "TRX-VERIFIED-300",
        "receipt_slip_path": app_record.receipt_slip_path or "images/sample_receipt.svg",
        "entry_timestamp": app_record.created_at.strftime("%d-%b-%Y %I:%M %p") if app_record.created_at else "15-Oct-2026",
        "review_notes": app_record.review_notes,
        "card": card_info
    }

@router.get("/applications", response_model=List[ApplicationResponse])
def list_applications(
    status_filter: Optional[MembershipStatus] = None,
    region: Optional[str] = None,
    current_user: User = Depends(require_roles(
        UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN, UserRole.GENERAL_SECRETARY, UserRole.MEMBERSHIP_OFFICER, UserRole.REGIONAL_ADMIN
    )),
    db: Session = Depends(get_db)
):
    query = db.query(MembershipApplication)
    
    # Regional isolation: If user is regional admin, filter only their region
    if current_user.role == UserRole.REGIONAL_ADMIN and current_user.assigned_region:
        query = query.filter(MembershipApplication.ancestral_region == current_user.assigned_region)
    elif region:
        query = query.filter(MembershipApplication.ancestral_region == region)
        
    if status_filter:
        query = query.filter(MembershipApplication.status == status_filter)
        
    return query.order_by(MembershipApplication.created_at.desc()).all()

@router.post("/applications/{app_id}/review")
def review_application(
    app_id: int,
    review: ApplicationReview,
    current_user: User = Depends(require_roles(
        UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN, UserRole.GENERAL_SECRETARY, UserRole.MEMBERSHIP_OFFICER
    )),
    db: Session = Depends(get_db)
):
    application = db.query(MembershipApplication).filter(MembershipApplication.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if review.status == MembershipStatus.APPROVED:
        member = approve_application(db, application, reviewer_username=current_user.username, notes=review.review_notes)
        return {
            "message": "Application approved and digital card generated successfully",
            "membership_id": member.membership_id,
            "card_pdf": member.cards[0].pdf_path if member.cards else None
        }
    else:
        application.status = review.status
        application.review_notes = review.review_notes
        application.reviewed_by = current_user.username
        db.commit()
        return {"message": f"Application status updated to {review.status.value}"}

@router.get("/directory", response_model=List[MemberResponse])
def get_approved_members(
    region: Optional[str] = None,
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Member).filter(Member.status == MembershipStatus.APPROVED)
    if region:
        query = query.filter(Member.ancestral_region == region)
    if city:
        query = query.filter(Member.current_city == city)
    return query.all()
