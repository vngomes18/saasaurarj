/**
 * Sistema de Autocomplete Otimizado
 * Previne requisições excessivas com debounce e cache
 */

class AutocompleteManager {
    constructor() {
        this.instances = new Map();
        this.globalCache = new Map();
    }
    
    /**
     * Criar instância de autocomplete
     */
    create(config) {
        const {
            inputId,
            suggestionsId,
            apiUrl,
            minChars = 2,
            debounceDelay = 300,
            maxSuggestions = 10,
            onSelect = null,
            onError = null,
            staticData = []
        } = config;
        
        const input = document.getElementById(inputId);
        const suggestionsContainer = document.getElementById(suggestionsId);
        
        if (!input || !suggestionsContainer) {
            console.error('Autocomplete: Input ou container de sugestões não encontrado');
            return;
        }
        
        const instance = {
            input,
            suggestionsContainer,
            apiUrl,
            minChars,
            debounceDelay,
            maxSuggestions,
            onSelect,
            onError,
            staticData,
            isVisible: false,
            selectedIndex: -1,
            lastQuery: '',
            cache: new Map()
        };
        
        this.instances.set(inputId, instance);
        this.setupEventListeners(instance);
        
        console.log(`✅ Autocomplete criado para: ${inputId}`);
        return instance;
    }
    
    /**
     * Configurar event listeners
     */
    setupEventListeners(instance) {
        const { input, suggestionsContainer } = instance;
        
        // Input com debounce
        input.addEventListener('input', (e) => {
            this.handleInput(instance, e.target.value);
        });
        
        // Focus - mostrar sugestões se houver valor
        input.addEventListener('focus', () => {
            if (input.value.trim()) {
                this.handleInput(instance, input.value);
            }
        });
        
        // Blur - esconder sugestões (com delay para permitir clique)
        input.addEventListener('blur', () => {
            setTimeout(() => {
                this.hideSuggestions(instance);
            }, 150);
        });
        
        // Navegação por teclado
        input.addEventListener('keydown', (e) => {
            this.handleKeydown(instance, e);
        });
        
        // Clique fora para esconder
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !suggestionsContainer.contains(e.target)) {
                this.hideSuggestions(instance);
            }
        });
    }
    
    /**
     * Lidar com input do usuário
     */
    async handleInput(instance, query) {
        query = query.trim();
        
        // Não fazer nada se a query for muito pequena
        if (query.length < instance.minChars) {
            this.hideSuggestions(instance);
            return;
        }
        
        // Não fazer nada se a query não mudou
        if (query === instance.lastQuery) {
            return;
        }
        
        instance.lastQuery = query;
        
        try {
            // Buscar sugestões (com debounce se for API)
            let suggestions;
            if (instance.apiUrl) {
                suggestions = await this.fetchSuggestionsWithDebounce(instance, query);
            } else {
                suggestions = this.filterStaticData(instance, query);
            }
            
            this.showSuggestions(instance, suggestions);
        } catch (error) {
            console.error('Erro ao buscar sugestões:', error);
            if (instance.onError) {
                instance.onError(error);
            }
        }
    }
    
    /**
     * Buscar sugestões com debounce
     */
    async fetchSuggestionsWithDebounce(instance, query) {
        const cacheKey = `${instance.apiUrl}:${query.toLowerCase()}`;
        
        // Verificar cache primeiro
        if (instance.cache.has(cacheKey)) {
            const cached = instance.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < 300000) { // 5 minutos
                return cached.data;
            }
        }
        
        // Usar debounce do RequestManager
        const debounceKey = `autocomplete_${instance.input.id}_${query}`;
        const data = await window.debounceRequest(debounceKey, instance.apiUrl);
        
        // Filtrar e limitar resultados
        let suggestions = Array.isArray(data) ? data : [];
        suggestions = suggestions
            .filter(item => {
                const text = typeof item === 'string' ? item : item.name || item.text || '';
                return text.toLowerCase().includes(query.toLowerCase());
            })
            .slice(0, instance.maxSuggestions);
        
        // Armazenar no cache
        instance.cache.set(cacheKey, {
            data: suggestions,
            timestamp: Date.now()
        });
        
        return suggestions;
    }
    
    /**
     * Filtrar dados estáticos
     */
    filterStaticData(instance, query) {
        return instance.staticData
            .filter(item => {
                const text = typeof item === 'string' ? item : item.name || item.text || '';
                return text.toLowerCase().includes(query.toLowerCase());
            })
            .slice(0, instance.maxSuggestions);
    }
    
    /**
     * Mostrar sugestões
     */
    showSuggestions(instance, suggestions) {
        const { suggestionsContainer } = instance;
        
        // Limpar sugestões anteriores
        suggestionsContainer.innerHTML = '';
        
        if (suggestions.length === 0) {
            this.hideSuggestions(instance);
            return;
        }
        
        // Criar elementos de sugestão
        suggestions.forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            
            const text = typeof suggestion === 'string' ? suggestion : suggestion.name || suggestion.text || '';
            item.textContent = text;
            item.dataset.index = index;
            
            // Destacar texto correspondente
            const query = instance.lastQuery.toLowerCase();
            const highlightedText = text.replace(
                new RegExp(`(${query})`, 'gi'),
                '<strong>$1</strong>'
            );
            item.innerHTML = highlightedText;
            
            // Click handler
            item.addEventListener('click', () => {
                this.selectSuggestion(instance, suggestion, index);
            });
            
            // Hover handler
            item.addEventListener('mouseenter', () => {
                this.setSelectedIndex(instance, index);
            });
            
            suggestionsContainer.appendChild(item);
        });
        
        // Mostrar container
        suggestionsContainer.style.display = 'block';
        instance.isVisible = true;
        instance.selectedIndex = -1;
    }
    
    /**
     * Esconder sugestões
     */
    hideSuggestions(instance) {
        instance.suggestionsContainer.style.display = 'none';
        instance.isVisible = false;
        instance.selectedIndex = -1;
    }
    
    /**
     * Lidar com teclas
     */
    handleKeydown(instance, e) {
        if (!instance.isVisible) return;
        
        const items = instance.suggestionsContainer.querySelectorAll('.autocomplete-item');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.setSelectedIndex(instance, Math.min(instance.selectedIndex + 1, items.length - 1));
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.setSelectedIndex(instance, Math.max(instance.selectedIndex - 1, -1));
                break;
                
            case 'Enter':
                e.preventDefault();
                if (instance.selectedIndex >= 0) {
                    const selectedItem = items[instance.selectedIndex];
                    const suggestion = selectedItem.textContent;
                    this.selectSuggestion(instance, suggestion, instance.selectedIndex);
                }
                break;
                
            case 'Escape':
                this.hideSuggestions(instance);
                break;
        }
    }
    
    /**
     * Definir índice selecionado
     */
    setSelectedIndex(instance, index) {
        const items = instance.suggestionsContainer.querySelectorAll('.autocomplete-item');
        
        // Remover seleção anterior
        items.forEach(item => item.classList.remove('selected'));
        
        // Definir nova seleção
        instance.selectedIndex = index;
        if (index >= 0 && index < items.length) {
            items[index].classList.add('selected');
        }
    }
    
    /**
     * Selecionar sugestão
     */
    selectSuggestion(instance, suggestion, index) {
        const text = typeof suggestion === 'string' ? suggestion : suggestion.name || suggestion.text || '';
        
        instance.input.value = text;
        this.hideSuggestions(instance);
        
        if (instance.onSelect) {
            instance.onSelect(suggestion, index);
        }
        
        // Trigger change event
        instance.input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    
    /**
     * Atualizar dados estáticos
     */
    updateStaticData(inputId, data) {
        const instance = this.instances.get(inputId);
        if (instance) {
            instance.staticData = data;
        }
    }
    
    /**
     * Limpar cache de uma instância
     */
    clearCache(inputId) {
        const instance = this.instances.get(inputId);
        if (instance) {
            instance.cache.clear();
        }
    }
    
    /**
     * Destruir instância
     */
    destroy(inputId) {
        const instance = this.instances.get(inputId);
        if (instance) {
            this.hideSuggestions(instance);
            this.instances.delete(inputId);
        }
    }
}

// Instância global
window.autocompleteManager = new AutocompleteManager();

// CSS moved to static/css/style.css

console.log('🚀 Autocomplete Manager initialized');
