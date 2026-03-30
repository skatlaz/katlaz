// FILE: app/katlaz.js

window.katlaz = {
    call: function(name, data = {}) {
        const payload = JSON.stringify({ name, data });

        if (window.webkit?.messageHandlers?.katlaz) {
            window.webkit.messageHandlers.katlaz.postMessage(payload);
        } else {
            console.warn("Katlaz bridge not found");
        }
    }
};

// =============================
// UI BINDING SYSTEM
// =============================

function bindUI() {
    const elements = document.querySelectorAll("[@click]");

    elements.forEach(el => {
        const fn = el.getAttribute("@click");

        el.addEventListener("click", () => {
            katlaz.call(fn);
        });
    });
}

document.addEventListener("DOMContentLoaded", bindUI);
