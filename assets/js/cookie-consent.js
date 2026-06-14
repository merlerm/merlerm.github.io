// Minimal GDPR cookie-consent banner for Google Analytics (Consent Mode v2).
// Analytics storage stays "denied" (set in scripts.liquid) until the visitor accepts.
(function () {
  "use strict";

  var STORAGE_KEY = "cookie-consent";
  var banner = document.getElementById("cookie-banner");
  if (!banner) return;

  function hasStoredChoice() {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      return v === "granted" || v === "denied";
    } catch (e) {
      return false;
    }
  }

  function gtag() {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(arguments);
  }

  function setConsent(choice) {
    try {
      localStorage.setItem(STORAGE_KEY, choice);
    } catch (e) {
      /* localStorage unavailable (private mode) — choice just won't persist */
    }
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", { analytics_storage: choice });
    } else {
      gtag("consent", "update", { analytics_storage: choice });
    }
    hideBanner();
  }

  function showBanner() {
    banner.hidden = false;
    // next frame so the CSS transition runs
    requestAnimationFrame(function () {
      banner.classList.add("cookie-banner-visible");
    });
  }

  function hideBanner() {
    banner.classList.remove("cookie-banner-visible");
    window.setTimeout(function () {
      banner.hidden = true;
    }, 300);
  }

  banner.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-consent]");
    if (!btn) return;
    setConsent(btn.getAttribute("data-consent"));
  });

  if (!hasStoredChoice()) {
    showBanner();
  }
})();
