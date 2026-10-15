from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RegionCreate(BaseModel):
    name_ur: str
    name_en: str
    code: str
    description: Optional[str] = None

class RegionResponse(RegionCreate):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class AreaCreate(BaseModel):
    region_id: int
    name_ur: str
    name_en: str
    description: Optional[str] = None

class AreaResponse(AreaCreate):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class OfficeBearerCreate(BaseModel):
    committee_id: int
    member_id: Optional[int] = None
    title_ur: str
    title_en: str
    name_ur: str
    name_en: str
    phone: Optional[str] = None
    email: Optional[str] = None
    is_public: bool = True

class OfficeBearerResponse(OfficeBearerCreate):
    id: int
    is_active: bool
    class Config:
        from_attributes = True

class CommitteeCreate(BaseModel):
    area_id: Optional[int] = None
    name_ur: str
    name_en: str
    committee_type: str = "LOCAL"
    description: Optional[str] = None

class CommitteeResponse(CommitteeCreate):
    id: int
    is_active: bool
    bearers: List[OfficeBearerResponse] = []
    class Config:
        from_attributes = True
