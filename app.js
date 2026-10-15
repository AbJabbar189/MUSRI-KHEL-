// Misri Khel Qaumi Ittehad - App Interactions
document.addEventListener("DOMContentLoaded", () => {
    // Mobile navigation toggle with backdrop/close on click outside
    const toggleBtn = document.querySelector(".mobile-toggle");
    const navMenu = document.querySelector(".nav-menu");
    
    if (toggleBtn && navMenu) {
        toggleBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            navMenu.classList.toggle("show");
            toggleBtn.innerHTML = navMenu.classList.contains("show") ? "✕" : "☰";
        });

        // Auto close when tapping any link
        navMenu.querySelectorAll(".nav-link").forEach(link => {
            link.addEventListener("click", () => {
                navMenu.classList.remove("show");
                toggleBtn.innerHTML = "☰";
            });
        });

        // Close when tapping outside
        document.addEventListener("click", (e) => {
            if (!navMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
                navMenu.classList.remove("show");
                toggleBtn.innerHTML = "☰";
            }
        });
    }

    // Load dynamic ticker if present
    const tickerElem = document.querySelector(".ticker-text");
    if (tickerElem && typeof api !== "undefined") {
        api.getAnnouncements().then(items => {
            if (items && items.length > 0) {
                const isEn = document.documentElement.lang === "en";
                const isPs = document.documentElement.lang === "ps";
                tickerElem.textContent = isEn ? items[0].title_en : items[0].title_ur;
            }
        }).catch(() => {});
    }
});

// Toast Notification
function showToast(message, type = "success") {
    let toast = document.getElementById("toast-container");
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast-container";
        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.zIndex = "99999";
        document.body.appendChild(toast);
    }
    
    const item = document.createElement("div");
    item.style.padding = "14px 24px";
    item.style.borderRadius = "8px";
    item.style.marginBottom = "10px";
    item.style.color = "#fff";
    item.style.fontWeight = "600";
    item.style.boxShadow = "0 4px 12px rgba(0,0,0,0.2)";
    item.style.fontSize = "14px";
    item.style.transition = "all 0.3s ease";
    
    if (type === "success") item.style.background = "#0D472B";
    else if (type === "error") item.style.background = "#DC2626";
    else item.style.background = "#D4AF37";
    
    item.textContent = message;
    toast.appendChild(item);
    
    setTimeout(() => {
        item.style.opacity = "0";
        setTimeout(() => item.remove(), 300);
    }, 4000);
}
