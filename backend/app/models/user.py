from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from app.database.session import Base

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    CENTRAL_ADMIN = "CENTRAL_ADMIN"
    GENERAL_SECRETARY = "GENERAL_SECRETARY"
    REGIONAL_ADMIN = "REGIONAL_ADMIN"
    COMMITTEE_PRESIDENT = "COMMITTEE_PRESIDENT"
    FINANCE_OFFICER = "FINANCE_OFFICER"
    MEMBERSHIP_OFFICER = "MEMBERSHIP_OFFICER"
    VERIFICATION_OFFICER = "VERIFICATION_OFFICER"
    AUDITOR = "AUDITOR"
    REGISTERED_MEMBER = "REGISTERED_MEMBER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    full_name_ur = Column(String(100), nullable=True)
    full_name_en = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.REGISTERED_MEMBER, nullable=False)
    assigned_region = Column(String(100), nullable=True)  # Regional isolation
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
