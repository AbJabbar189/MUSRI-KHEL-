# مصری خیل قومی اتحاد فاؤنڈیشن
## Misri Khel Qaumi Ittehad — Complete Digital Community Platform

A dignified, secure, and modern digital platform for the **Misri Khel Qaumi Ittehad Foundation (مصری خیل قومی اتحاد فاؤنڈیشن)**. Inspired by institutional community jamat portals (such as Bantva Memon Jamat `bmjr.net`), tailored with the official Misri Khel green & gold visual identity, and fully localized in **اردو (Urdu)**, **پښتو (Pashto)**, and **English**.

---

## 🌟 Key Features

1. **Official Branding & Design System:**
   - Incorporates the official Misri Khel emblem (mountain peaks, pine valley, hands of brotherhood, crescent & star, wheat laurel).
   - Motto: **اتحاد • خدمت • عزت • ترقی** (Unity • Service • Honor • Progress).
   - Responsive design with bmjr-style counters, download boxes, video highlights, and publication grid.

2. **Multi-Language Support (اردو / پښتو / English):**
   - Instant client-side language switching.
   - Native Right-to-Left (RTL) typography with Nastaliq font styling.

3. **Online Membership & Verifiable Digital Cards:**
   - Online applicant registration wizard with automated application number generator (`APP-2026-XXXX`).
   - Duplicate prevention by mobile number matching.
   - Instant application status tracking for applicants.
   - One-click approval generating a **verifiable digital card with QR code** and downloadable **PDF membership card**.
   - Public QR verification page (`/verify.html`) that validates card authenticity without leaking private personal data.

4. **Secretariat & Administrative Workspace (`/admin.html`):**
   - Administrative review inbox with one-click decision-making (Approve, Under Review, Reject).
   - Regional data isolation (Karachi, Shangla, Torghar, Buner).
   - Financial ledger summary (Income, Expenses, Welfare balance) and voucher entry.
   - Immutable audit logging for governance.

5. **Scholars & Professionals Directory (`/professionals.html`):**
   - Public directory of religious scholars (Ulama), doctors, engineers, lawyers, IT experts, and teachers.
   - Live category and city filters.

6. **Publication & Download Center (Memon-Samaj style):**
   - Dedicated downloadable forms (Membership Form, Marriage/Liaison Form, Constitution Draft).
   - Monthly Misri Khel Samaj bulletin archives.

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+ (Verified on Python 3.14)
- Pip

### 2. Run Database Seeding
To initialize the database tables and populate sample administrative accounts, initial regional committees, sample members, cards, and publications:

```bash
python scripts/seed_data.py
```

### 3. Launch the Server
Start the unified application (which serves both the FastAPI API and the frontend portal):

```bash
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Open your browser at:
- **Public Portal:** `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/index.html`
- **Membership Registration:** `http://127.0.0.1:8000/membership.html`
- **QR Card Verification:** `http://127.0.0.1:8000/verify.html`
- **Professionals Directory:** `http://127.0.0.1:8000/professionals.html`
- **Secretariat / Admin Dashboard:** `http://127.0.0.1:8000/admin.html`
- **Interactive API Documentation:** `http://127.0.0.1:8000/docs`

---

## 🔐 Default Administrative Credentials

| Username | Password | Role | Assigned Region |
| :--- | :--- | :--- | :--- |
| `admin` | `Admin@12345` | Super Administrator | All Regions (Global) |
| `secretary` | `Admin@12345` | General Secretary | All Regions |
| `karachi_admin` | `Admin@12345` | Regional Admin | Karachi |

---

## 🧪 Automated Testing

Execute the backend test suite:

```bash
python -m pytest backend/tests/test_api.py -v
```

All 9 tests verify health check, authentication, duplicate prevention, public directory filters, application review, card generation, and privacy-preserving QR verification.

---

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app & static file mounts
│   │   ├── core/                # Config, JWT, and bcrypt security
│   │   ├── database/            # SQLAlchemy database engine & session
│   │   ├── models/              # Relational models (Members, Cards, Committees, Finance)
│   │   ├── schemas/             # Pydantic v2 schemas
│   │   ├── services/            # Card generation (QR & ReportLab PDF) & member workflows
│   │   ├── api/                 # Sub-routers for auth, members, cards, finance, content
│   │   └── static/              # Storage for logos, QR codes, and generated PDF cards
│   └── tests/                   # Automated pytest suite
├── frontend/
│   ├── public/                  # Public web pages (HTML)
│   │   ├── index.html           # Main Portal (bmjr.net style)
│   │   ├── about.html           # Mission & Vision
│   │   ├── history.html         # Regional & Tribal History
│   │   ├── leadership.html      # Central & Regional Committees
│   │   ├── membership.html      # Online Application & Tracker
│   │   ├── verify.html          # Public QR Card Verification
│   │   ├── professionals.html   # Directory of Scholars & Professionals
│   │   ├── news-events.html     # News, Events & Downloads
│   │   ├── contact.html         # Contact & Regional Desks
│   │   └── admin.html           # Secretariat Dashboard
│   └── src/
│       ├── css/                 # Modern styling & RTL/LTR stylesheets
│       └── js/                  # i18n dictionary (Urdu, Pashto, English) & API client
├── docs/                        # Architecture, Database, and Security documentation
├── scripts/
│   └── seed_data.py             # Database initialization and seeder
└── README.md
```
