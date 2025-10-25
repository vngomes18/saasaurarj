// Register service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/static/js/sw.js')
      .then(async (reg) => {
        // Attempt to register background sync at startup
        if ('sync' in reg) {
          try { await reg.sync.register('sync-forms'); } catch (e) {}
        }

        // Listen for messages from the service worker (for toasts)
        navigator.serviceWorker.addEventListener('message', (event) => {
          const data = event.data || {};
          if (data.type === 'toast' && typeof showToast === 'function') {
            showToast(data.message || 'Ação concluída', data.level || 'info');
          }
        });
      })
      .catch((err) => console.error('SW registration failed:', err));
  });
}

// Handle install prompt
let deferredPrompt;
const installBtn = document.getElementById('pwa-install-btn');
if (installBtn) {
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log('Install prompt outcome:', outcome);
    deferredPrompt = null;
    installBtn.classList.add('d-none');
  });
}

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  if (installBtn) installBtn.classList.remove('d-none');
});

// Optional: notify when installed
window.addEventListener('appinstalled', () => {
  console.log('PWA installed');
  if (installBtn) installBtn.classList.add('d-none');
});

// Offline form queue: intercept forms marked with data-offline-queue="true"
document.addEventListener('DOMContentLoaded', () => {
  const offlineForms = Array.from(document.querySelectorAll('form[data-offline-queue="true"]'));
  offlineForms.forEach((form) => {
    form.addEventListener('submit', async (e) => {
      if (navigator.onLine) return; // allow normal submit online

      e.preventDefault();
      const formData = new FormData(form);
      const body = new URLSearchParams(formData).toString();
      const url = form.getAttribute('action') || window.location.pathname;

      // Save into IndexedDB (same DB used by SW)
      try {
        await queueOfflineForm(url, body);
        if (typeof showToast === 'function') {
          showToast('Sem conexão. Envio salvo e será sincronizado.', 'warning');
        }
        // Trigger background sync (or immediate sync fallback)
        if (navigator.serviceWorker && navigator.serviceWorker.ready) {
          const reg = await navigator.serviceWorker.ready;
          if ('sync' in reg) {
            try { await reg.sync.register('sync-forms'); } catch (e) {}
          } else {
            const sw = navigator.serviceWorker.controller;
            if (sw) sw.postMessage({ type: 'sync-now' });
          }
        }
      } catch (err) {
        console.error('Failed to queue form:', err);
        if (typeof showToast === 'function') {
          showToast('Falha ao salvar offline. Tente novamente.', 'error');
        }
      }
    });
  });
});

// Minimal IndexedDB helper (window context)
const DB_NAME = 'aurarj-offline';
const STORE_NAME = 'formQueue';

function openDBWindow() {
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

async function queueOfflineForm(url, body) {
  const db = await openDBWindow();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const entry = { url, body, timestamp: Date.now() };
    tx.objectStore(STORE_NAME).add(entry).onsuccess = () => resolve(true);
    tx.oncomplete = () => db.close();
    tx.onerror = () => reject(tx.error);
  });
}