import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.member import (
    MembershipApplication,
    Member,
    MembershipCard,
    MembershipStatus,
    CardStatus
)
from app.models.audit import AuditLog
from app.services.card_service import generate_qr_code, generate_membership_card_pdf

def generate_application_number(db: Session) -> str:
    year = datetime.now().year
    count = db.query(MembershipApplication).count() + 1
    return f"APP-{year}-{count:04d}"

def generate_membership_id(db: Session) -> str:
    year = datetime.now().year
    count = db.query(Member).count() + 1
    return f"MKQI-{year}-{count:04d}"

def generate_card_number(db: Session) -> str:
    year = datetime.now().year
    count = db.query(MembershipCard).count() + 1
    return f"CRD-{year}-{count:04d}"

def approve_application(
    db: Session,
    application: MembershipApplication,
    reviewer_username: str,
    notes: str = None
) -> Member:
    # 1. Update application
    application.status = MembershipStatus.APPROVED
    application.reviewed_by = reviewer_username
    application.reviewed_at = datetime.now()
    if notes:
        application.review_notes = notes

    # 2. Create Member
    membership_id = generate_membership_id(db)
    member = Member(
        membership_id=membership_id,
        application_id=application.id,
        full_name_ur=application.full_name_ur,
        full_name_en=application.full_name_en,
        father_name_ur=application.father_name_ur,
        father_name_en=application.father_name_en,
        cnic=application.cnic,
        mobile_number=application.mobile_number,
        current_city=application.current_city,
        current_area=application.current_area,
        ancestral_region=application.ancestral_region,
        ancestral_village=application.ancestral_village,
        entry_fee=application.entry_fee,
        fee_status=application.fee_status,
        payment_method=application.payment_method,
        transaction_reference=application.transaction_reference,
        receipt_slip_path=application.receipt_slip_path,
        occupation=application.occupation,
        professional_category=application.professional_category,
        status=MembershipStatus.APPROVED
    )
    db.add(member)
    db.flush()

    # 3. Issue digital membership card & QR code
    token = str(uuid.uuid4())
    qr_rel_path = generate_qr_code(token)
    card_number = generate_card_number(db)
    
    # Generate PDF
    pdf_rel_path = generate_membership_card_pdf(
        card_number=card_number,
        membership_id=member.membership_id,
        name_en=member.full_name_en,
        name_ur=member.full_name_ur,
        city=member.current_city,
        ancestral_region=member.ancestral_region,
        issue_date=datetime.now().strftime("%d-%b-%Y"),
        qr_filename_rel=qr_rel_path
    )

    card = MembershipCard(
        card_number=card_number,
        member_id=member.id,
        verification_token=token,
        status=CardStatus.ACTIVE,
        qr_code_path=qr_rel_path,
        pdf_path=pdf_rel_path,
        issued_by=reviewer_username
    )
    db.add(card)

    # 4. Audit Log
    audit = AuditLog(
        actor_username=reviewer_username,
        action="APPROVE_APPLICATION",
        target_entity="Member",
        target_id=member.membership_id,
        details=f"Approved application {application.application_number} and issued card {card_number}"
    )
    db.add(audit)
    db.commit()
    db.refresh(member)
    return member
