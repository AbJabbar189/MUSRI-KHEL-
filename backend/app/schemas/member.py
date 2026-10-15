from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.member import MembershipStatus, CardStatus

class ApplicationCreate(BaseModel):
    full_name_ur: str = Field(..., min_length=2, max_length=150)
    full_name_en: str = Field(..., min_length=2, max_length=150)
    father_name_ur: Optional[str] = None
    father_name_en: Optional[str] = None
    mobile_number: str = Field(..., min_length=10, max_length=20)
    emergency_contact: Optional[str] = None
    email: Optional[str] = None
    current_city: str
    current_area: str
    ancestral_region: str
    ancestral_village: Optional[str] = None
    clan_sub_tribe: Optional[str] = None
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    professional_category: Optional[str] = None
    declaration_accepted: bool = True

class ApplicationReview(BaseModel):
    status: MembershipStatus
    review_notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    application_number: str
    full_name_ur: str
    full_name_en: str
    father_name_ur: Optional[str] = None
    father_name_en: Optional[str] = None
    mobile_number: str
    current_city: str
    current_area: str
    ancestral_region: str
    ancestral_village: Optional[str] = None
    occupation: Optional[str] = None
    professional_category: Optional[str] = None
    status: MembershipStatus
    review_notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MemberResponse(BaseModel):
    id: int
    membership_id: str
    full_name_ur: str
    full_name_en: str
    father_name_ur: Optional[str] = None
    father_name_en: Optional[str] = None
    mobile_number: str
    current_city: str
    current_area: str
    ancestral_region: str
    ancestral_village: Optional[str] = None
    occupation: Optional[str] = None
    professional_category: Optional[str] = None
    status: MembershipStatus
    joined_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class CardResponse(BaseModel):
    id: int
    card_number: str
    member_id: int
    verification_token: str
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: CardStatus
    qr_code_path: Optional[str] = None
    pdf_path: Optional[str] = None

    class Config:
        from_attributes = True

class PublicVerificationResponse(BaseModel):
    is_valid: bool
    membership_id: str
    member_name_en: str
    member_name_ur: str
    status: str
    issue_date: str
    card_status: str
    organization: str = "مصری خیل قومی اتحاد فاؤنڈیشن"
