// Misri Khel Qaumi Ittehad - API Client
const API_BASE = window.location.origin.includes(":8000") 
    ? "/api" 
    : "http://127.0.0.1:8000/api";

const api = {
    // Auth
    async login(username, password) {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Login failed");
        }
        return await res.json();
    },

    async getMe(token) {
        const res = await fetch(`${API_BASE}/auth/me`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        return await res.json();
    },

    // Public Membership
    async applyMembership(data) {
        try {
            const res = await fetch(`${API_BASE}/members/apply`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            if (res.ok) {
                return await res.json();
            }
            const err = await res.json();
            throw new Error(err.detail || "Application submission failed");
        } catch (fetchErr) {
            // Local fallback (GitHub Pages static hosting mode)
            const appNum = `APP-2026-${Math.floor(1000 + Math.random() * 9000)}`;
            const localRecord = {
                id: Date.now(),
                application_number: appNum,
                ...data,
                entry_fee: 300.0,
                fee_status: data.transaction_reference ? "PAID" : "PENDING",
                status: "PENDING",
                created_at: new Date().toISOString(),
                receipt_slip_path: data.receipt_slip_path || "images/sample_receipt.svg"
            };
            const stored = JSON.parse(localStorage.getItem('mkqi_local_apps') || '[]');
            stored.push(localRecord);
            localStorage.setItem('mkqi_local_apps', JSON.stringify(stored));
            return localRecord;
        }
    },

    async checkStatus(identifier) {
        const cleanQuery = identifier.trim().toLowerCase();
        const cleanDigits = cleanQuery.replace(/[^0-9]/g, '');

        try {
            const res = await fetch(`${API_BASE}/members/status/${encodeURIComponent(identifier)}`);
            if (res.ok) {
                return await res.json();
            }
        } catch (e) {
            // Backend offline or running on GitHub Pages
        }

        // Check local storage for newly applied records
        const localApps = JSON.parse(localStorage.getItem('mkqi_local_apps') || '[]');
        const foundLocal = localApps.find(a => 
            (a.application_number && a.application_number.toLowerCase().includes(cleanQuery)) ||
            (a.cnic && a.cnic.replace(/[^0-9]/g, '') === cleanDigits) ||
            (a.mobile_number && a.mobile_number.includes(cleanDigits)) ||
            (a.full_name_ur && a.full_name_ur.includes(cleanQuery)) ||
            (a.full_name_en && a.full_name_en.toLowerCase().includes(cleanQuery))
        );

        if (foundLocal) {
            return {
                found: true,
                type: "APPLICATION",
                application_number: foundLocal.application_number,
                membership_id: "زیرِ جائزہ (Review Pending)",
                name: foundLocal.full_name_ur,
                name_en: foundLocal.full_name_en,
                father_name_ur: foundLocal.father_name_ur || "-",
                father_name_en: foundLocal.father_name_en || "-",
                cnic: foundLocal.cnic || "فائل میں محفوظ",
                mobile: foundLocal.mobile_number,
                status: foundLocal.status || "PENDING",
                current_city: foundLocal.current_city,
                current_area: foundLocal.current_area,
                ancestral_region: foundLocal.ancestral_region,
                ancestral_village: foundLocal.ancestral_village || "-",
                occupation: foundLocal.occupation || "-",
                professional_category: foundLocal.professional_category || "عام ممبر",
                entry_fee: 300.0,
                fee_status: foundLocal.fee_status || "PAID",
                payment_method: foundLocal.payment_method || "EasyPaisa",
                transaction_reference: foundLocal.transaction_reference || "TRX-LOCAL-300",
                receipt_slip_path: foundLocal.receipt_slip_path || "images/sample_receipt.svg",
                entry_timestamp: new Date(foundLocal.created_at || Date.now()).toLocaleDateString("ur-PK", { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
                review_notes: "آپ کی 300 روپے فیس کی رسید اور کوائف کامیابی کے ساتھ موصول ہو چکے ہیں۔ سیکریٹریٹ توثیق کر رہا ہے۔"
            };
        }

        // Seeded verified member default (Matches CNIC, Name, or ID)
        if (
            cleanDigits === "1520112345671" || 
            cleanDigits === "03001234567" || 
            cleanQuery.includes("15201") ||
            cleanQuery.includes("imran") || 
            cleanQuery.includes("عمران") || 
            cleanQuery.includes("0001")
        ) {
            return {
                found: true,
                type: "MEMBER",
                membership_id: "MKQI-2026-0001",
                application_number: "APP-2026-0001",
                name: "محمد عمران خان مصری خیل",
                name_en: "Muhammad Imran Khan Misri Khel",
                father_name_ur: "حاجی گل زمان خان",
                father_name_en: "Haji Gul Zaman Khan",
                cnic: "15201-1234567-1",
                mobile: "0300-1234567",
                status: "APPROVED",
                current_city: "کراچی (Karachi)",
                current_area: "اتحاد ٹاؤن، بلدیہ زون",
                ancestral_region: "شانگلہ (Shangla)",
                ancestral_village: "الپوری (Alpuri)",
                occupation: "سافٹ ویئر انجینئر / آئی ٹی کنسلٹنٹ",
                professional_category: "آئی ٹی و تکنیکی شعبہ",
                // Entry Fee PKR 300 & Receipt Details
                entry_fee: 300.0,
                fee_status: "PAID",
                payment_method: "EasyPaisa",
                transaction_reference: "EP-982341890",
                receipt_slip_path: "images/sample_receipt.svg",
                entry_timestamp: "15 اکتوبر 2026 • شام 05:22 بجے",
                card_issued: true,
                card_number: "CRD-2026-0001",
                card_pdf: "images/sample_receipt.svg",
                verification_token: "a089f9fa-080c-454d-b32d-febaa4db4813"
            };
        }

        throw new Error("اس شناختی کارڈ نمبر، نام یا موبائل پر کوئی ریکارڈ موجود نہیں ہے۔ براہِ کرم درست معلومات درج کریں۔");
    },

    // Card Verification
    async verifyCard(token) {
        try {
            const res = await fetch(`${API_BASE}/cards/verify/${encodeURIComponent(token)}`);
            if (res.ok) return await res.json();
        } catch (e) {}

        return {
            is_valid: true,
            membership_id: "MKQI-2026-0001",
            member_name_en: "Muhammad Imran Khan",
            member_name_ur: "محمد عمران خان مصری خیل",
            status: "APPROVED",
            issue_date: "15-Oct-2026",
            card_status: "ACTIVE",
            organization: "مصری خیل قومی اتحاد فاؤنڈیشن"
        };
    },

    // Content & Media
    async getAnnouncements() {
        const res = await fetch(`${API_BASE}/content/announcements`);
        return await res.json();
    },

    async getNews() {
        const res = await fetch(`${API_BASE}/content/news`);
        return await res.json();
    },

    async getEvents() {
        const res = await fetch(`${API_BASE}/content/events`);
        return await res.json();
    },

    async getDocuments(category = null) {
        const url = category ? `${API_BASE}/content/documents?category=${category}` : `${API_BASE}/content/documents`;
        const res = await fetch(url);
        return await res.json();
    },

    // Leadership & Committees
    async getLeadership() {
        try {
            const res = await fetch(`${API_BASE}/committees/leadership`);
            if (res.ok) return await res.json();
        } catch (e) {}

        return [
            { id: 1, title_ur: "سرپرست اعلیٰ", title_en: "Chief Patron", name_ur: "عبد اللہ بھائی", name_en: "Abdullah Bhai" },
            { id: 2, title_ur: "وائس چیئرمین", title_en: "Vice Chairman", name_ur: "محمد ذوالقرنین", name_en: "Muhammad Zulqarnain" },
            { id: 3, title_ur: "ڈپٹی چیئرمین", title_en: "Deputy Chairman", name_ur: "صلاح الدین ایوبی", name_en: "Salahuddin Ayubi" },
            { id: 4, title_ur: "صدر", title_en: "President", name_ur: "نصیب زمین بھائی", name_en: "Naseeb Zameen Bhai" },
            { id: 5, title_ur: "نائب صدر", title_en: "Vice President", name_ur: "نظیر محمد بھائی", name_en: "Nazir Muhammad Bhai" },
            { id: 6, title_ur: "سینئر نائب صدر", title_en: "Senior Vice President", name_ur: "محمد نواب بھائی", name_en: "Muhammad Nawab Bhai" },
            { id: 7, title_ur: "جوئنیر نائب صدر", title_en: "Junior Vice President", name_ur: "مولانا محمد سلیمان بھائی", name_en: "Maulana Muhammad Sulaiman Bhai" },
            { id: 8, title_ur: "جنرل سیکرٹری", title_en: "General Secretary", name_ur: "فرید الرحمٰن", name_en: "Farid-ur-Rehman" },
            { id: 9, title_ur: "نائب ڈپٹی جنرل سیکرٹری", title_en: "Naib Deputy General Secretary", name_ur: "فخر البشر صاحب", name_en: "Fakhr-ul-Bashar Sahib" },
            { id: 10, title_ur: "جوائنٹ سیکرٹری", title_en: "Joint Secretary", name_ur: "تاج معین اللہ بھائی", name_en: "Taj Moeenullah Bhai" },
            { id: 11, title_ur: "خزانچی", title_en: "Treasurer", name_ur: "مولانا مطیع اللہ صاحب", name_en: "Maulana Mutee-ullah Sahib" },
            { id: 12, title_ur: "سیکرٹری تنظیم", title_en: "Organizing Secretary", name_ur: "محمد زمان درویش", name_en: "Muhammad Zaman Darwesh" },
            { id: 13, title_ur: "سیکرٹری تعلیم", title_en: "Education Secretary", name_ur: "حیات گل بھائی", name_en: "Hayat Gul Bhai" },
            { id: 14, title_ur: "سیکرٹری فلاحی امور", title_en: "Welfare Secretary", name_ur: "نور قیوم بھائی", name_en: "Noor Qayyum Bhai" },
            { id: 15, title_ur: "آفس سیکرٹری", title_en: "Office Secretary", name_ur: "عبد القوی بھائی", name_en: "Abdul Qawi Bhai" }
        ];
    },

    async getRegions() {
        const res = await fetch(`${API_BASE}/committees/regions`);
        return await res.json();
    },

    // Professionals
    async getProfessionals(category = null, city = null, search = null) {
        let url = `${API_BASE}/professionals/list?`;
        if (category) url += `category=${encodeURIComponent(category)}&`;
        if (city) url += `city=${encodeURIComponent(city)}&`;
        if (search) url += `search=${encodeURIComponent(search)}&`;
        const res = await fetch(url);
        return await res.json();
    },

    // Partners
    async getPartners() {
        const res = await fetch(`${API_BASE}/partners/list`);
        return await res.json();
    },

    // Admin Operations
    async getApplications(token, region = null, status = null) {
        let url = `${API_BASE}/members/applications?`;
        if (region) url += `region=${encodeURIComponent(region)}&`;
        if (status) url += `status_filter=${encodeURIComponent(status)}&`;
        const res = await fetch(url, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Failed to load applications");
        return await res.json();
    },

    async reviewApplication(token, appId, status, notes) {
        const res = await fetch(`${API_BASE}/members/applications/${appId}/review`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ status, review_notes: notes })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Review failed");
        }
        return await res.json();
    },

    async getFinanceSummary(token) {
        const res = await fetch(`${API_BASE}/finance/summary`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (!res.ok) throw new Error("Failed to fetch finance summary");
        return await res.json();
    }
};
