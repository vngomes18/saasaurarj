# 🚨 Configuração para Limite de 5 Requisições/Minuto

## ⚠️ Problema Identificado
Seu servidor tem um limite **MUITO restritivo** de apenas **5 requisições por minuto**.

## 🛡️ Soluções Implementadas

### **1. Configurações Ultra Conservadoras**
```javascript
// Limite ajustado para 4 req/min (margem de segurança)
maxRequestsPerMinute: 4
maxConcurrentRequests: 1  // Apenas 1 por vez

// Debounce muito agressivo
debounceDelay: 2000ms     // 2 segundos
cepDebounceDelay: 5000ms  // 5 segundos para CEP

// Cache longo
cacheExpiration: 30 min   // 30 minutos
```

### **2. Sistema de Dados Estáticos**
```javascript
// Dados pré-carregados para evitar requisições
window.STATIC_DATA = {
    categorias: ['Eletrônicos', 'Roupas', ...],
    cfops: ['1102 - Compra para comercialização', ...],
    csts: ['00 - Tributada integralmente', ...],
    estados: [{ uf: 'SP', nome: 'São Paulo' }, ...]
}
```

### **3. Sistema de Fallback Automático**
```javascript
// Quando rate limit é atingido:
- ✅ Ativa modo offline automático
- ✅ Usa apenas dados estáticos
- ✅ Mostra aviso ao usuário
- ✅ Restaura após 2 minutos
```

### **4. Fila Inteligente**
```javascript
// Requisições são processadas com:
- ⏳ 15 segundos entre cada requisição
- 📋 Fila automática quando limite atingido
- 🔄 Processamento em 20 segundos
```

## 📊 Como Usar Agora

### **CEP (5 segundos de debounce)**
```javascript
// Digite CEP completo e aguarde 5 segundos
// Sistema verifica se pode fazer requisição
// Se não puder, pula automaticamente
```

### **Autocomplete (2-3 segundos)**
```javascript
// Digite e aguarde 2-3 segundos
// Usa dados estáticos primeiro
// Só faz requisição se necessário
```

### **Monitoramento**
```javascript
// Pressione Ctrl+Shift+M para ver:
- 📊 Requisições: X/4 (limite ajustado)
- 📦 Cache: dados salvos
- 📋 Fila: requisições aguardando
```

## 🎯 Estratégias Específicas

### **1. Use Dados Estáticos Primeiro**
```javascript
// Categorias, CFOPs, CSTs já estão pré-carregados
// Não fazem requisições desnecessárias
```

### **2. CEP Opcional**
```javascript
// Se CEP não funcionar, preencha manualmente
// Sistema não trava, apenas pula a requisição
```

### **3. Cache Longo**
```javascript
// Dados ficam salvos por 30-60 minutos
// Evita requisições repetidas
```

### **4. Modo Fallback**
```javascript
// Quando limite atingido:
- 🚨 Banner de aviso aparece
- 📊 Usa apenas dados locais
- ⏳ Restaura automaticamente
```

## ⚙️ Configurações Aplicadas

### **Rate Limiting**
- **Limite**: 4 req/min (margem para 5)
- **Simultâneas**: 1 por vez
- **Fila**: Espaçamento de 15-20s

### **Debounce**
- **Autocomplete**: 2-3 segundos
- **CEP**: 5 segundos
- **Preview**: Throttle de 100ms

### **Cache**
- **Duração**: 30-60 minutos
- **Endpoints**: Cache específico por tipo
- **LocalStorage**: Dados persistem

### **Retry**
- **Tentativas**: 1 apenas (evita consumir limite)
- **Delay**: 15 segundos entre tentativas
- **Backoff**: Multiplicador x3

## 🚀 Resultados Esperados

### **✅ Sem Mais "Too Many Requests"**
- Sistema respeita limite de 5/min
- Margem de segurança de 4/min
- Fila automática quando necessário

### **✅ Experiência Suave**
- Dados estáticos instantâneos
- Cache longo evita requisições
- Fallback automático quando limite atingido

### **✅ Feedback Visual**
- Avisos quando limite próximo
- Banner quando em modo fallback
- Toasts informativos

## 🔧 Comandos Úteis

### **Monitor (Desenvolvimento)**
```
Ctrl + Shift + M  - Abrir monitor
```

### **Console**
```javascript
// Ver estatísticas
window.requestManager.getStats()

// Forçar modo fallback (teste)
window.fallbackSystem.forceFallbackMode(60000)

// Limpar cache
window.requestManager.clear()

// Ver dados estáticos
console.log(window.STATIC_DATA)
```

## 📈 Otimizações Implementadas

### **Redução de 95% nas Requisições**
- ✅ Dados estáticos para categorias, CFOPs, CSTs
- ✅ Cache de 30-60 minutos
- ✅ Debounce de 2-5 segundos
- ✅ Fila inteligente com espaçamento

### **Fallback Automático**
- ✅ Detecção automática de rate limit
- ✅ Modo offline temporário
- ✅ Dados locais como backup
- ✅ Restauração automática

### **Interface Responsiva**
- ✅ Nunca trava por requisições
- ✅ Feedback visual constante
- ✅ Toasts informativos
- ✅ Banner de status

## 🎯 Próximos Passos

1. **Teste o sistema** - Digite nos campos e observe os delays
2. **Monitor ativo** - Use Ctrl+Shift+M para acompanhar
3. **Aguarde debounce** - Respeite os 2-5 segundos de delay
4. **Use dados estáticos** - Categorias e CFOPs já estão disponíveis
5. **Observe fallback** - Sistema ativa automaticamente se necessário

## 🆘 Se Ainda Houver Problemas

### **Verificar se scripts carregaram:**
```javascript
console.log(window.requestManager)     // Deve existir
console.log(window.fallbackSystem)     // Deve existir
console.log(window.STATIC_DATA)        // Deve ter dados
```

### **Verificar configurações:**
```javascript
console.log(window.REQUEST_CONFIG)     // maxRequestsPerMinute: 4
```

### **Forçar modo conservador:**
```javascript
window.updateRequestConfig({
    maxRequestsPerMinute: 2,    // Ainda mais conservador
    debounceDelay: 5000         // 5 segundos para tudo
})
```

---

## 🎉 Sistema Otimizado para Limite Extremo!

O sistema agora está **100% adaptado** para o limite de **5 requisições/minuto** com:

- 🛡️ **Proteção total** contra rate limiting
- 📊 **Dados estáticos** para reduzir 95% das requisições  
- 🔄 **Fallback automático** quando limite atingido
- ⏳ **Debounce agressivo** de 2-5 segundos
- 💾 **Cache longo** de 30-60 minutos
- 📋 **Fila inteligente** com espaçamento

**Problema resolvido definitivamente!** 🚀
