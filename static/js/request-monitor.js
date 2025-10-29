/**
 * Monitor de Requisições
 * Exibe estatísticas e alertas sobre uso de API
 */

class RequestMonitor {
    constructor() {
        this.isVisible = false;
        this.updateInterval = null;
        this.createMonitorUI();
        
        // Só mostrar em desenvolvimento
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            this.setupKeyboardShortcut();
        }
    }
    
    /**
     * Criar interface do monitor
     */
    createMonitorUI() {
        const monitor = document.createElement('div');
        monitor.id = 'request-monitor';
        monitor.innerHTML = [
            '<div class="monitor-header">',
                '<span>📊 Request Monitor</span>',
                '<button class="monitor-close" onclick="requestMonitor.hide()">×</button>',
            '</div>',
            '<div class="monitor-content">',
                '<div class="monitor-stat">',
                    '<label>Cache:</label>',
                    '<span id="cache-size">0</span>',
                '</div>',
                '<div class="monitor-stat">',
                    '<label>Fila:</label>',
                    '<span id="queue-size">0</span>',
                '</div>',
                '<div class="monitor-stat">',
                    '<label>Requisições/min:</label>',
                    '<span id="current-requests">0</span>/<span id="max-requests">30</span>',
                '</div>',
                '<div class="monitor-stat">',
                    '<label>Status:</label>',
                    '<span id="processing-status">Idle</span>',
                '</div>',
                '<div class="monitor-actions">',
                    '<button onclick="requestMonitor.clearCache()">Limpar Cache</button>',
                    '<button onclick="requestMonitor.showStats()">Detalhes</button>',
                '</div>',
            '</div>'
        ].join('');
        
        // CSS moved to static/css/style.css
        document.body.appendChild(monitor);
        
        this.monitor = monitor;
    }
    
    /**
     * Configurar atalho de teclado (Ctrl+Shift+M)
     */
    setupKeyboardShortcut() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'M') {
                e.preventDefault();
                this.toggle();
            }
        });
        
        console.log('💡 Pressione Ctrl+Shift+M para abrir o Request Monitor');
    }
    
    /**
     * Mostrar monitor
     */
    show() {
        this.monitor.style.display = 'block';
        this.isVisible = true;
        this.startUpdating();
    }
    
    /**
     * Esconder monitor
     */
    hide() {
        this.monitor.style.display = 'none';
        this.isVisible = false;
        this.stopUpdating();
    }
    
    /**
     * Alternar visibilidade
     */
    toggle() {
        if (this.isVisible) {
            this.hide();
        } else {
            this.show();
        }
    }
    
    /**
     * Iniciar atualizações automáticas
     */
    startUpdating() {
        this.updateStats();
        this.updateInterval = setInterval(() => {
            this.updateStats();
        }, 1000);
    }
    
    /**
     * Parar atualizações automáticas
     */
    stopUpdating() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
    
    /**
     * Atualizar estatísticas
     */
    updateStats() {
        if (!window.requestManager) return;
        
        const stats = window.requestManager.getStats();
        
        // Atualizar elementos
        document.getElementById('cache-size').textContent = stats.cacheSize;
        document.getElementById('queue-size').textContent = stats.queueSize;
        document.getElementById('current-requests').textContent = stats.currentRequests;
        document.getElementById('max-requests').textContent = stats.maxRequests;
        
        // Status de processamento
        const statusEl = document.getElementById('processing-status');
        if (stats.isProcessing) {
            statusEl.textContent = 'Processando';
            statusEl.className = 'processing';
        } else {
            statusEl.textContent = 'Idle';
            statusEl.className = 'idle';
        }
        
        // Cores de alerta para requisições
        const requestsEl = document.getElementById('current-requests');
        requestsEl.className = '';
        
        const percentage = stats.currentRequests / stats.maxRequests;
        if (percentage >= 0.9) {
            requestsEl.className = 'danger';
        } else if (percentage >= 0.7) {
            requestsEl.className = 'warning';
        }
        
        // Alerta se estiver próximo do limite
        if (percentage >= 0.9 && !this.alertShown) {
            this.showAlert('⚠️ Próximo do limite de requisições!');
            this.alertShown = true;
        } else if (percentage < 0.7) {
            this.alertShown = false;
        }
    }
    
    /**
     * Limpar cache
     */
    clearCache() {
        if (window.requestManager) {
            const oldSize = window.requestManager.cache.size;
            window.requestManager.cache.clear();
            this.showAlert(`🗑️ Cache limpo (${oldSize} itens removidos)`);
        }
    }
    
    /**
     * Mostrar estatísticas detalhadas
     */
    showStats() {
        if (!window.requestManager) return;
        
        const stats = window.requestManager.getStats();
        const details = `
📊 Estatísticas Detalhadas:

Cache: ${stats.cacheSize} itens
Fila: ${stats.queueSize} requisições
Requisições atuais: ${stats.currentRequests}/${stats.maxRequests}
Status: ${stats.isProcessing ? 'Processando' : 'Idle'}

Configurações:
- Max req/min: ${window.requestManager.config.maxRequestsPerMinute}
- Cache expira em: ${window.requestManager.config.cacheExpiration / 1000}s
- Debounce: ${window.requestManager.config.debounceDelay}ms
- Max tentativas: ${window.requestManager.config.retryAttempts}
        `.trim();
        
        alert(details);
    }
    
    /**
     * Mostrar alerta temporário
     */
    showAlert(message) {
        console.warn(message);
        
        // Mostrar toast se disponível
        if (typeof showToast === 'function') {
            showToast(message, 'warning');
        }
    }
}

// Inicializar monitor quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.requestMonitor = new RequestMonitor();
});

console.log('🔍 Request Monitor loaded');
