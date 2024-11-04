const CACHE_NAME = '{{ build.app_name }} {{ version }}';
const urlsToCache = [
  '/',
  '/index.html',
  '/settings.js',
  '/nprompter.css',
  '/app.js',
  // Add other assets to cache
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});