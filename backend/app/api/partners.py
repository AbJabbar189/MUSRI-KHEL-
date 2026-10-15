from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.partner import Partner, PartnerDiscount

router = APIRouter(prefix="/partners", tags=["Partner Benefits"])

@router.get("/list")
def get_partners(db: Session = Depends(get_db)):
    partners = db.query(Partner).filter(
        Partner.is_active == True,
        Partner.agreement_verified == True
    ).all()
    results = []
    for p in partners:
        results.append({
            "id": p.id,
            "business_name_ur": p.business_name_ur,
            "business_name_en": p.business_name_en,
            "category": p.business_category,
            "contact_person": p.contact_person,
            "city": p.city,
            "address": p.address,
            "discounts": [
                {
                    "id": d.id,
                    "title_ur": d.title_ur,
                    "title_en": d.title_en,
                    "discount_percentage": d.discount_percentage,
                    "terms_ur": d.terms_ur,
                    "terms_en": d.terms_en
                }
                for d in p.discounts if d.is_active
            ]
        })
    return results
