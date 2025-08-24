// safeguard.js

(function () {
  // 🔹 Replace this with your Google Apps Script Web App URL
  const REPORT_URL = "https://script.google.com/macros/s/AKfycbxszNBOQIJy-rDdyMAat_r47xt-zQY8unh8O9Gsmz25JjnQI4xWMRh1h-priuiW0fI24w/exec";

  // Show fallback UI
  function showFallback(msg) {
    document.body.innerHTML = `
      <div style="padding:20px; font-family:sans-serif; text-align:center;">
        <h2>⚠️ Oops, something went wrong</h2>
        <p>${msg || "Please try again later."}</p>
        <button onclick="location.reload()">🔄 Reload</button>
      </div>
    `;
  }

  // 🔹 Send error report to Google Sheets
  function reportError(errorInfo) {
    try {
      fetch(REPORT_URL, {
        method: "POST",
        mode: "no-cors", // important for static apps
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(errorInfo),
      });
    } catch (err) {
      console.warn("Failed to send error report:", err);
    }
  }

  // 🔹 Prepare error data
  function buildErrorData(err) {
    return {
      url: location.href,
      userAgent: navigator.userAgent,
      message: err.message || err.toString(),
      stack: err.stack || "no stack",
    };
  }

  // 🔹 Global error catcher
  window.addEventListener("error", (e) => {
    console.error("Caught by safeguard.js:", e.error || e.message);
    reportError(buildErrorData(e.error || e));
    showFallback("An error occurred while loading this module.");
  });

  window.addEventListener("unhandledrejection", (e) => {
    console.error("Unhandled promise:", e.reason);
    reportError(buildErrorData(e.reason || {}));
    showFallback("Something unexpected happened.");
  });

  // 🔹 Auto-wrap DOMContentLoaded
  const origAddEventListener = document.addEventListener;
  document.addEventListener = function (type, listener, options) {
    if (type === "DOMContentLoaded" && typeof listener === "function") {
      const wrapped = function (ev) {
        try {
          listener(ev);
        } catch (err) {
          console.error("safeguard.js trapped error:", err);
          reportError(buildErrorData(err));
          showFallback("The page couldn’t load correctly.");
        }
      };
      return origAddEventListener.call(this, type, wrapped, options);
    }
    return origAddEventListener.call(this, type, listener, options);
  };

  // 🔹 Auto-wrap window.onload
  const origOnload = window.onload;
  window.onload = function (ev) {
    try {
      if (origOnload) origOnload(ev);
    } catch (err) {
      console.error("safeguard.js trapped window.onload error:", err);
      reportError(buildErrorData(err));
      showFallback("The page couldn’t finish loading.");
    }
  };

  console.log("✅ safeguard.js active – errors will be logged to Google Sheets");
})();
