const CACHE_NAME = 'teachings-ai-v1';

const urlsToCache = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/script.js',
  '/js/musicControl.js',
  '/manifest.json',

  // HTML Pages
  '/alphabets.html',
  '/animals.html',
  '/birds.html',
  '/bodyparts.html',
  '/colors.html',
  '/fruits.html',
  '/healthyfoods.html',
  '/math.html',
  '/numbers.html',
  '/publicservice.html',
  '/vegetables.html',
  '/vehicles.html',
  '/rhyming.html',
  '/sight.html',
  '/word-matching.html',
  '/counting.html',
  '/odd-even.html',
  '/shapes.html',
  '/patterns.html',
  '/Grammar.html',
  '/downloads.html',


  // Assets
  '/assets/audio/background_music.mp3',
  '/assets/audio/click.mp3',
  '/assets/images/app_icon_192.png',
  '/assets/images/app_icon_512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
