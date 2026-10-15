from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.committee import Region, Area, Committee, OfficeBearer
from app.schemas.committee import (
    RegionResponse, RegionCreate,
    AreaResponse, AreaCreate,
    CommitteeResponse, CommitteeCreate,
    OfficeBearerResponse, OfficeBearerCreate
)
from app.models.user import User, UserRole
from app.api.auth import require_roles

router = APIRouter(prefix="/committees", tags=["Committees & Hierarchy"])

@router.get("/regions", response_model=List[RegionResponse])
def get_regions(db: Session = Depends(get_db)):
    return db.query(Region).filter(Region.is_active == True).all()

@router.get("/areas", response_model=List[AreaResponse])
def get_areas(region_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Area).filter(Area.is_active == True)
    if region_id:
        query = query.filter(Area.region_id == region_id)
    return query.all()

@router.get("/list", response_model=List[CommitteeResponse])
def get_committees(area_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Committee).filter(Committee.is_active == True)
    if area_id:
        query = query.filter(Committee.area_id == area_id)
    return query.all()

@router.get("/leadership", response_model=List[OfficeBearerResponse])
def get_leadership(is_public: bool = True, db: Session = Depends(get_db)):
    return db.query(OfficeBearer).filter(
        OfficeBearer.is_active == True,
        OfficeBearer.is_public == is_public
    ).all()

@router.post("/regions", response_model=RegionResponse)
def create_region(
    payload: RegionCreate,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN)),
    db: Session = Depends(get_db)
):
    region = Region(**payload.model_dump())
    db.add(region)
    db.commit()
    db.refresh(region)
    return region

@router.post("/areas", response_model=AreaResponse)
def create_area(
    payload: AreaCreate,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.CENTRAL_ADMIN, UserRole.REGIONAL_ADMIN)),
    db: Session = Depends(get_db)
):
    area = Area(**payload.model_dump())
    db.add(area)
    db.commit()
    db.refresh(area)
    return area
