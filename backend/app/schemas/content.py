from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnnouncementCreate(BaseModel):
    title_ur: str
    title_en: str
    content_ur: str
    content_en: str
    category: str = "GENERAL"

class AnnouncementResponse(AnnouncementCreate):
    id: int
    is_published: bool
    published_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class NewsCreate(BaseModel):
    title_ur: str
    title_en: str
    summary_ur: Optional[str] = None
    summary_en: Optional[str] = None
    content_ur: str
    content_en: str
    image_path: Optional[str] = None
    author: str = "سیکرٹری اطلاعات"

class NewsResponse(NewsCreate):
    id: int
    is_published: bool
    published_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title_ur: str
    title_en: str
    description_ur: str
    description_en: str
    event_date: datetime
    location_ur: str
    location_en: str
    organizer: str = "مصری خیل قومی اتحاد"

class EventResponse(EventCreate):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: int
    title_ur: str
    title_en: str
    category: str
    file_path: str
    file_size: Optional[str] = None
    downloads_count: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
