// js/script.js
document.addEventListener("DOMContentLoaded", () => {
  // Track PWA vs Web mode
  const isPWA = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;

  gtag('event', 'pwa_mode_check', {
    event_category: 'App Mode',
    event_label: isPWA ? 'PWA' : 'Web',
    app_mode: isPWA ? 'PWA' : 'Web'
  });

  gtag('set', 'user_properties', {
    app_mode: isPWA ? 'PWA' : 'Web'
  });

  console.log("App Mode:", isPWA ? 'PWA' : 'Web');

  // Track module clicks (enhancement)
  const buttons = document.querySelectorAll(".module-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const id = button.id;
      if (id) {
        gtag('event', 'module_click', {
          event_category: 'Navigation',
          event_label: id,
          app_mode: isPWA ? 'PWA' : 'Web'
        });
      }
    });
  });
});

// Global CDN Definition -->

  const CDN = 'https://cdn.jsdelivr.net/gh/Pravin2311/Teachings.ai@main/';
