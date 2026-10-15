from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.session import Base

class Professional(Base):
    __tablename__ = "professionals"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    
    full_name_ur = Column(String(150), nullable=False)
    full_name_en = Column(String(150), nullable=False)
    father_name_ur = Column(String(150), nullable=True)
    
    # Category: Ulama/Religious, Doctor, Engineer, Teacher, Lawyer, Accountant, IT, Business, Student, Other
    category = Column(String(100), index=True, nullable=False)
    qualification = Column(String(200), nullable=False)
    specialization = Column(String(200), nullable=True)
    experience_years = Column(Integer, default=0)
    current_city = Column(String(100), nullable=False)
    current_workplace = Column(String(200), nullable=True)
    
    contact_phone = Column(String(30), nullable=True)
    contact_email = Column(String(100), nullable=True)
    linkedin_or_profile = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    
    is_public = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
