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

// === Push Notification Setup ===
let vapidPublicKey = window.VAPID_PUBLIC_KEY;

// Only run if VAPID key is available
if (vapidPublicKey && 'serviceWorker' in navigator && 'PushManager' in window) {
  // Convert base64 string to Uint8Array
  function urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');
    const rawData = window.atob(base64);
    return Uint8Array.from([...rawData], c => c.charCodeAt(0));
  }

  // Register service worker and handle subscription
  navigator.serviceWorker.register('/service-worker.js')
    .then(registration => {
      console.log('SW registered for push');
      
      // Wait for service worker to be ready
      navigator.serviceWorker.ready.then(reg => {
        // Check if already subscribed
        reg.pushManager.getSubscription().then(sub => {
          if (sub) {
            // Already subscribed
            console.log('Already subscribed');
            updateNotifyButton(true);
            return;
          }

          // Show button if not subscribed
          updateNotifyButton(false);
        });
      });
    })
    .catch(err => {
      console.error('SW registration failed', err);
    });

  // Add click listener to notify button (if it exists)
  function setupNotifyButton() {
    const btn = document.getElementById('notify-btn');
    if (!btn) return;

    btn.addEventListener('click', () => {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          navigator.serviceWorker.ready.then(reg => {
            reg.pushManager.subscribe({
              userVisibleOnly: true,
              applicationServerKey: urlB64ToUint8Array(vapidPublicKey)
            })
            .then(sub => {
              console.log('✅ Subscribed:', JSON.stringify(sub));
              btn.textContent = '✅ Subscribed!';
              btn.disabled = true;
              alert('You’ll get alerts when new modules are added!');
            })
            .catch(err => {
              console.error('❌ Subscribe failed:', err);
              alert('Failed to subscribe. Please try again.');
            });
          });
        } else {
          alert('Please allow notifications to get updates.');
        }
      });
    });
  }

  // Update button text based on subscription
  function updateNotifyButton(isSubscribed) {
    const btn = document.getElementById('notify-btn');
    if (btn) {
      if (isSubscribed) {
        btn.textContent = '✅ Subscribed!';
        btn.disabled = true;
      } else {
        btn.textContent = '🔔 Get Updates';
        btn.disabled = false;
        setupNotifyButton(); // Add click listener
      }
    }
  }

  // Run button setup when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupNotifyButton);
  } else {
    setupNotifyButton();
  }
} else {
  // Push not supported or no VAPID key
  const btn = document.getElementById('notify-btn');
  if (btn) btn.style.display = 'none';
}
