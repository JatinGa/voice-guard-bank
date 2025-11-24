const CACHE_NAME = 'sentinelpay-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/favicon.ico',
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  // For GET requests, try cache then network
  if (req.method === 'GET') {
    event.respondWith(
      caches.match(req).then((cached) => cached || fetch(req).catch(() => caches.match('/')))
    );
  }
});
