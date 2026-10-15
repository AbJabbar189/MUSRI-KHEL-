from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProfessionalCreate(BaseModel):
    member_id: Optional[int] = None
    full_name_ur: str
    full_name_en: str
    father_name_ur: Optional[str] = None
    category: str
    qualification: str
    specialization: Optional[str] = None
    experience_years: int = 0
    current_city: str
    current_workplace: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    linkedin_or_profile: Optional[str] = None
    bio: Optional[str] = None
    is_public: bool = True

class ProfessionalResponse(ProfessionalCreate):
    id: int
    is_verified: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
