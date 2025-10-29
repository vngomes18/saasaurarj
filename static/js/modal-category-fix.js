// Modal Category Fix - Solução específica para o modal de nova categoria
// Este arquivo resolve problemas específicos com o modal de categoria que bloqueia cliques

document.addEventListener('DOMContentLoaded', function() {
    // Função para corrigir problemas específicos do modal de categoria
    function fixCategoryModal() {
        const modal = document.getElementById('novaCategoriaModal');
        if (!modal) return;
        
        // Garantir que o modal tenha z-index correto
        modal.style.zIndex = '9999';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        
        // Garantir que o backdrop seja removido se existir
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => {
            if (backdrop.style.zIndex < '9998') {
                backdrop.remove();
            }
        });
        
        // Garantir que todos os elementos do modal sejam clicáveis
        const modalContent = modal.querySelector('.modal-content');
        if (modalContent) {
            modalContent.style.zIndex = '10000';
            modalContent.style.pointerEvents = 'auto';
            modalContent.style.position = 'relative';
            
            // Garantir que todos os elementos internos sejam clicáveis
            const allElements = modalContent.querySelectorAll('*');
            allElements.forEach(el => {
                el.style.pointerEvents = 'auto';
                el.style.position = 'relative';
                el.style.zIndex = '10001';
            });
            
            // Garantir que os botões sejam clicáveis
            const buttons = modalContent.querySelectorAll('.btn');
            buttons.forEach(btn => {
                btn.style.pointerEvents = 'auto';
                btn.style.cursor = 'pointer';
                btn.style.zIndex = '10002';
            });
            
            // Garantir que o input seja clicável
            const inputs = modalContent.querySelectorAll('input');
            inputs.forEach(input => {
                input.style.pointerEvents = 'auto';
                input.style.cursor = 'text';
                input.style.zIndex = '10002';
            });
        }
        
        // Garantir que o body não tenha pointer-events bloqueado
        document.body.style.pointerEvents = 'auto';
        
        // Remover qualquer overlay invisível
        const overlays = document.querySelectorAll('.modal::before, .modal::after');
        overlays.forEach(overlay => overlay.remove());
    }
    
    // Executar correção quando o modal é aberto
    const modal = document.getElementById('novaCategoriaModal');
    if (modal) {
        // Quando o modal é mostrado
        modal.addEventListener('shown.bs.modal', function() {
            fixCategoryModal();
            
            // Focar no campo de input
            const input = modal.querySelector('#nova-categoria-nome');
            if (input) {
                setTimeout(() => {
                    input.focus();
                    input.select();
                }, 100);
            }
        });
        
        // Quando o modal está sendo mostrado
        modal.addEventListener('show.bs.modal', function() {
            // Limpar problemas antes de mostrar
            document.body.style.pointerEvents = 'auto';
            
            // Remover backdrops duplicados
            const backdrops = document.querySelectorAll('.modal-backdrop');
            backdrops.forEach(backdrop => backdrop.remove());
        });
        
        // Quando o modal é fechado
        modal.addEventListener('hidden.bs.modal', function() {
            // Limpar todos os problemas
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            document.body.style.pointerEvents = 'auto';
            document.body.classList.remove('modal-open');
            
            // Remover todos os backdrops
            const backdrops = document.querySelectorAll('.modal-backdrop');
            backdrops.forEach(backdrop => backdrop.remove());
            
            // Limpar valor do input
            const input = modal.querySelector('#nova-categoria-nome');
            if (input) {
                input.value = '';
            }
        });
    }
    
    // Função para forçar a correção do modal
    function forceFixModal() {
        const modal = document.getElementById('novaCategoriaModal');
        if (modal && modal.classList.contains('show')) {
            fixCategoryModal();
        }
    }
    
    // Executar correção periodicamente quando o modal estiver aberto
    setInterval(() => {
        const modal = document.getElementById('novaCategoriaModal');
        if (modal && modal.classList.contains('show')) {
            forceFixModal();
        }
    }, 100);
    
    // Executar correção quando há cliques no modal
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('novaCategoriaModal');
        if (modal && modal.classList.contains('show')) {
            // Se o clique foi no modal, garantir que funcione
            if (modal.contains(e.target)) {
                forceFixModal();
            }
        }
    });
    
    // Função para abrir o modal de forma segura
    function openCategoryModalSafely() {
        const modal = document.getElementById('novaCategoriaModal');
        if (modal) {
            // Limpar problemas antes de abrir
            document.body.style.pointerEvents = 'auto';
            
            // Remover backdrops existentes
            const backdrops = document.querySelectorAll('.modal-backdrop');
            backdrops.forEach(backdrop => backdrop.remove());
            
            // Abrir modal
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            
            // Aplicar correções após um pequeno delay
            setTimeout(() => {
                fixCategoryModal();
            }, 100);
        }
    }
    
    // Tornar função globalmente acessível
    window.openCategoryModalSafely = openCategoryModalSafely;
});

// Função utilitária para corrigir modal de categoria
function fixCategoryModalIssues() {
    const modal = document.getElementById('novaCategoriaModal');
    if (!modal) return;
    
    // Forçar z-index alto
    modal.style.zIndex = '9999';
    
    // Garantir que todos os elementos sejam clicáveis
    const allElements = modal.querySelectorAll('*');
    allElements.forEach(el => {
        el.style.pointerEvents = 'auto';
        el.style.position = 'relative';
        el.style.zIndex = '10001';
    });
    
    // Garantir que o body não esteja bloqueado
    document.body.style.pointerEvents = 'auto';
    
    // Remover backdrops duplicados
    const backdrops = document.querySelectorAll('.modal-backdrop');
    if (backdrops.length > 1) {
        for (let i = 1; i < backdrops.length; i++) {
            backdrops[i].remove();
        }
    }
}
