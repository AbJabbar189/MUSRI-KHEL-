from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.professional import Professional
from app.schemas.professional import ProfessionalResponse, ProfessionalCreate
from app.models.user import User, UserRole
from app.api.auth import require_roles

router = APIRouter(prefix="/professionals", tags=["Professionals & Scholars Directory"])

@router.get("/list", response_model=List[ProfessionalResponse])
def get_professionals(
    category: Optional[str] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Professional).filter(
        Professional.is_public == True,
        Professional.is_verified == True
    )
    if category and category != "ALL":
        query = query.filter(Professional.category == category)
    if city and city != "ALL":
        query = query.filter(Professional.current_city == city)
    if search:
        query = query.filter(
            (Professional.full_name_en.ilike(f"%{search}%")) |
            (Professional.full_name_ur.ilike(f"%{search}%")) |
            (Professional.qualification.ilike(f"%{search}%")) |
            (Professional.specialization.ilike(f"%{search}%"))
        )
    return query.all()

@router.post("/", response_model=ProfessionalResponse)
def add_professional(
    payload: ProfessionalCreate,
    current_user: User = Depends(require_roles(
        UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN, UserRole.GENERAL_SECRETARY
    )),
    db: Session = Depends(get_db)
):
    prof = Professional(**payload.model_dump())
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof
