from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    business_name_ur = Column(String(150), nullable=False)
    business_name_en = Column(String(150), nullable=False)
    business_category = Column(String(100), nullable=False)  # Hospital, Pharmacy, School, Academy, Retail, Legal
    contact_person = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    agreement_verified = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    discounts = relationship("PartnerDiscount", back_populates="partner")

class PartnerDiscount(Base):
    __tablename__ = "partner_discounts"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    title_ur = Column(String(150), nullable=False)
    title_en = Column(String(150), nullable=False)
    discount_percentage = Column(Float, nullable=True)  # e.g., 20.0 (20%)
    terms_ur = Column(Text, nullable=True)
    terms_en = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    partner = relationship("Partner", back_populates="discounts")
    redemptions = relationship("DiscountRedemption", back_populates="discount")

class DiscountRedemption(Base):
    __tablename__ = "discount_redemptions"

    id = Column(Integer, primary_key=True, index=True)
    discount_id = Column(Integer, ForeignKey("partner_discounts.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    redeemed_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(String(255), nullable=True)

    discount = relationship("PartnerDiscount", back_populates="redemptions")
