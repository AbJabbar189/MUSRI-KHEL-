from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.content import Announcement, CommunityNews, Event, OfficialDocument
from app.schemas.content import (
    AnnouncementResponse, AnnouncementCreate,
    NewsResponse, NewsCreate,
    EventResponse, EventCreate,
    DocumentResponse
)

router = APIRouter(prefix="/content", tags=["Content & News"])

@router.get("/announcements", response_model=List[AnnouncementResponse])
def get_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).filter(Announcement.is_published == True).order_by(Announcement.published_at.desc()).all()

@router.get("/news", response_model=List[NewsResponse])
def get_news(db: Session = Depends(get_db)):
    return db.query(CommunityNews).filter(CommunityNews.is_published == True).order_by(CommunityNews.published_at.desc()).all()

@router.get("/events", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.is_active == True).order_by(Event.event_date.asc()).all()

@router.get("/documents", response_model=List[DocumentResponse])
def get_documents(category: str = None, db: Session = Depends(get_db)):
    query = db.query(OfficialDocument).filter(OfficialDocument.is_public == True)
    if category:
        query = query.filter(OfficialDocument.category == category)
    return query.order_by(OfficialDocument.created_at.desc()).all()
