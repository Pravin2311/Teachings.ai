// js/script.js

document.addEventListener("DOMContentLoaded", () => {
  // Track module button clicks
  const buttons = document.querySelectorAll(".module-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const id = button.id;
      if (id) {
        window.location.href = `${id}.html`;
      }
    });
  });

  // Track if user is using PWA or Web
  const isPWA = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;

  // Send GA4 event
  gtag('event', 'pwa_mode_check', {
    event_category: 'App Mode',
    event_label: isPWA ? 'PWA' : 'Web',
    app_mode: isPWA ? 'PWA' : 'Web'
  });

  // Optionally, set user property for segmentation
  gtag('set', 'user_properties', {
    app_mode: isPWA ? 'PWA' : 'Web'
  });

  console.log("GA4 App Mode Tracked:", isPWA ? 'PWA' : 'Web');
});
