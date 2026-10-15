# Security & Data Governance Checklist
## Misri Khel Qaumi Ittehad Digital Platform

### 1. Data Minimization & Privacy
- [x] **No Mandatory CNIC or Sensitive Identifiers by Default:** National identity card numbers are not collected or required by default during community self-registration.
- [x] **Safe Public QR Verification:** The public verification endpoint (`/api/cards/verify/{token}`) only exposes verification validity, member name, and membership ID. Mobile numbers, full residential addresses, and family details are never leaked to public verifiers.
- [x] **Independent Directory Permissions:** Being a registered member does not automatically publish a member's profile into the public Scholars & Professionals directory. Listing requires explicit consent and administrator verification.

### 2. Authentication & Authorization
- [x] **Salted Password Hashing:** Uses `bcrypt` with cryptographic salt generation. Plaintext passwords are never logged or stored.
- [x] **Role-Based Access Control (RBAC):** Backend endpoints strictly verify user roles (`SUPER_ADMIN`, `CENTRAL_ADMIN`, `GENERAL_SECRETARY`, `REGIONAL_ADMIN`, `FINANCE_OFFICER`). UI button hiding is accompanied by mandatory server-side permission enforcement.
- [x] **Regional Isolation:** Regional administrators (e.g. `karachi_admin`) are restricted to viewing and managing records belonging to their assigned region.

### 3. Application Protection
- [x] **Duplicate Application Prevention:** Submissions check against existing pending or active members with the same mobile number to prevent fraudulent duplicate cards.
- [x] **Input Validation:** Strong type and length constraints enforced via Pydantic v2 schemas.
- [x] **Audit Trail:** Sensitive operations (such as approving applications, generating cards, issuing vouchers) record an immutable entry in the `audit_logs` table.

### 4. Production Deployment Best Practices
- [ ] Set `DEBUG=False` in `.env`.
- [ ] Generate a secure 64-character random string for `SECRET_KEY`.
- [ ] Restrict `CORS_ORIGINS` to the exact production domain.
- [ ] Serve behind reverse proxy (Nginx or Caddy) with automated TLS/HTTPS certificates.
- [ ] Configure daily automated database backups of `misri_khel.db` or PostgreSQL dumps.
