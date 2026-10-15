import os
import qrcode
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from app.core.config import settings

# Credit card dimensions: 85.6 mm x 53.98 mm
CARD_WIDTH = 85.6 * mm
CARD_HEIGHT = 53.98 * mm

def generate_qr_code(verification_token: str) -> str:
    verification_url = f"{settings.BASE_URL}/verify.html?token={verification_token}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=1,
    )
    qr.add_data(verification_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0D472B", back_color="white")
    
    filename = f"qr_{verification_token}.png"
    filepath = os.path.join(settings.QR_DIR, filename)
    img.save(filepath)
    return f"/static/qr/{filename}"

def generate_membership_card_pdf(
    card_number: str,
    membership_id: str,
    name_en: str,
    name_ur: str,
    city: str,
    ancestral_region: str,
    issue_date: str,
    qr_filename_rel: str
) -> str:
    pdf_filename = f"card_{membership_id.replace('/', '_').replace('-', '_')}.pdf"
    pdf_path = os.path.join(settings.CARDS_DIR, pdf_filename)
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(CARD_WIDTH, CARD_HEIGHT),
        leftMargin=3 * mm,
        rightMargin=3 * mm,
        topMargin=3 * mm,
        bottomMargin=3 * mm
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=9,
        textColor=colors.HexColor('#0D472B'),
        alignment=1
    )
    motto_style = ParagraphStyle(
        'CardMotto',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=5.5,
        leading=7,
        textColor=colors.HexColor('#B8860B'),
        alignment=1
    )
    text_style = ParagraphStyle(
        'CardText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor('#1A202C')
    )
    bold_style = ParagraphStyle(
        'CardBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor('#0D472B')
    )
    
    story = []
    
    # Organization Header
    story.append(Paragraph("MISRI KHEL QAUMI ITTEHAD FOUNDATION", title_style))
    story.append(Paragraph("Unity • Service • Honor • Progress", motto_style))
    story.append(Spacer(1, 1.5 * mm))
    
    # QR code full path
    qr_full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), qr_filename_rel.lstrip("/"))
    qr_elem = None
    if os.path.exists(qr_full_path):
        qr_elem = RLImage(qr_full_path, width=22 * mm, height=22 * mm)
    
    # Logo full path
    logo_full_path = os.path.join(settings.STATIC_DIR, "images", "logo.jpg")
    logo_elem = None
    if os.path.exists(logo_full_path):
        logo_elem = RLImage(logo_full_path, width=16 * mm, height=16 * mm)
    
    # Member details table
    details_data = [
        [Paragraph(f"<b>Name:</b> {name_en}", text_style), qr_elem or ""],
        [Paragraph(f"<b>ID:</b> {membership_id}", bold_style), ""],
        [Paragraph(f"<b>Region:</b> {ancestral_region} | {city}", text_style), ""],
        [Paragraph(f"<b>Issued:</b> {issue_date}", text_style), Paragraph("<font size=4.5 color='#0F5132'>SCAN TO VERIFY</font>", title_style)]
    ]
    
    t = Table(details_data, colWidths=[54 * mm, 25 * mm], rowHeights=[6.5 * mm, 6.5 * mm, 6.5 * mm, 6.5 * mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (1, 0), (1, 2)),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(t)
    doc.build(story)
    
    return f"/static/cards/{pdf_filename}"
