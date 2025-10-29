// Dropdown Fix JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Fix dropdown z-index issues
    fixDropdownZIndex();
    
    // Ensure dropdowns work properly
    setupDropdownHandlers();
});

function fixDropdownZIndex() {
    // Get all dropdown menus
    const dropdowns = document.querySelectorAll('.dropdown-menu');
    
    dropdowns.forEach(dropdown => {
        // Ensure high z-index
        dropdown.style.zIndex = '1060';
        
        // Add event listeners to ensure visibility
        dropdown.addEventListener('show.bs.dropdown', function() {
            this.style.zIndex = '1060';
            this.style.position = 'absolute';
            this.style.display = 'block';
        });
        
        dropdown.addEventListener('shown.bs.dropdown', function() {
            this.style.zIndex = '1060';
            this.style.display = 'block';
        });
        
        dropdown.addEventListener('hide.bs.dropdown', function() {
            // Keep z-index high during hide animation
            this.style.zIndex = '1060';
        });
    });
}

function setupDropdownHandlers() {
    // Handle navbar dropdowns specifically
    const navbarDropdowns = document.querySelectorAll('.navbar-nav .dropdown');
    
    navbarDropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            // Ensure proper positioning
            toggle.addEventListener('click', function(e) {
                // Set high z-index for the dropdown
                menu.style.zIndex = '1060';
                menu.style.position = 'absolute';
                
                // Ensure it's positioned correctly
                if (menu.classList.contains('dropdown-menu-end')) {
                    menu.style.right = '0';
                    menu.style.left = 'auto';
                }
            });
            
            // Handle when dropdown is shown
            dropdown.addEventListener('show.bs.dropdown', function() {
                menu.style.zIndex = '1060';
                menu.style.position = 'absolute';
            });
            
            // Handle when dropdown is hidden
            dropdown.addEventListener('hide.bs.dropdown', function() {
                // Keep z-index high during hide
                menu.style.zIndex = '1060';
            });
        }
    });
}

// Additional fix for Bootstrap 5 dropdown issues
document.addEventListener('click', function(e) {
    // If clicking outside dropdown, ensure proper z-index
    if (!e.target.closest('.dropdown')) {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(dropdown => {
            dropdown.style.zIndex = '1060';
        });
    }
});

// Fix for window resize
window.addEventListener('resize', function() {
    const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
    openDropdowns.forEach(dropdown => {
        dropdown.style.zIndex = '1060';
        dropdown.style.position = 'absolute';
    });
});

// Fix for scroll events
window.addEventListener('scroll', function() {
    const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
    openDropdowns.forEach(dropdown => {
        dropdown.style.zIndex = '1060';
    });
});
