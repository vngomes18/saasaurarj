// Modal Fix - Solução para problemas com modais que travam o site
// Este arquivo resolve conflitos e problemas de z-index em modais

document.addEventListener('DOMContentLoaded', function() {
    // Função para corrigir problemas de modal
    function fixModalIssues() {
        // Corrigir z-index de modais
        const modals = document.querySelectorAll('.modal');
        modals.forEach((modal, index) => {
            modal.style.zIndex = 1060 + index;
        });
        
        // Corrigir backdrop de modais
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach((backdrop, index) => {
            backdrop.style.zIndex = 1055 + index;
        });
        
        // Garantir que o body não trave incorretamente
        function ensureBodyScroll() {
            if (!document.querySelector('.modal.show')) {
                document.body.style.overflow = '';
                document.body.style.paddingRight = '';
                document.body.classList.remove('modal-open');
            }
        }
        
        // Executar verificação periodicamente
        setInterval(ensureBodyScroll, 100);
        
        // Corrigir quando modais são fechados
        document.addEventListener('hidden.bs.modal', function(e) {
            // Limpar estilos do body
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            
            // Remover classe modal-open se não há modais abertos
            if (!document.querySelector('.modal.show')) {
                document.body.classList.remove('modal-open');
            }
        });
        
        // Corrigir quando modais são mostrados
        document.addEventListener('shown.bs.modal', function(e) {
            // Garantir que apenas este modal tenha foco
            const modal = e.target;
            const backdrops = document.querySelectorAll('.modal-backdrop');
            
            // Remover backdrops duplicados
            if (backdrops.length > 1) {
                for (let i = 1; i < backdrops.length; i++) {
                    backdrops[i].remove();
                }
            }
            
            // Garantir que o modal tenha o z-index correto
            modal.style.zIndex = 1060;
            
            // Focar no primeiro campo de input do modal
            const firstInput = modal.querySelector('input, textarea, select');
            if (firstInput) {
                setTimeout(() => {
                    firstInput.focus();
                }, 300);
            }
        });
    }
    
    // Executar correção imediatamente
    fixModalIssues();
    
    // Re-executar quando novos elementos são adicionados
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.classList && node.classList.contains('modal')) {
                        fixModalIssues();
                    }
                });
            }
        });
    });
    
    // Observar mudanças no DOM
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Função para limpar problemas de modal
    function cleanupModalIssues() {
        // Remover backdrops duplicados
        const backdrops = document.querySelectorAll('.modal-backdrop');
        if (backdrops.length > 1) {
            for (let i = 1; i < backdrops.length; i++) {
                backdrops[i].remove();
            }
        }
        
        // Limpar estilos do body
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
        
        // Remover classe modal-open se não há modais
        if (!document.querySelector('.modal.show')) {
            document.body.classList.remove('modal-open');
        }
    }
    
    // Limpar problemas periodicamente
    setInterval(cleanupModalIssues, 500);
    
    // Limpar quando a página é descarregada
    window.addEventListener('beforeunload', cleanupModalIssues);
    
    // Limpar quando há mudança de foco
    window.addEventListener('blur', cleanupModalIssues);
    window.addEventListener('focus', cleanupModalIssues);
});

// Função utilitária para abrir modal sem problemas
function openModalSafely(modalElement) {
    // Limpar problemas existentes primeiro
    cleanupModalIssues();
    
    // Mostrar modal
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
    
    // Garantir que funcione corretamente
    setTimeout(() => {
        const firstInput = modalElement.querySelector('input, textarea, select');
        if (firstInput) {
            firstInput.focus();
        }
    }, 300);
}

// Função utilitária para fechar todos os modais
function closeAllModals() {
    const modals = document.querySelectorAll('.modal.show');
    modals.forEach(modal => {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
    });
    
    // Limpar problemas
    cleanupModalIssues();
}

// Função para limpar problemas de modal (acessível globalmente)
function cleanupModalIssues() {
    // Remover backdrops duplicados
    const backdrops = document.querySelectorAll('.modal-backdrop');
    if (backdrops.length > 1) {
        for (let i = 1; i < backdrops.length; i++) {
            backdrops[i].remove();
        }
    }
    
    // Limpar estilos do body
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    
    // Remover classe modal-open se não há modais
    if (!document.querySelector('.modal.show')) {
        document.body.classList.remove('modal-open');
    }
}
