// Settings Management JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar configurações
    initializeSettings();
    
    // Configurar event listeners para dark mode
    setupDarkModeToggle();
    
    // Configurar auto-save para configurações
    setupAutoSave();
});

function initializeSettings() {
    // Verificar se há configurações salvas no localStorage
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        applySettings(settings);
    }
}

function setupDarkModeToggle() {
    // Função removida - dark mode agora só é controlado via página de configurações
}

function setupAutoSave() {
    // Auto-save para formulários de configurações
    const settingsForm = document.querySelector('form[action*="atualizar_configuracoes"]');
    if (settingsForm) {
        const inputs = settingsForm.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Salvar configurações no localStorage
                saveSettingsToLocal();
                
                // Atualizar preview se existir
                updatePreview();
            });
        });
    }
}

function saveSettingsToLocal() {
    const form = document.querySelector('form[action*="atualizar_configuracoes"]');
    if (!form) return;
    
    const formData = new FormData(form);
    const settings = {};
    
    for (let [key, value] of formData.entries()) {
        if (key === 'dark_mode' || key === 'notifications') {
            settings[key] = true;
        } else {
            settings[key] = value;
        }
    }
    
    // Verificar checkboxes que não foram enviados
    const darkModeCheck = document.getElementById('dark_mode');
    const notificationsCheck = document.getElementById('notifications');
    
    if (darkModeCheck && !settings.dark_mode) {
        settings.dark_mode = darkModeCheck.checked;
    }
    
    if (notificationsCheck && !settings.notifications) {
        settings.notifications = notificationsCheck.checked;
    }
    
    localStorage.setItem('userSettings', JSON.stringify(settings));
}

function updatePreview() {
    // Atualizar preview em tempo real se existir
    const previewElements = {
        dark_mode: document.querySelector('.list-group-item:nth-child(1) .badge'),
        notifications: document.querySelector('.list-group-item:nth-child(2) .badge'),
        auto_logout: document.querySelector('.list-group-item:nth-child(3) .badge'),
        dashboard_refresh: document.querySelector('.list-group-item:nth-child(4) .badge')
    };

    if (previewElements.dark_mode) {
        const darkModeCheck = document.getElementById('dark_mode');
        if (darkModeCheck) {
            previewElements.dark_mode.textContent = darkModeCheck.checked ? 'Ativo' : 'Inativo';
            previewElements.dark_mode.className = `badge bg-${darkModeCheck.checked ? 'success' : 'secondary'}`;
        }
    }

    if (previewElements.notifications) {
        const notificationsCheck = document.getElementById('notifications');
        if (notificationsCheck) {
            previewElements.notifications.textContent = notificationsCheck.checked ? 'Ativo' : 'Inativo';
            previewElements.notifications.className = `badge bg-${notificationsCheck.checked ? 'success' : 'secondary'}`;
        }
    }

    if (previewElements.auto_logout) {
        const autoLogoutInput = document.getElementById('auto_logout');
        if (autoLogoutInput) {
            previewElements.auto_logout.textContent = autoLogoutInput.value + 'min';
        }
    }

    if (previewElements.dashboard_refresh) {
        const refreshInput = document.getElementById('dashboard_refresh');
        if (refreshInput) {
            previewElements.dashboard_refresh.textContent = refreshInput.value + 's';
        }
    }
}

function applySettings(settings) {
    // Aplicar configurações salvas
    if (settings.dark_mode !== undefined) {
        const darkModeCheck = document.getElementById('dark_mode');
        if (darkModeCheck) {
            darkModeCheck.checked = settings.dark_mode;
        }
    }
    
    if (settings.notifications !== undefined) {
        const notificationsCheck = document.getElementById('notifications');
        if (notificationsCheck) {
            notificationsCheck.checked = settings.notifications;
        }
    }
    
    if (settings.auto_logout) {
        const autoLogoutInput = document.getElementById('auto_logout');
        if (autoLogoutInput) {
            autoLogoutInput.value = settings.auto_logout;
        }
    }
    
    if (settings.dashboard_refresh) {
        const refreshInput = document.getElementById('dashboard_refresh');
        if (refreshInput) {
            refreshInput.value = settings.dashboard_refresh;
        }
    }
    
    if (settings.language) {
        const languageSelect = document.getElementById('language');
        if (languageSelect) {
            languageSelect.value = settings.language;
        }
    }
    
    if (settings.timezone) {
        const timezoneSelect = document.getElementById('timezone');
        if (timezoneSelect) {
            timezoneSelect.value = settings.timezone;
        }
    }
    
    // Atualizar preview
    updatePreview();
}

function showToast(message, type = 'info') {
    // Criar toast notification
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    var icon = (type === 'success') ? 'check-circle' : (type === 'error') ? 'exclamation-circle' : 'info-circle';
    toast.innerHTML = [
        '<div class="d-flex">',
            '<div class="toast-body">',
                '<i class="fas fa-' + icon + ' me-2"></i>',
                String(message),
            '</div>',
            '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>',
        '</div>'
    ].join('');
    
    toastContainer.appendChild(toast);
    
    // Inicializar e mostrar toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remover toast após ser escondido
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Função removida - dark mode agora controlado apenas via página de configurações
