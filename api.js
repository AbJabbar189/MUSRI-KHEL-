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
        const res = await fetch(`${API_BASE}/members/apply`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Application submission failed");
        }
        return await res.json();
    },

    async checkStatus(identifier) {
        const res = await fetch(`${API_BASE}/members/status/${encodeURIComponent(identifier)}`);
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Record not found");
        }
        return await res.json();
    },

    // Card Verification
    async verifyCard(token) {
        const res = await fetch(`${API_BASE}/cards/verify/${encodeURIComponent(token)}`);
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Invalid or unverified token");
        }
        return await res.json();
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
        const res = await fetch(`${API_BASE}/committees/leadership`);
        return await res.json();
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
