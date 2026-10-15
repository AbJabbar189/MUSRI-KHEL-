from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name_ur = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)  # e.g., KHI, SHN, TGH, BNR
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    areas = relationship("Area", back_populates="region")

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    name_ur = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    region = relationship("Region", back_populates="areas")
    committees = relationship("Committee", back_populates="area")

class Committee(Base):
    __tablename__ = "committees"

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=True)
    name_ur = Column(String(150), nullable=False)
    name_en = Column(String(150), nullable=False)
    committee_type = Column(String(50), default="LOCAL")  # CENTRAL, REGIONAL, LOCAL, ADVISORY, YOUTH
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    area = relationship("Area", back_populates="committees")
    bearers = relationship("OfficeBearer", back_populates="committee")
    meetings = relationship("Meeting", back_populates="committee")

class OfficeBearer(Base):
    __tablename__ = "office_bearers"

    id = Column(Integer, primary_key=True, index=True)
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    
    title_ur = Column(String(100), nullable=False)  # صدر، نائب صدر، جنرل سیکرٹری، خزانچی، رابطہ سیکرٹری
    title_en = Column(String(100), nullable=False)  # President, Vice President, General Secretary, Finance Secretary
    name_ur = Column(String(150), nullable=False)
    name_en = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    is_public = Column(Boolean, default=True)
    term_start = Column(DateTime(timezone=True), nullable=True)
    term_end = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    committee = relationship("Committee", back_populates="bearers")

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    committee_id = Column(Integer, ForeignKey("committees.id"), nullable=False)
    title_ur = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    meeting_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(200), nullable=True)
    agenda = Column(Text, nullable=True)
    minutes = Column(Text, nullable=True)
    decisions = Column(Text, nullable=True)
    conducted_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    committee = relationship("Committee", back_populates="meetings")
