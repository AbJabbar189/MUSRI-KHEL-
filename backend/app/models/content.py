from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title_ur = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    content_ur = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    category = Column(String(50), default="GENERAL")  # URGENT, WELFARE, EDUCATION, EVENT, GENERAL
    is_published = Column(Boolean, default=True)
    published_at = Column(DateTime(timezone=True), server_default=func.now())

class CommunityNews(Base):
    __tablename__ = "community_news"

    id = Column(Integer, primary_key=True, index=True)
    title_ur = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    summary_ur = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    content_ur = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=True)
    author = Column(String(100), default="سیکرٹری اطلاعات")
    is_published = Column(Boolean, default=True)
    published_at = Column(DateTime(timezone=True), server_default=func.now())

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title_ur = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    description_ur = Column(Text, nullable=False)
    description_en = Column(Text, nullable=False)
    event_date = Column(DateTime(timezone=True), nullable=False)
    location_ur = Column(String(255), nullable=False)
    location_en = Column(String(255), nullable=False)
    organizer = Column(String(150), default="مصری خیل قومی اتحاد")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OfficialDocument(Base):
    __tablename__ = "official_documents"

    id = Column(Integer, primary_key=True, index=True)
    title_ur = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=False)
    category = Column(String(100), default="FORM")  # FORM, POLICY, CONSTITUTION_DRAFT, REPORT, MAGAZINE
    file_path = Column(String(255), nullable=False)
    file_size = Column(String(50), nullable=True)
    is_public = Column(Boolean, default=True)
    downloads_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
