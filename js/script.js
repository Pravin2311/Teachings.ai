// js/script.js

// === Global Variables ===
const CDN = 'https://cdn.jsdelivr.net/gh/Pravin2311/Teachings.ai@main/'; // ✅ Fixed: no extra spaces

// === Analytics & PWA Detection ===
document.addEventListener('DOMContentLoaded', () => {
  // Track PWA vs Web mode
  const isPWA = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;

  if (typeof gtag === 'function') {
    gtag('event', 'pwa_mode_check', {
      event_category: 'App Mode',
      event_label: isPWA ? 'PWA' : 'Web',
      app_mode: isPWA ? 'PWA' : 'Web'
    });

    gtag('set', 'user_properties', {
      app_mode: isPWA ? 'PWA' : 'Web'
    });
  }

  console.log("App Mode:", isPWA ? 'PWA' : 'Web');

  // Track module clicks
  const buttons = document.querySelectorAll(".module-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const id = button.id;
      if (id && typeof gtag === 'function') {
        gtag('event', 'module_click', {
          event_category: 'Navigation',
          event_label: id,
          app_mode: isPWA ? 'PWA' : 'Web'
        });
      }
    });
  });

  // === Push Notification Setup ===
  const btn = document.getElementById('notify-btn');
  if (!btn) {
    console.warn('🔔 notify-btn not found');
    return;
  }

  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    btn.style.display = 'none';
    return;
  }

  // Register service worker
  navigator.serviceWorker.register('/service-worker.js')
    .then(registration => {
      console.log('✅ SW registered');

      // Check current subscription
      return registration.pushManager.getSubscription();
    })
    .then(sub => {
      if (sub) {
        btn.textContent = '✅ Subscribed!';
        btn.disabled = true;
      } else {
        // Only add listener if not already subscribed
        btn.addEventListener('click', subscribeUser);
      }
    })
    .catch(err => {
      console.error('❌ SW registration failed:', err);
      btn.style.display = 'none';
    });

  // Separate function for subscription
  async function subscribeUser() {
    const permission = await Notification.requestPermission();
    if (permission !== 'granted') {
      alert('Please allow notifications.');
      return;
    }

    // Convert base64 string to Uint8Array
    function urlB64ToUint8Array(base64String) {
      const padding = '='.repeat((4 - base64String.length % 4) % 4);
      const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');
      const rawData = window.atob(base64);
      return new Uint8Array([...rawData].map(c => c.charCodeAt(0)));
    }

    try {
      console.log('🔑 VAPID Key:', window.VAPID_PUBLIC_KEY);

      if (!window.VAPID_PUBLIC_KEY) {
        throw new Error('VAPID_PUBLIC_KEY not set in HTML');
      }

      const applicationServerKey = urlB64ToUint8Array(window.VAPID_PUBLIC_KEY);

      console.log('✅ Converted to Uint8Array:', applicationServerKey);
      console.log('📏 Key Length:', applicationServerKey.length);

      if (applicationServerKey.length !== 32) {
        throw new Error(`Invalid key length: ${applicationServerKey.length}. Must be 32.`);
      }

      const subscription = await navigator.serviceWorker.ready.then(reg =>
        reg.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey
        })
      );

      console.log('🎉 Subscribed:', JSON.stringify(subscription));
      btn.textContent = '✅ Subscribed!';
      btn.disabled = true;

    } catch (err) {
      console.error('❌ Subscribe failed:', err);
      alert('Failed to subscribe. Please try again.');
    }
  }
});