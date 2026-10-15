from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from app.database.session import get_db
from app.models.member import MembershipCard, CardStatus, Member
from app.schemas.member import PublicVerificationResponse
from app.core.config import settings

router = APIRouter(prefix="/cards", tags=["Membership Cards & Verification"])

@router.get("/verify/{token}", response_model=PublicVerificationResponse)
def verify_card_token(token: str, db: Session = Depends(get_db)):
    card = db.query(MembershipCard).filter(MembershipCard.verification_token == token).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification token not found or invalid"
        )
    
    member = card.member
    is_valid = (card.status == CardStatus.ACTIVE)
    
    # Return minimal safe public verification data (respects privacy, no CNIC/phone/address leaked)
    return PublicVerificationResponse(
        is_valid=is_valid,
        membership_id=member.membership_id,
        member_name_en=member.full_name_en,
        member_name_ur=member.full_name_ur,
        status=member.status.value,
        issue_date=card.issue_date.strftime("%d-%b-%Y") if card.issue_date else "N/A",
        card_status=card.status.value,
        organization="مصری خیل قومی اتحاد فاؤنڈیشن"
    )

@router.get("/download/{identifier}")
@router.get("/{identifier}/pdf")
def download_card(identifier: str, db: Session = Depends(get_db)):
    card = db.query(MembershipCard).filter(
        (MembershipCard.card_number == identifier) | 
        (MembershipCard.verification_token == identifier)
    ).first()
    if not card or not card.pdf_path:
        # Check by member's membership_id
        member = db.query(Member).filter(Member.membership_id == identifier).first()
        if member and member.cards:
            card = member.cards[0]

    if not card or not card.pdf_path:
        raise HTTPException(status_code=404, detail="Card PDF not found")
        
    full_path = os.path.join(settings.STATIC_DIR, card.pdf_path.replace("/static/", ""))
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File on disk not found")
        
    return FileResponse(
        path=full_path,
        media_type="application/pdf",
        filename=f"MisriKhel_Card_{card.member.membership_id}.pdf"
    )
