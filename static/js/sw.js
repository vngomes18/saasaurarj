const CACHE_NAME = 'aurarj-cache-v2';
const OFFLINE_URL = '/static/offline.html';

const ASSETS_TO_CACHE = [
  '/',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/js/dark-theme.js',
  '/static/js/dropdown-fix.js',
  '/static/js/settings.js',
  '/static/icons/icon-192.svg',
  '/static/icons/icon-512.svg',
  '/static/manifest.json',
  OFFLINE_URL,
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Network-first for navigation requests (HTML) with offline fallback
// IndexedDB helpers for offline form queue
const DB_NAME = 'aurarj-offline';
const STORE_NAME = 'formQueue';

function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'id', autoIncrement: true });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function addToQueue(entry) {
  return openDB().then((db) => new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).add(entry).onsuccess = (e) => resolve(e.target.result);
    tx.oncomplete = () => db.close();
    tx.onerror = () => reject(tx.error);
  }));
}

function getAllQueue() {
  return openDB().then((db) => new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const req = tx.objectStore(STORE_NAME).getAll();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => reject(req.error);
    tx.oncomplete = () => db.close();
  }));
}

function deleteFromQueue(id) {
  return openDB().then((db) => new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).delete(id).onsuccess = () => resolve(true);
    tx.oncomplete = () => db.close();
    tx.onerror = () => reject(tx.error);
  }));
}

async function processQueue() {
  const entries = await getAllQueue();
  let successCount = 0;
  for (const entry of entries) {
    try {
      const res = await fetch(entry.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: entry.body,
        credentials: 'include',
      });
      if (res && res.ok) {
        await deleteFromQueue(entry.id);
        successCount++;
      }
    } catch (err) {
      // Keep in queue
    }
  }

  if (successCount > 0) {
    const clientsList = await self.clients.matchAll();
    clientsList.forEach((client) => {
      client.postMessage({ type: 'toast', message: `${successCount} envios sincronizados`, level: 'success' });
    });
  }
}

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-forms') {
    event.waitUntil(processQueue());
  }
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'sync-now') {
    event.waitUntil(processQueue());
  }
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const isNavigate = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');

  if (isNavigate) {
    // Network-first for HTML
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy)).catch(() => {});
          return res;
        })
        .catch(async () => {
          const cached = await caches.match(req);
          return cached || caches.match(OFFLINE_URL);
        })
    );
    return;
  }

  // Handle POST: queue when offline or failed
  if (req.method === 'POST') {
    event.respondWith((async () => {
      try {
        const res = await fetch(req.clone());
        return res;
      } catch (err) {
        // Clone body as text for queue
        const bodyText = await req.clone().text();
        await addToQueue({ url: req.url, body: bodyText, timestamp: Date.now() });
        // Register background sync if available
        if (self.registration && 'sync' in self.registration) {
          try { await self.registration.sync.register('sync-forms'); } catch (e) {}
        }
        return new Response(JSON.stringify({ queued: true }), {
          status: 202,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    })());
    return;
  }

  // Stale-while-revalidate for static GET assets
  if (req.method === 'GET') {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(req);
      const networkPromise = fetch(req).then((res) => {
        if (res && res.status === 200 && (res.type === 'basic' || res.type === 'cors')) {
          cache.put(req, res.clone()).catch(() => {});
        }
        return res;
      }).catch(() => cached);

      return cached || networkPromise;
    })());
  }
});