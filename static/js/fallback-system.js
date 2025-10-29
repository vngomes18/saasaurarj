/**
 * Sistema de Fallback para Limite Muito Restritivo
 * Usa dados estáticos quando rate limit é atingido
 */

class FallbackSystem {
    constructor() {
        this.rateLimitReached = false;
        this.fallbackMode = false;
        this.setupRateLimitDetection();
    }
    
    /**
     * Detectar quando rate limit é atingido
     */
    setupRateLimitDetection() {
        // Interceptar erros 429
        const originalFetch = window.fetch;
        window.fetch = async function(...args) {
            try {
                const response = await originalFetch.apply(this, arguments);
                
                if (response.status === 429) {
                    window.fallbackSystem.handleRateLimit();
                }
                
                return response;
            } catch (error) {
                throw error;
            }
        };
        
        // Monitorar requisições do RequestManager
        if (window.requestManager) {
            const originalMakeRequest = window.requestManager.makeRequest;
            window.requestManager.makeRequest = async function(...args) {
                try {
                    return await originalMakeRequest.apply(this, arguments);
                } catch (error) {
                    if (error.message.includes('429') || error.message.includes('Too Many Requests')) {
                        window.fallbackSystem.handleRateLimit();
                    }
                    throw error;
                }
            };
        }
    }
    
    /**
     * Lidar com rate limit atingido
     */
    handleRateLimit() {
        this.rateLimitReached = true;
        this.fallbackMode = true;
        
        console.warn('🚨 Rate limit atingido! Ativando modo fallback com dados estáticos');
        
        // Mostrar aviso ao usuário
        this.showFallbackNotification();
        
        // Resetar após 2 minutos
        setTimeout(() => {
            this.resetFallbackMode();
        }, 2 * 60 * 1000);
    }
    
    /**
     * Resetar modo fallback
     */
    resetFallbackMode() {
        this.rateLimitReached = false;
        this.fallbackMode = false;
        
        console.log('✅ Modo fallback desativado. Requisições normais restauradas.');
        
        if (typeof showToast === 'function') {
            showToast('✅ Conexão restaurada', 'success');
        }
    }
    
    /**
     * Mostrar notificação de fallback
     */
    showFallbackNotification() {
        const message = '⚠️ Limite de requisições atingido. Usando dados locais temporariamente.';
        
        console.warn(message);
        
        if (typeof showToast === 'function') {
            showToast(message, 'warning');
        }
        
        // Criar banner de aviso
        this.createFallbackBanner();
    }
    
    /**
     * Criar banner de aviso
     */
    createFallbackBanner() {
        // Remover banner existente
        const existingBanner = document.getElementById('fallback-banner');
        if (existingBanner) {
            existingBanner.remove();
        }
        
        const banner = document.createElement('div');
        banner.id = 'fallback-banner';
        banner.innerHTML = `
            <div class="alert alert-warning alert-dismissible fade show m-0" role="alert">
                <strong>⚠️ Modo Offline Temporário:</strong> 
                Usando dados locais devido ao limite de requisições. 
                Conexão será restaurada automaticamente.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Inserir no topo da página
        document.body.insertBefore(banner, document.body.firstChild);
        
        // Remover automaticamente após 10 segundos
        setTimeout(() => {
            if (banner && banner.parentNode) {
                banner.remove();
            }
        }, 10000);
    }
    
    /**
     * Obter dados com fallback
     */
    async getDataWithFallback(type, filter = '') {
        if (this.fallbackMode) {
            console.log(`📊 Usando dados estáticos para: ${type}`);
            return window.getStaticData(type, filter);
        }
        
        try {
            // Tentar requisição normal (com rate limiting)
            const data = await window.safeRequest(`/api/${type}`);
            
            // Salvar nos dados estáticos para futuro uso
            if (Array.isArray(data)) {
                data.forEach(item => {
                    window.addStaticData(type, item);
                });
            }
            
            return data;
        } catch (error) {
            console.warn(`⚠️ Erro na requisição ${type}, usando dados estáticos:`, error);
            
            // Ativar modo fallback temporariamente
            this.fallbackMode = true;
            setTimeout(() => {
                this.fallbackMode = false;
            }, 30000); // 30 segundos
            
            return window.getStaticData(type, filter);
        }
    }
    
    /**
     * Buscar CEP com fallback
     */
    async getCepWithFallback(cep) {
        if (this.fallbackMode) {
            console.log('📊 CEP em modo fallback - não fazendo requisição');
            return null;
        }
        
        try {
            return await window.safeRequest(`/api/cep/${cep}`);
        } catch (error) {
            console.warn('⚠️ Erro na requisição CEP, pulando:', error);
            return null;
        }
    }
    
    /**
     * Verificar se está em modo fallback
     */
    isInFallbackMode() {
        return this.fallbackMode;
    }
    
    /**
     * Forçar modo fallback (para testes)
     */
    forceFallbackMode(duration = 60000) {
        this.fallbackMode = true;
        console.log(`🧪 Modo fallback forçado por ${duration/1000}s`);
        
        setTimeout(() => {
            this.resetFallbackMode();
        }, duration);
    }
}

// Instância global
window.fallbackSystem = new FallbackSystem();

// Funções de conveniência
window.getDataSafe = (type, filter) => {
    return window.fallbackSystem.getDataWithFallback(type, filter);
};

window.getCepSafe = (cep) => {
    return window.fallbackSystem.getCepWithFallback(cep);
};

// Aguardar RequestManager estar disponível
document.addEventListener('DOMContentLoaded', () => {
    const setupFallback = () => {
        if (window.requestManager) {
            window.fallbackSystem.setupRateLimitDetection();
        } else {
            setTimeout(setupFallback, 100);
        }
    };
    setupFallback();
});

console.log('🛡️ Fallback System loaded - Proteção contra rate limiting');
