from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_username = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)  # APPROVE_APPLICATION, ISSUE_CARD, UPDATE_STATUS, etc.
    target_entity = Column(String(100), nullable=False)  # Member, Application, FinancialTransaction, etc.
    target_id = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
