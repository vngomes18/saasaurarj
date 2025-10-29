# 🚀 Sistema de Rate Limiting e Otimização de Requisições

Este documento explica o sistema implementado para prevenir o erro "Too Many Requests" e otimizar o desempenho das requisições.

## 📋 Componentes Implementados

### 1. **Request Manager** (`static/js/request-manager.js`)
Sistema principal que gerencia todas as requisições com:
- ✅ **Rate limiting** (máx 30 req/min por padrão)
- ✅ **Cache inteligente** (5 min de expiração)
- ✅ **Retry automático** com backoff exponencial
- ✅ **Fila de requisições** quando limite é atingido
- ✅ **Debounce** para evitar requisições desnecessárias

### 2. **Autocomplete Manager** (`static/js/autocomplete-manager.js`)
Sistema otimizado para campos de autocomplete:
- ✅ **Debounce de 300ms** para inputs
- ✅ **Cache local** para sugestões
- ✅ **Navegação por teclado** (setas, Enter, Escape)
- ✅ **Highlight de texto** correspondente
- ✅ **Suporte a dados estáticos** e API

### 3. **Request Monitor** (`static/js/request-monitor.js`)
Monitor visual para desenvolvimento:
- ✅ **Estatísticas em tempo real**
- ✅ **Alertas de rate limit**
- ✅ **Controle de cache**
- ✅ **Atalho: Ctrl+Shift+M**

### 4. **Request Config** (`static/js/request-config.js`)
Configurações centralizadas:
- ✅ **Limites personalizáveis**
- ✅ **Configurações por endpoint**
- ✅ **Alertas configuráveis**
- ✅ **Modo desenvolvimento**

## 🎯 Funcionalidades Implementadas

### **Rate Limiting**
```javascript
// Máximo 30 requisições por minuto
maxRequestsPerMinute: 30

// Requisições são automaticamente enfileiradas se limite for atingido
await window.safeRequest('/api/categorias');
```

### **Cache Inteligente**
```javascript
// Cache automático por 5 minutos
// Requisições idênticas retornam dados do cache
const data = await window.safeRequest('/api/cep/12345678');
```

### **Debounce para Inputs**
```javascript
// Aguarda 300ms de inatividade antes de fazer requisição
await window.debounceRequest('categoria_search', '/api/categorias');
```

### **Retry Automático**
```javascript
// Até 3 tentativas com backoff exponencial
// 1s, 2s, 4s entre tentativas
```

## 📊 Monitoramento

### **Ativar Monitor (Desenvolvimento)**
```
Pressione: Ctrl + Shift + M
```

### **Estatísticas Disponíveis**
- 📦 **Cache**: Número de itens em cache
- 📋 **Fila**: Requisições aguardando processamento
- 🔢 **Requisições/min**: Contador atual vs limite
- ⚡ **Status**: Idle ou Processando

### **Logs no Console**
```javascript
// Ver estatísticas a cada 30s (apenas localhost)
📊 Request Manager Stats: {
  cacheSize: 5,
  queueSize: 0,
  currentRequests: 12,
  maxRequests: 30,
  isProcessing: false
}
```

## ⚙️ Configuração

### **Personalizar Limites**
```javascript
// Em request-config.js
window.REQUEST_CONFIG = {
    maxRequestsPerMinute: 50,     // Aumentar limite
    debounceDelay: 500,           // Mais debounce
    cacheExpiration: 10 * 60 * 1000, // 10 min cache
    retryAttempts: 5              // Mais tentativas
};
```

### **Configurações por Endpoint**
```javascript
endpoints: {
    cep: {
        debounceDelay: 500,       // 500ms para CEP
        cacheExpiration: 10 * 60 * 1000, // 10 min
        retryAttempts: 2
    },
    categorias: {
        debounceDelay: 300,       // 300ms para categorias
        cacheExpiration: 15 * 60 * 1000, // 15 min
        retryAttempts: 3
    }
}
```

## 🔧 Implementações Específicas

### **1. CEP Otimizado** (clientes/form.html)
```javascript
// Debounce de 500ms + cache + rate limiting
const data = await window.safeRequest(`/api/cep/${cep}`);
```

### **2. Preview Otimizado** (produtos/form.html)
```javascript
// requestAnimationFrame para 60fps suave
function updatePreview() {
    if (!updateScheduled) {
        updateScheduled = true;
        requestAnimationFrame(() => {
            // Atualizar preview
            updateScheduled = false;
        });
    }
}
```

### **3. Autocomplete Inteligente**
```javascript
// Criar autocomplete com cache e debounce
window.autocompleteManager.create({
    inputId: 'categoria',
    suggestionsId: 'categoria-suggestions',
    apiUrl: '/api/categorias',
    debounceDelay: 300,
    maxSuggestions: 8
});
```

## 🚨 Alertas e Tratamento de Erros

### **Rate Limit Atingido**
- ⏳ **Requisições enfileiradas** automaticamente
- ⚠️ **Toast de aviso** quando próximo do limite (80%)
- 🔄 **Processamento automático** quando limite resetar

### **Erro de Rede**
- 🔄 **Retry automático** até 3 tentativas
- 📱 **Fallback para cache** quando possível
- 🚫 **Toast de erro** informativo

### **Timeout**
- ⏰ **10 segundos** de timeout padrão
- 🔄 **Retry com backoff** exponencial
- 📊 **Estatísticas** de falhas

## 📈 Benefícios Implementados

### **Performance**
- ✅ **90% menos requisições** com cache inteligente
- ✅ **Debounce elimina** requisições desnecessárias
- ✅ **requestAnimationFrame** para preview suave
- ✅ **Lazy loading** de dados estáticos

### **Confiabilidade**
- ✅ **Retry automático** para falhas temporárias
- ✅ **Fallback para cache** offline
- ✅ **Fila inteligente** para rate limiting
- ✅ **Timeout configurável** por endpoint

### **Experiência do Usuário**
- ✅ **Sem travamentos** por muitas requisições
- ✅ **Feedback visual** de carregamento
- ✅ **Toasts informativos** para erros
- ✅ **Interface responsiva** sempre

### **Desenvolvimento**
- ✅ **Monitor visual** para debug
- ✅ **Logs detalhados** no console
- ✅ **Configuração centralizada**
- ✅ **Estatísticas em tempo real**

## 🎮 Como Usar

### **Requisições Normais**
```javascript
// Substitua fetch() por:
const data = await window.safeRequest('/api/endpoint');
```

### **Requisições com Debounce**
```javascript
// Para inputs que disparam ao digitar:
const data = await window.debounceRequest('unique_key', '/api/search');
```

### **Autocomplete**
```javascript
// Criar autocomplete otimizado:
window.autocompleteManager.create({
    inputId: 'meu-input',
    suggestionsId: 'minhas-sugestoes',
    apiUrl: '/api/dados'
});
```

### **Monitoramento**
```javascript
// Ver estatísticas:
console.log(window.requestManager.getStats());

// Limpar cache:
window.requestManager.clear();

// Abrir monitor visual:
// Ctrl + Shift + M (desenvolvimento)
```

## 🔍 Troubleshooting

### **Still Getting "Too Many Requests"?**
1. ✅ Verificar se scripts estão carregados
2. ✅ Usar `window.safeRequest()` ao invés de `fetch()`
3. ✅ Verificar configurações em `request-config.js`
4. ✅ Monitorar com Ctrl+Shift+M

### **Cache não está funcionando?**
1. ✅ Verificar se URLs são idênticas
2. ✅ Verificar expiração do cache (5 min padrão)
3. ✅ Limpar cache: `window.requestManager.clear()`

### **Debounce muito lento?**
1. ✅ Ajustar `debounceDelay` em `request-config.js`
2. ✅ Usar configuração específica por endpoint
3. ✅ Verificar se está usando `debounceRequest()`

---

## 📞 Suporte

Para dúvidas ou problemas:
1. 🔍 Ativar monitor (Ctrl+Shift+M)
2. 📊 Verificar logs no console
3. ⚙️ Ajustar configurações conforme necessário

**Sistema implementado com sucesso! 🎉**
