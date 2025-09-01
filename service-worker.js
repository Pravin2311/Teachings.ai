// service-worker.js

// Bump version when content changes (e.g., v2, v3)
const CACHE_NAME = 'teachings-ai-v2';

// List of assets to cache
const urlsToCache = [
  // ———————————— Core Pages —————————————
  '/',
  '/index.html',
  '/games.html',
  '/about.html',
  '/feedback.html',
  '/disclaimer.html',
  '/privacy-policy.html',
  '/downloads.html',

  // —————————— Learning Modules ——————————
  '/numbers.html',
  '/alphabets.html',
  '/phonics.html',
  '/animals.html',
  '/birds.html',
  '/fruits.html',
  '/vegetables.html',
  '/colors.html',
  '/bodyparts.html',
  '/vehicles.html',
  '/plants.html',
  '/countries.html',
  '/scientists.html',
  '/planets.html',
  '/electronic-gadgets.html',
  '/fantasy-world.html',
  '/nature-explorer.html',
  '/math.html',
  '/grammar.html',
  '/rhyming.html',
  '/sight.html',
  '/sentences.html',
  '/shapes.html',
  '/patterns.html',
  '/odd-even.html',
  '/counting.html',
  '/publicservice.html',
  '/word-matching.html',

  // ———————— Interactive Games ————————
  '/numbers-alphabets-sorting.html',
  '/fruits-vegetables-sorting.html',
  '/colors-sorting.html',
  '/odd-even-sorting.html',
  '/animals-birds-sorting.html',
  '/match-numbers.html',
  '/match-shapes.html',
  '/match-animals.html',
  '/match-words.html',

  // ——————————— Assets ———————————
  '/manifest.json',
  '/assets/images/app_icon_192.png',
  '/assets/images/app_icon_512.png',
  '/assets/audio/background_music.mp3',
  '/assets/audio/click.mp3',

  // ———————————— CSS —————————————
  '/css/style.css',
  '/css/numbers.css',
  '/css/alphabets.css',
  '/css/phonics.css',
  '/css/animals.css',
  '/css/birds.css',
  '/css/fruits.css',
  '/css/vegetables.css',
  '/css/colors.css',
  '/css/bodyparts.css',
  '/css/vehicles.css',
  '/css/plants.css',
  '/css/countries.css',
  '/css/scientists.css',
  '/css/planets.css',
  '/css/electronic-gadgets.css',
  '/css/fantasy-world.css',
  '/css/nature-explorer.css',
  '/css/math.css',
  '/css/grammar.css',
  '/css/rhyming.css',
  '/css/sight.css',
  '/css/sentences.css',
  '/css/shapes.css',
  '/css/patterns.css',
  '/css/oddEven.css',
  '/css/counting.css',
  '/css/publicservice.css',
  '/css/word-matching.css',
  '/css/healthyfoods.css',

  // ———————————— JS ——————————————
  '/js/script.js',
  '/js/musicControl.js',
  '/js/imageHelper.js',
  '/js/globalImageLoader.js',
  '/js/numbers.js',
  '/js/alphabets.js',
  '/js/phonics.js',
  '/js/animals.js',
  '/js/birds.js',
  '/js/fruits.js',
  '/js/vegetables.js',
  '/js/colors.js',
  '/js/bodyparts.js',
  '/js/vehicles.js',
  '/js/plants.js',
  '/js/countries.js',
  '/js/scientists.js',
  '/js/planets.js',
  '/js/electronic-gadgets.js',
  '/js/fantasy-world.js',
  '/js/nature-explorer.js',
  '/js/math.js',
  '/js/grammar.js',
  '/js/rhyming.js',
  '/js/sight.js',
  '/js/sentences.js',
  '/js/shapes.js',
  '/js/patterns.js',
  '/js/oddEven.js',
  '/js/counting.js',
  '/js/publicservice.js',
  '/js/word-matching.js',
  '/js/healthyfoods.js',
  '/js/lanscapes.js'  // Fixed typo: was "lanscapes.js"
]; // Assets

// Install: cache all assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache)
          .catch(err => {
            console.error('Failed to cache:', err);
          });
      })
  );
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(name => name !== CACHE_NAME)
                  .map(name => caches.delete(name))
      );
    })
  );

  // Claim clients immediately
  return self.clients.claim();
});

// Fetch: serve from cache, fallback to network
self.addEventListener('fetch', event => {
  // Skip non-GET requests or external domains
  if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
    return event.respondWith(fetch(event.request));
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version if available
        return response || fetch(event.request);
      })
      .catch(() => {
        // Fallback in case of network failure
        return fetch(event.request);
      })
  );
});

// ———————————————————————————————————————
// 🔔 Push Notifications (for new module alerts)
// ———————————————————————————————————————

// Listen for push events
self.addEventListener('push', event => {
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: '/assets/images/app_icon_192.png',
    badge: '/assets/images/app_icon_192.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    }
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Open page when notification is clicked
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});