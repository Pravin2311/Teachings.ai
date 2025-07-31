const CACHE_NAME = 'teachings-ai-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/script.js',
  '/js/musicControl.js',
  '/shapes/index.html',
  '/shapes/shapes.js',
  '/assets/audio/background_music.mp3',
  '/assets/audio/click.mp3',
  '/assets/images/app_icon_192.png',
  '/assets/images/app_icon_512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
