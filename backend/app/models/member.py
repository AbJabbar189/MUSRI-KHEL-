from sqlalchemy import Column, Integer, Float, String, Text, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database.session import Base

class MembershipStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"

class MembershipApplication(Base):
    __tablename__ = "membership_applications"

    id = Column(Integer, primary_key=True, index=True)
    application_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # Personal Info
    full_name_ur = Column(String(150), nullable=False)
    full_name_en = Column(String(150), nullable=False)
    father_name_ur = Column(String(150), nullable=True)
    father_name_en = Column(String(150), nullable=True)
    
    # Contact Info
    mobile_number = Column(String(20), index=True, nullable=False)
    emergency_contact = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Geographic distribution
    current_city = Column(String(100), nullable=False)  # Karachi, Rawalpindi, etc.
    current_area = Column(String(150), nullable=False)  # e.g., Ittehad Town, Manghopir, Qasba Colony
    ancestral_region = Column(String(100), nullable=False)  # Shangla, Torghar, Buner, etc.
    ancestral_village = Column(String(150), nullable=True)
    clan_sub_tribe = Column(String(100), nullable=True)  # Misri Khel sub-clan
    
    # Professional & Education
    occupation = Column(String(150), nullable=True)
    education_level = Column(String(100), nullable=True)
    professional_category = Column(String(100), nullable=True)
    
    # CNIC & Financial Entry Fee
    cnic = Column(String(25), index=True, nullable=True)
    entry_fee = Column(Float, default=300.0, nullable=False)
    fee_status = Column(String(50), default="PAID", nullable=False)
    payment_method = Column(String(50), default="EasyPaisa", nullable=True)
    transaction_reference = Column(String(100), nullable=True)
    receipt_slip_path = Column(String(255), nullable=True)

    # Documents & Meta
    photo_path = Column(String(255), nullable=True)
    declaration_accepted = Column(Boolean, default=True)
    
    # Workflow
    status = Column(SQLEnum(MembershipStatus), default=MembershipStatus.PENDING, index=True, nullable=False)
    review_notes = Column(Text, nullable=True)
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    member = relationship("Member", back_populates="application", uselist=False)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(String(50), unique=True, index=True, nullable=False)  # e.g., MKQI-2026-0001
    application_id = Column(Integer, ForeignKey("membership_applications.id"), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    full_name_ur = Column(String(150), nullable=False)
    full_name_en = Column(String(150), nullable=False)
    father_name_ur = Column(String(150), nullable=True)
    father_name_en = Column(String(150), nullable=True)
    cnic = Column(String(25), index=True, nullable=True)
    mobile_number = Column(String(20), index=True, nullable=False)
    current_city = Column(String(100), nullable=False)
    current_area = Column(String(150), nullable=False)
    ancestral_region = Column(String(100), nullable=False)
    ancestral_village = Column(String(150), nullable=True)
    
    # Financial details
    entry_fee = Column(Float, default=300.0, nullable=False)
    fee_status = Column(String(50), default="PAID", nullable=False)
    payment_method = Column(String(50), default="EasyPaisa", nullable=True)
    transaction_reference = Column(String(100), nullable=True)
    receipt_slip_path = Column(String(255), nullable=True)
    
    occupation = Column(String(150), nullable=True)
    professional_category = Column(String(100), nullable=True)
    photo_path = Column(String(255), nullable=True)
    
    status = Column(SQLEnum(MembershipStatus), default=MembershipStatus.APPROVED, index=True, nullable=False)
    joined_date = Column(DateTime(timezone=True), server_default=func.now())
    
    application = relationship("MembershipApplication", back_populates="member")
    cards = relationship("MembershipCard", back_populates="member")

class CardStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"

class MembershipCard(Base):
    __tablename__ = "membership_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(50), unique=True, index=True, nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    verification_token = Column(String(100), unique=True, index=True, nullable=False)
    
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(CardStatus), default=CardStatus.ACTIVE, nullable=False)
    
    qr_code_path = Column(String(255), nullable=True)
    pdf_path = Column(String(255), nullable=True)
    
    issued_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    member = relationship("Member", back_populates="cards")
