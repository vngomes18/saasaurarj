// Currency Input Fix - Solução específica para campos de valor
// Este arquivo resolve os problemas de edição nos campos de preço

document.addEventListener('DOMContentLoaded', function() {
    // Função para melhorar a experiência de edição de campos de moeda
    function enhanceCurrencyInputs() {
        const currencyInputs = document.querySelectorAll('.currency-input, input[name="preco"]');
        
        currencyInputs.forEach(input => {
            // Remove event listeners existentes para evitar conflitos
            const newInput = input.cloneNode(true);
            input.parentNode.replaceChild(newInput, input);
            
            // Adiciona funcionalidade de seleção completa ao clicar
            newInput.addEventListener('click', function() {
                // Se o campo contém apenas números, seleciona tudo para facilitar a substituição
                const value = this.value.replace(/[^\d,]/g, '');
                if (value.length > 0) {
                    this.select();
                }
            });
            
            // Adiciona funcionalidade de seleção completa ao focar (se vazio)
            newInput.addEventListener('focus', function() {
                if (this.value === '' || this.value === '0,00') {
                    this.select();
                }
            });
            
            // Melhora a formatação durante a digitação
            newInput.addEventListener('input', function(e) {
                let value = this.value;
                
                // Remove tudo exceto números e vírgula
                value = value.replace(/[^\d,]/g, '');
                
                // Garantir apenas uma vírgula
                const commaCount = (value.match(/,/g) || []).length;
                if (commaCount > 1) {
                    value = value.replace(/,/g, '');
                    value = value.replace(/(\d{2})$/, ',$1');
                }
                
                // Limitar a 2 casas decimais após a vírgula
                const parts = value.split(',');
                if (parts[1] && parts[1].length > 2) {
                    parts[1] = parts[1].substring(0, 2);
                    value = parts.join(',');
                }
                
                // Atualiza o valor
                this.value = value;
                
                // Dispara evento de mudança para outros scripts
                const changeEvent = new Event('change', { bubbles: true });
                this.dispatchEvent(changeEvent);
            });
            
            // Melhora o controle de teclas
            newInput.addEventListener('keydown', function(e) {
                // Permite teclas especiais
                if ([8, 46, 9, 27, 13, 37, 38, 39, 40].indexOf(e.keyCode) !== -1 ||
                    // Permite Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                    (e.keyCode === 65 && e.ctrlKey === true) ||
                    (e.keyCode === 67 && e.ctrlKey === true) ||
                    (e.keyCode === 86 && e.ctrlKey === true) ||
                    (e.keyCode === 88 && e.ctrlKey === true) ||
                    // Permite home, end
                    (e.keyCode >= 35 && e.keyCode <= 36)) {
                    return;
                }
                
                // Permite números e vírgula
                if ((e.keyCode >= 48 && e.keyCode <= 57) || // números
                    (e.keyCode >= 96 && e.keyCode <= 105) || // números do teclado numérico
                    (e.keyCode === 188 || e.keyCode === 190)) { // vírgula
                    return;
                }
                
                // Bloqueia tudo o mais
                e.preventDefault();
            });
            
            // Adiciona funcionalidade de duplo clique para limpar
            newInput.addEventListener('dblclick', function() {
                this.value = '';
                this.focus();
            });
        });
    }
    
    // Executa a melhoria imediatamente
    enhanceCurrencyInputs();
    
    // Re-executa quando novos elementos são adicionados dinamicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.classList && node.classList.contains('currency-input')) {
                            enhanceCurrencyInputs();
                        } else if (node.querySelector && node.querySelector('.currency-input')) {
                            enhanceCurrencyInputs();
                        }
                    }
                });
            }
        });
    });
    
    // Observa mudanças no DOM
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// Função utilitária para formatar valores monetários
function formatCurrency(value) {
    if (typeof value === 'string') {
        value = parseFloat(value.replace(',', '.')) || 0;
    }
    return value.toFixed(2).replace('.', ',');
}

// Função utilitária para limpar campos de moeda
function clearCurrencyField(input) {
    input.value = '';
    input.focus();
    input.select();
}
