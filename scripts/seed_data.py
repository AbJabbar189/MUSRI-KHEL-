import os
import sys

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from datetime import datetime, timedelta
from app.database.session import Base, engine, SessionLocal
from app.models.user import User, UserRole
from app.models.member import MembershipApplication, Member, MembershipCard, MembershipStatus, CardStatus
from app.models.committee import Region, Area, Committee, OfficeBearer, Meeting
from app.models.professional import Professional
from app.models.finance import FinancialTransaction, TransactionType, TransactionStatus
from app.models.partner import Partner, PartnerDiscount
from app.models.content import Announcement, CommunityNews, Event, OfficialDocument
from app.core.security import hash_password
from app.services.member_service import approve_application

def seed():
    print("Initializing Database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Users
        if not db.query(User).filter(User.username == "admin").first():
            print("Creating administrative users...")
            super_admin = User(
                username="admin",
                email="admin@misrikhel.org",
                full_name_ur="مرکزی منتظم اعلیٰ",
                full_name_en="Central Super Administrator",
                hashed_password=hash_password("Admin@12345"),
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_verified=True
            )
            secretary = User(
                username="secretary",
                email="secretary@misrikhel.org",
                full_name_ur="جنرل سیکرٹری",
                full_name_en="General Secretary",
                hashed_password=hash_password("Admin@12345"),
                role=UserRole.GENERAL_SECRETARY,
                is_active=True,
                is_verified=True
            )
            khi_admin = User(
                username="karachi_admin",
                email="karachi@misrikhel.org",
                full_name_ur="ریجنل ایڈمن کراچی",
                full_name_en="Regional Admin Karachi",
                hashed_password=hash_password("Admin@12345"),
                role=UserRole.REGIONAL_ADMIN,
                assigned_region="Karachi",
                is_active=True,
                is_verified=True
            )
            db.add_all([super_admin, secretary, khi_admin])
            db.commit()

        # 2. Regions & Areas
        if db.query(Region).count() == 0:
            print("Creating regions and areas...")
            r_khi = Region(name_ur="کراچی ریجن", name_en="Karachi Region", code="KHI", description="کراچی ڈویژن برائے مصری خیل برادری")
            r_shn = Region(name_ur="شانگلہ ریجن", name_en="Shangla Region", code="SHN", description="ضلع شانگلہ، خیبر پختونخوا")
            r_tgh = Region(name_ur="تورغر ریجن", name_en="Torghar Region", code="TGH", description="ضلع تورغر، خیبر پختونخوا")
            r_bnr = Region(name_ur="بونیر ریجن", name_en="Buner Region", code="BNR", description="ضلع بونیر، خیبر پختونخوا")
            db.add_all([r_khi, r_shn, r_tgh, r_bnr])
            db.flush()

            a_khi1 = Area(region_id=r_khi.id, name_ur="اتحاد ٹاؤن و بلدیہ", name_en="Ittehad Town & Baldia")
            a_khi2 = Area(region_id=r_khi.id, name_ur="منگھوپیر و قصبہ کالونی", name_en="Manghopir & Qasba Colony")
            a_shn1 = Area(region_id=r_shn.id, name_ur="الپوری و پورن", name_en="Alpuri & Puran")
            a_tgh1 = Area(region_id=r_tgh.id, name_ur="جدبہ و کنڈر", name_en="Judba & Khandar")
            db.add_all([a_khi1, a_khi2, a_shn1, a_tgh1])
            db.flush()

            # Committees
            c_central = Committee(name_ur="مرکزی سپریم کونسل", name_en="Central Supreme Council", committee_type="CENTRAL", description="اعلیٰ مشاورتی و انتظامی ادارہ")
            c_khi = Committee(area_id=a_khi1.id, name_ur="کراچی زونل کمیٹی", name_en="Karachi Zonal Committee", committee_type="REGIONAL", description="کراچی کے امور و فلاحی سرگرمیاں")
            c_shn = Committee(area_id=a_shn1.id, name_ur="شانگلہ رابطہ کمیٹی", name_en="Shangla Liaison Committee", committee_type="REGIONAL", description="شانگلہ علاقائی امور")
            db.add_all([c_central, c_khi, c_shn])
            db.flush()

            # Office bearers (Central Cabinet)
            cabinet = [
                ("سرپرست اعلیٰ", "Chief Patron", "عبد اللہ بھائی", "Abdullah Bhai"),
                ("وائس چیئرمین", "Vice Chairman", "محمد ذوالقرنین", "Muhammad Zulqarnain"),
                ("ڈپٹی چیئرمین", "Deputy Chairman", "صلاح الدین ایوبی", "Salahuddin Ayubi"),
                ("صدر", "President", "نصیب زمین بھائی", "Naseeb Zameen Bhai"),
                ("نائب صدر", "Vice President", "نظیر محمد بھائی", "Nazir Muhammad Bhai"),
                ("سینئر نائب صدر", "Senior Vice President", "محمد نواب بھائی", "Muhammad Nawab Bhai"),
                ("جوئنیر نائب صدر", "Junior Vice President", "مولانا محمد سلیمان بھائی", "Maulana Muhammad Sulaiman Bhai"),
                ("جنرل سیکرٹری", "General Secretary", "فرید الرحمٰن", "Farid-ur-Rehman"),
                ("نائب ڈپٹی جنرل سیکرٹری", "Naib Deputy General Secretary", "فخر البشر صاحب", "Fakhr-ul-Bashar Sahib"),
                ("جوائنٹ سیکرٹری", "Joint Secretary", "تاج معین اللہ بھائی", "Taj Moeenullah Bhai"),
                ("خزانچی", "Treasurer", "مولانا مطیع اللہ صاحب", "Maulana Mutee-ullah Sahib"),
                ("سیکرٹری تنظیم", "Organizing Secretary", "محمد زمان درویش", "Muhammad Zaman Darwesh"),
                ("سیکرٹری تعلیم", "Education Secretary", "حیات گل بھائی", "Hayat Gul Bhai"),
                ("سیکرٹری فلاحی امور", "Welfare Secretary", "نور قیوم بھائی", "Noor Qayyum Bhai"),
                ("آفس سیکرٹری", "Office Secretary", "عبد القوی بھائی", "Abdul Qawi Bhai")
            ]
            for title_ur, title_en, name_ur, name_en in cabinet:
                db.add(OfficeBearer(committee_id=c_central.id, title_ur=title_ur, title_en=title_en, name_ur=name_ur, name_en=name_en, is_public=True))
            db.commit()

        # 3. Seed Sample Membership Application & Approved Member
        if db.query(MembershipApplication).count() == 0:
            print("Creating sample membership application & card...")
            app1 = MembershipApplication(
                application_number="APP-2026-0001",
                full_name_ur="عمران خان مصری خیل",
                full_name_en="Imran Khan Misri Khel",
                father_name_ur="گل زمان خان",
                father_name_en="Gul Zaman Khan",
                mobile_number="03001234567",
                current_city="Karachi",
                current_area="Ittehad Town",
                ancestral_region="Shangla",
                ancestral_village="Alpuri",
                occupation="سافٹ ویئر انجینئر",
                professional_category="IT",
                education_level="BS Computer Science",
                declaration_accepted=True,
                status=MembershipStatus.PENDING
            )
            db.add(app1)
            db.commit()
            db.refresh(app1)

            # Approve this application to generate a live membership card with QR & PDF
            approve_application(db, app1, reviewer_username="admin", notes="Verified credentials through local elder liaison.")

            # Second application (pending review)
            app2 = MembershipApplication(
                application_number="APP-2026-0002",
                full_name_ur="ڈاکٹر طارق شاہ",
                full_name_en="Dr. Tariq Shah",
                father_name_ur="فضل الرحمٰن",
                father_name_en="Fazal-ur-Rehman",
                mobile_number="03129876543",
                current_city="Karachi",
                current_area="Qasba Colony",
                ancestral_region="Torghar",
                ancestral_village="Judba",
                occupation="میڈیکل آفیسر (ڈاکٹر)",
                professional_category="Doctor",
                education_level="MBBS",
                declaration_accepted=True,
                status=MembershipStatus.PENDING
            )
            db.add(app2)
            db.commit()

        # 4. Professionals & Scholars Directory
        if db.query(Professional).count() == 0:
            print("Seeding professional directory...")
            p1 = Professional(
                full_name_ur="مولانا مفتی عبدالحلیم مصری خیل",
                full_name_en="Mufti Abdul Haleem",
                category="Religious Scholar",
                qualification="شہادت العالمیہ (وفاق المدارس)",
                specialization="افتاء و علوم اسلامی",
                experience_years=15,
                current_city="Karachi",
                current_workplace="جامعہ اسلامیہ",
                contact_phone="0300-5551122",
                bio="برادری کے مسائل میں شرعی رہنمائی اور مصالحتی خدمات",
                is_public=True,
                is_verified=True
            )
            p2 = Professional(
                full_name_ur="ڈاکٹر سجاد احمد مصری خیل",
                full_name_en="Dr. Sajjad Ahmad",
                category="Doctor",
                qualification="MBBS, FCPS (Cardiology)",
                specialization="ماہر امراض قلب",
                experience_years=12,
                current_city="Karachi",
                current_workplace="سول ہسپتال کراچی",
                contact_phone="0321-4443322",
                bio="مفت میڈیکل کیمپ اور مستحق مریضوں کے لیے طبی رہنمائی",
                is_public=True,
                is_verified=True
            )
            p3 = Professional(
                full_name_ur="انجینئر کامران مصری خیل",
                full_name_en="Engr. Kamran Misri Khel",
                category="Engineer",
                qualification="B.Sc Civil Engineering (NED)",
                specialization="کنسٹرکشن و انفراسٹرکچر",
                experience_years=8,
                current_city="Karachi",
                current_workplace="نیشنل کنسٹرکشن فرم",
                contact_phone="0333-7778899",
                is_public=True,
                is_verified=True
            )
            p4 = Professional(
                full_name_ur="ایڈووکیٹ شیر افضل مصری خیل",
                full_name_en="Advocate Sher Afzal",
                category="Lawyer",
                qualification="LL.B (High Court Bar)",
                specialization="سول و ریونیو لا",
                experience_years=10,
                current_city="Shangla",
                current_workplace="ڈسٹرکٹ بار ایسوسی ایشن",
                contact_phone="0345-8889900",
                is_public=True,
                is_verified=True
            )
            db.add_all([p1, p2, p3, p4])
            db.commit()

        # 5. Announcements, News & Events
        if db.query(Announcement).count() == 0:
            print("Seeding announcements and news...")
            a1 = Announcement(
                title_ur="مصری خیل قومی اتحاد کے باضابطہ ڈیجیٹل پورٹل کا آغاز",
                title_en="Official Launch of Misri Khel Qaumi Ittehad Digital Portal",
                content_ur="الحمد للہ مصری خیل قومی اتحاد کے ممبرشپ اور تنظیمی ریکارڈ کی ڈیجیٹلائزیشن کا باضابطہ آغاز کر دیا گیا ہے۔ تمام برادری افراد آن لائن رجسٹریشن فارم پر کر کے ڈیجیٹل کارڈ حاصل کر سکتے ہیں۔",
                content_en="Alhamdulillah, the digital community platform for Misri Khel Qaumi Ittehad is officially launched. Members can now register online and acquire verifiable digital membership cards.",
                category="URGENT"
            )
            a2 = Announcement(
                title_ur="کراچی اور شانگلہ کی تمام علاقائی کمیٹیوں کا اجلاس برائے فلاحی منصوبہ بندی",
                title_en="Regional Committee Meeting for Community Welfare Strategy",
                content_ur="تمام علاقائی ذمہ داران کو مطلع کیا جاتا ہے کہ آئندہ اتوار کو مرکزی مشاورتی اجلاس منعقد ہوگا جس میں تعلیمی وظائف اور میڈیکل فنڈز پر غور کیا جائے گا۔",
                content_en="Notice to all office bearers regarding upcoming consultation meeting on educational scholarships and healthcare initiatives.",
                category="WELFARE"
            )
            db.add_all([a1, a2])

            n1 = CommunityNews(
                title_ur="شانگلہ و کراچی کے طلبہ کے لیے مفت کیریئر کونسلنگ سیمینار کا کامیاب انعقاد",
                title_en="Successful Career Guidance Seminar for Youth in Karachi",
                summary_ur="طلباء و طالبات کو جدید آئی ٹی اور پروفیشنل تعلیم سے ہم آہنگ کرنے کے لیے شاندار سیمینار کا انعقاد کیا گیا۔",
                summary_en="An interactive career orientation workshop organized for community students and young graduates.",
                content_ur="مصری خیل قومی اتحاد کی جانب سے منعقدہ کیریئر کونسلنگ سیشن میں سینئر ڈاکٹرز، انجینئرز اور آئی ٹی ماہرین نے نوجوانوں کو رہنمائی فراہم کی۔ شرکاء نے ڈیجیٹل سکلز اور جدید ہنر سیکھنے کے عزم کا اظہار کیا۔",
                content_en="The educational session brought together experienced doctors, engineers, and software experts who delivered practical guidance for college and university admissions.",
                author="سیکرٹری اطلاعات"
            )
            db.add(n1)

            e1 = Event(
                title_ur="سالانہ مصری خیل قومی اتحاد برادری کنونشن 2026",
                title_en="Annual Misri Khel Grand Community Convention 2026",
                description_ur="اتحاد، بھائی چارے اور فلاحی مقاصد کے لیے سالانہ برادری کنونشن، جس میں کراچی، شانگلہ، تورغر اور بونیر کے عمائدین اور نوجوان شرکت کریں گے۔",
                description_en="Grand annual gathering focusing on solidarity, mutual assistance, education, and elder counsel.",
                event_date=datetime.now() + timedelta(days=25),
                location_ur="کمیونٹی سینٹر، اتحاد ٹاؤن، کراچی",
                location_en="Community Center, Ittehad Town, Karachi",
                organizer="مرکزی انتظامیہ"
            )
            db.add(e1)

            # Official Downloads (Memon Samaj style download forms)
            d1 = OfficialDocument(
                title_ur="ممبرشپ فارم (پرنٹ ایبل فارمیٹ)",
                title_en="Official Membership Registration Form (PDF)",
                category="FORM",
                file_path="/static/downloads/membership_form.pdf",
                file_size="240 KB",
                downloads_count=142
            )
            d2 = OfficialDocument(
                title_ur="مصری خیل قومی اتحاد - منشور و قواعد وضوابط (مسودہ)",
                title_en="Constitution & Community Code of Conduct Draft",
                category="CONSTITUTION_DRAFT",
                file_path="/static/downloads/constitution_draft.pdf",
                file_size="520 KB",
                downloads_count=98
            )
            d3 = OfficialDocument(
                title_ur="ماہنامہ مصری خیل بلیٹن - شمارہ اول",
                title_en="Monthly Misri Khel Samaj Bulletin - Issue 1",
                category="MAGAZINE",
                file_path="/static/downloads/misri_khel_bulletin_1.pdf",
                file_size="1.2 MB",
                downloads_count=310
            )
            db.add_all([d1, d2, d3])
            db.commit()

        # 6. Partners & Discounts
        if db.query(Partner).count() == 0:
            print("Seeding partner benefits...")
            pr1 = Partner(
                business_name_ur="الشفاء ڈائیگنوسٹک سینٹر و لیبارٹری",
                business_name_en="Al-Shifa Diagnostic & Lab",
                business_category="Medical / Healthcare",
                contact_person="ڈاکٹر طاہر",
                phone="021-3221199",
                city="Karachi",
                address="مین روڈ، اتحاد ٹاؤن، کراچی",
                is_active=True,
                agreement_verified=True
            )
            db.add(pr1)
            db.flush()

            pd1 = PartnerDiscount(
                partner_id=pr1.id,
                title_ur="تمام لیب ٹیسٹوں پر 25 فیصد خصوصی رعایت",
                title_en="25% Discount on all Clinical Lab Tests",
                discount_percentage=25.0,
                terms_ur="مصری خیل قومی اتحاد کا فعال ڈیجیٹل ممبرشپ کارڈ دکھانے پر قابل اطلاق ہے۔",
                terms_en="Applicable on presentation of verified Misri Khel digital membership card."
            )
            db.add(pd1)

            # Financial sample record
            tx1 = FinancialTransaction(
                voucher_no="VCH-2026-0001",
                transaction_type=TransactionType.DONATION,
                category="Community Welfare Fund",
                amount=50000.0,
                description="مخلص برادری ممبر کی جانب سے فلاحی فنڈ برائے طلباء وظائف",
                payment_method="BANK_TRANSFER",
                reference_number="FT-9923841",
                status=TransactionStatus.APPROVED,
                entered_by="admin",
                approved_by="admin"
            )
            db.add(tx1)
            db.commit()

        print("Database seeding completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
