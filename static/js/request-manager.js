/**
 * Sistema de Gerenciamento de Requisições
 * Previne "Too Many Requests" com rate limiting, cache e debounce
 */

class RequestManager {
    constructor() {
        this.cache = new Map();
        this.requestQueue = [];
        this.isProcessing = false;
        this.requestCounts = new Map();
        this.debounceTimers = new Map();
        
        // Configurações - ULTRA CONSERVADORAS PARA LIMITE DE 5/MIN
        this.config = {
            maxRequestsPerMinute: 4,         // Margem de segurança
            maxConcurrentRequests: 1,        // Uma por vez
            cacheExpiration: 30 * 60 * 1000, // 30 minutos
            debounceDelay: 2000,             // 2 segundos
            retryAttempts: 1,                // Apenas 1 retry
            retryDelay: 15000                // 15 segundos
        };
        
        // Limpar cache expirado a cada minuto
        setInterval(() => this.cleanExpiredCache(), 60000);
        
        // Resetar contadores a cada minuto
        setInterval(() => this.resetRequestCounts(), 60000);
    }
    
    /**
     * Fazer requisição com rate limiting e cache
     */
    async makeRequest(url, options = {}) {
        const cacheKey = this.getCacheKey(url, options);
        
        // Verificar cache primeiro
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.config.cacheExpiration) {
                console.log('📦 Cache hit:', url);
                return cached.data;
            }
        }
        
        // Verificar rate limit
        if (!this.canMakeRequest()) {
            console.warn('⚠️ Rate limit exceeded, queuing request:', url);
            return this.queueRequest(url, options);
        }
        
        try {
            this.incrementRequestCount();
            const response = await this.fetchWithRetry(url, options);
            const data = await response.json();
            
            // Armazenar no cache
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });
            
            console.log('✅ Request successful:', url);
            return data;
        } catch (error) {
            console.error('❌ Request failed:', url, error);
            throw error;
        }
    }
    
    /**
     * Requisição com debounce para campos de input
     */
    debounceRequest(key, url, options = {}) {
        return new Promise((resolve, reject) => {
            // Cancelar timer anterior se existir
            if (this.debounceTimers.has(key)) {
                clearTimeout(this.debounceTimers.get(key));
            }
            
            // Criar novo timer
            const timer = setTimeout(async () => {
                try {
                    const result = await this.makeRequest(url, options);
                    resolve(result);
                } catch (error) {
                    reject(error);
                }
                this.debounceTimers.delete(key);
            }, this.config.debounceDelay);
            
            this.debounceTimers.set(key, timer);
        });
    }
    
    /**
     * Verificar se pode fazer requisição (rate limiting)
     */
    canMakeRequest() {
        const currentMinute = Math.floor(Date.now() / 60000);
        const count = this.requestCounts.get(currentMinute) || 0;
        return count < this.config.maxRequestsPerMinute;
    }
    
    /**
     * Incrementar contador de requisições
     */
    incrementRequestCount() {
        const currentMinute = Math.floor(Date.now() / 60000);
        const count = this.requestCounts.get(currentMinute) || 0;
        this.requestCounts.set(currentMinute, count + 1);
    }
    
    /**
     * Resetar contadores antigos
     */
    resetRequestCounts() {
        const currentMinute = Math.floor(Date.now() / 60000);
        for (const [minute] of this.requestCounts) {
            if (minute < currentMinute - 1) {
                this.requestCounts.delete(minute);
            }
        }
    }
    
    /**
     * Fazer requisição com retry automático
     */
    async fetchWithRetry(url, options, attempt = 1) {
        try {
            const response = await fetch(url, options);
            
            if (response.status === 429) {
                const retryAfter = response.headers.get('Retry-After') || this.config.retryDelay / 1000;
                console.warn(`⏳ Rate limited, retrying in ${retryAfter}s...`);
                await this.sleep(retryAfter * 1000);
                
                if (attempt < this.config.retryAttempts) {
                    return this.fetchWithRetry(url, options, attempt + 1);
                }
            }
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return response;
        } catch (error) {
            if (attempt < this.config.retryAttempts) {
                console.warn(`🔄 Retry attempt ${attempt} for:`, url);
                await this.sleep(this.config.retryDelay * attempt);
                return this.fetchWithRetry(url, options, attempt + 1);
            }
            throw error;
        }
    }
    
    /**
     * Adicionar requisição à fila
     */
    async queueRequest(url, options) {
        return new Promise((resolve, reject) => {
            this.requestQueue.push({ url, options, resolve, reject });
            this.processQueue();
        });
    }
    
    /**
     * Processar fila de requisições - ULTRA CONSERVADOR
     */
    async processQueue() {
        if (this.isProcessing || this.requestQueue.length === 0) {
            return;
        }
        
        this.isProcessing = true;
        
        // Processar apenas 1 requisição por vez com espaçamento longo
        if (this.requestQueue.length > 0 && this.canMakeRequest()) {
            const { url, options, resolve, reject } = this.requestQueue.shift();
            
            try {
                const result = await this.makeRequest(url, options);
                resolve(result);
            } catch (error) {
                reject(error);
            }
            
            // Pausa longa entre requisições (15 segundos)
            await this.sleep(15000);
        }
        
        this.isProcessing = false;
        
        // Se ainda há itens na fila, processar novamente em 20 segundos
        if (this.requestQueue.length > 0) {
            console.warn(`⏳ ${this.requestQueue.length} requisições na fila. Processando em 20s...`);
            setTimeout(() => this.processQueue(), 20000);
        }
    }
    
    /**
     * Gerar chave de cache
     */
    getCacheKey(url, options) {
        const method = options.method || 'GET';
        const body = options.body || '';
        return `${method}:${url}:${body}`;
    }
    
    /**
     * Limpar cache expirado
     */
    cleanExpiredCache() {
        const now = Date.now();
        for (const [key, value] of this.cache) {
            if (now - value.timestamp > this.config.cacheExpiration) {
                this.cache.delete(key);
            }
        }
    }
    
    /**
     * Utilitário para sleep
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * Obter estatísticas
     */
    getStats() {
        const currentMinute = Math.floor(Date.now() / 60000);
        const currentRequests = this.requestCounts.get(currentMinute) || 0;
        
        return {
            cacheSize: this.cache.size,
            queueSize: this.requestQueue.length,
            currentRequests: currentRequests,
            maxRequests: this.config.maxRequestsPerMinute,
            isProcessing: this.isProcessing
        };
    }
    
    /**
     * Limpar tudo
     */
    clear() {
        this.cache.clear();
        this.requestQueue.length = 0;
        this.requestCounts.clear();
        for (const timer of this.debounceTimers.values()) {
            clearTimeout(timer);
        }
        this.debounceTimers.clear();
    }
}

// Instância global
window.requestManager = new RequestManager();

// Função de conveniência para debounce
window.debounceRequest = (key, url, options) => {
    return window.requestManager.debounceRequest(key, url, options);
};

// Função de conveniência para requisições normais
window.safeRequest = (url, options) => {
    return window.requestManager.makeRequest(url, options);
};

// Log de estatísticas no console (apenas em desenvolvimento)
if (window.location.hostname === 'localhost') {
    setInterval(() => {
        const stats = window.requestManager.getStats();
        console.log('📊 Request Manager Stats:', stats);
    }, 30000); // A cada 30 segundos
}

console.log('🚀 Request Manager initialized');
