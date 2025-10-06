// CMUJ Wiki - Service Worker for PWA Support
// Version 2025-01-06

const CACHE_NAME = 'cmuj-wiki-v2025-01-06';
const BASE_PATH = '/cmuj-wiki/';

// Core files to cache immediately (app shell)
const CORE_CACHE = [
  BASE_PATH,
  BASE_PATH + 'index.html',
  BASE_PATH + 'javascripts/password-gate.js',
  BASE_PATH + 'stylesheets/nojs-protection.css',
  BASE_PATH + 'stylesheets/homepage-widget.css',
  BASE_PATH + 'stylesheets/quiz.css',
  BASE_PATH + 'stylesheets/calendar.css',
  BASE_PATH + 'manifest.json'
];

// Install event - cache core files
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[ServiceWorker] Caching core files');
        return cache.addAll(CORE_CACHE);
      })
      .then(() => self.skipWaiting()) // Activate immediately
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[ServiceWorker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim()) // Take control immediately
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          // Return cached version
          return cachedResponse;
        }

        // Not in cache, fetch from network
        return fetch(event.request).then((networkResponse) => {
          // Don't cache non-GET requests or non-successful responses
          if (event.request.method !== 'GET' || !networkResponse || networkResponse.status !== 200) {
            return networkResponse;
          }

          // Clone the response
          const responseToCache = networkResponse.clone();

          // Cache the fetched response for future use
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });

          return networkResponse;
        });
      })
      .catch(() => {
        // Network failed, user is offline
        // Return a custom offline page if you want
        console.log('[ServiceWorker] Fetch failed; returning offline page');
      })
  );
});

// Handle service worker messages (for future features)
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
