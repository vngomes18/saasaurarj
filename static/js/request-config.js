/**
 * Configuração do Sistema de Requisições
 * Personalize os limites e comportamentos aqui
 */

// Configurações globais do sistema de requisições
window.REQUEST_CONFIG = {
    // Rate Limiting - AJUSTADO PARA LIMITE MUITO RESTRITIVO
    maxRequestsPerMinute: 4,         // Máximo 4 req/min (margem de segurança para limite de 5)
    maxConcurrentRequests: 1,        // Apenas 1 requisição simultânea
    
    // Cache - AGRESSIVO PARA LIMITE RESTRITIVO
    cacheExpiration: 30 * 60 * 1000, // 30 minutos em ms (cache longo)
    enableCache: true,                // Habilitar cache
    
    // Debounce/Throttle - MUITO AGRESSIVO
    debounceDelay: 2000,             // 2 segundos para autocomplete
    cepDebounceDelay: 3000,          // 3 segundos para CEP
    previewThrottleDelay: 100,       // Throttle mais lento para preview
    
    // Retry - CONSERVADOR PARA LIMITE RESTRITIVO
    retryAttempts: 1,                // Apenas 1 tentativa (evitar consumir limite)
    retryDelay: 15000,               // 15 segundos entre tentativas
    retryBackoffMultiplier: 3,       // Backoff mais agressivo
    
    // Timeouts
    requestTimeout: 15000,           // 15 segundos timeout (mais tempo)
    
    // Desenvolvimento
    enableMonitor: true,             // Habilitar monitor de requisições
    enableLogs: true,                // Habilitar logs detalhados
    enableStats: true,               // Habilitar coleta de estatísticas
    
    // Endpoints específicos - CONFIGURAÇÕES ULTRA CONSERVADORAS
    endpoints: {
        cep: {
            debounceDelay: 5000,             // 5 segundos para CEP
            cacheExpiration: 60 * 60 * 1000, // 1 hora para CEP
            retryAttempts: 0                 // Sem retry para CEP
        },
        categorias: {
            debounceDelay: 3000,             // 3 segundos para categorias
            cacheExpiration: 60 * 60 * 1000, // 1 hora para categorias
            retryAttempts: 0                 // Sem retry para categorias
        },
        fornecedores: {
            debounceDelay: 3000,             // 3 segundos para fornecedores
            cacheExpiration: 60 * 60 * 1000, // 1 hora para fornecedores
            retryAttempts: 0                 // Sem retry para fornecedores
        }
    },
    
    // Alertas - MUITO CONSERVADOR
    alerts: {
        showRateLimitWarning: true,   // Mostrar aviso quando próximo do limite
        warningThreshold: 0.5,        // 50% do limite para mostrar aviso (2/4 req)
        showErrorToasts: true,        // Mostrar toasts de erro
        showSuccessToasts: false      // Mostrar toasts de sucesso
    }
};

// Aplicar configurações quando o RequestManager estiver disponível
document.addEventListener('DOMContentLoaded', () => {
    // Aguardar RequestManager estar disponível
    const checkRequestManager = () => {
        if (window.requestManager) {
            // Aplicar configurações
            Object.assign(window.requestManager.config, window.REQUEST_CONFIG);
            
            console.log('⚙️ Request Config aplicado:', window.REQUEST_CONFIG);
            
            // Configurar alertas personalizados
            setupCustomAlerts();
        } else {
            // Tentar novamente em 100ms
            setTimeout(checkRequestManager, 100);
        }
    };
    
    checkRequestManager();
});

/**
 * Configurar alertas personalizados
 */
function setupCustomAlerts() {
    if (!window.REQUEST_CONFIG.alerts.showRateLimitWarning) return;
    
    // Monitorar rate limit
    setInterval(() => {
        if (!window.requestManager) return;
        
        const stats = window.requestManager.getStats();
        const percentage = stats.currentRequests / stats.maxRequests;
        
        if (percentage >= window.REQUEST_CONFIG.alerts.warningThreshold) {
            if (!window.rateLimitWarningShown) {
                showRateLimitWarning(stats);
                window.rateLimitWarningShown = true;
            }
        } else {
            window.rateLimitWarningShown = false;
        }
    }, 5000); // Verificar a cada 5 segundos
}

/**
 * Mostrar aviso de rate limit
 */
function showRateLimitWarning(stats) {
    const message = `⚠️ Muitas requisições: ${stats.currentRequests}/${stats.maxRequests}`;
    
    console.warn(message);
    
    if (window.REQUEST_CONFIG.alerts.showErrorToasts && typeof showToast === 'function') {
        showToast(message, 'warning');
    }
}

/**
 * Função utilitária para obter configuração de endpoint
 */
window.getEndpointConfig = function(url) {
    const config = { ...window.REQUEST_CONFIG };
    
    // Verificar se há configuração específica para o endpoint
    for (const [key, endpointConfig] of Object.entries(window.REQUEST_CONFIG.endpoints)) {
        if (url.includes(key)) {
            Object.assign(config, endpointConfig);
            break;
        }
    }
    
    return config;
};

/**
 * Função para atualizar configurações em tempo real
 */
window.updateRequestConfig = function(newConfig) {
    Object.assign(window.REQUEST_CONFIG, newConfig);
    
    if (window.requestManager) {
        Object.assign(window.requestManager.config, newConfig);
        console.log('⚙️ Configuração atualizada:', newConfig);
    }
};

console.log('⚙️ Request Config loaded');
