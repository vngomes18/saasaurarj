// Main JavaScript for SaaS Sistema de Gestão

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Confirm delete actions
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            if (confirm('Tem certeza que deseja excluir este item?')) {
                window.location.href = url;
            }
        });
    });

    // Real-time search in tables
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.table-responsive').querySelector('table');
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('.currency-input');
    currencyInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            value = (value / 100).toFixed(2);
            this.value = 'R$ ' + value.replace('.', ',');
        });
    });

    // Format phone inputs
    const phoneInputs = document.querySelectorAll('.phone-input');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length <= 11) {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
                if (value.length < 14) {
                    value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
                }
            }
            this.value = value;
        });
    });

    // Format CPF/CNPJ inputs
    const cpfCnpjInputs = document.querySelectorAll('.cpf-cnpj-input');
    cpfCnpjInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length <= 11) {
                // CPF format
                value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            } else {
                // CNPJ format
                value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
            }
            this.value = value;
        });
    });

    // Dynamic form for sale items
    if (document.getElementById('sale-form')) {
        const saleForm = document.getElementById('sale-form');
        const addItemBtn = document.getElementById('add-item-btn');
        const itemsContainer = document.getElementById('sale-items');
        let itemCount = 0;

        addItemBtn.addEventListener('click', function() {
            itemCount++;
            const itemHtml = `
                <div class="row sale-item mb-3" data-item="${itemCount}">
                    <div class="col-md-4">
                        <label class="form-label">Produto</label>
                        <select class="form-select produto-select" name="produto_${itemCount}" required>
                            <option value="">Selecione um produto</option>
                            <!-- Produtos serão carregados via AJAX -->
                        </select>
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Quantidade</label>
                        <input type="number" class="form-control quantidade-input" name="quantidade_${itemCount}" min="1" required>
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Preço Unit.</label>
                        <input type="text" class="form-control preco-input" readonly>
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Subtotal</label>
                        <input type="text" class="form-control subtotal-input" readonly>
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">&nbsp;</label>
                        <button type="button" class="btn btn-danger btn-sm d-block remove-item-btn">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
            itemsContainer.insertAdjacentHTML('beforeend', itemHtml);
            loadProducts(itemCount);
        });

        // Load products for new item
        function loadProducts(itemIndex) {
            fetch('/api/produtos')
                .then(response => response.json())
                .then(produtos => {
                    const select = document.querySelector(`[data-item="${itemIndex}"] .produto-select`);
                    produtos.forEach(produto => {
                        const option = document.createElement('option');
                        option.value = produto.id;
                        option.textContent = `${produto.nome} - R$ ${produto.preco.toFixed(2)} (Estoque: ${produto.estoque_atual})`;
                        option.dataset.preco = produto.preco;
                        option.dataset.estoque = produto.estoque_atual;
                        select.appendChild(option);
                    });
                });
        }

        // Handle product selection
        itemsContainer.addEventListener('change', function(e) {
            if (e.target.classList.contains('produto-select')) {
                const selectedOption = e.target.selectedOptions[0];
                const itemRow = e.target.closest('.sale-item');
                const precoInput = itemRow.querySelector('.preco-input');
                
                if (selectedOption && selectedOption.dataset.preco) {
                    precoInput.value = 'R$ ' + parseFloat(selectedOption.dataset.preco).toFixed(2);
                    calculateSubtotal(itemRow);
                }
            }
        });

        // Handle quantity change
        itemsContainer.addEventListener('input', function(e) {
            if (e.target.classList.contains('quantidade-input')) {
                const itemRow = e.target.closest('.sale-item');
                calculateSubtotal(itemRow);
            }
        });

        // Remove item
        itemsContainer.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-item-btn') || e.target.closest('.remove-item-btn')) {
                const itemRow = e.target.closest('.sale-item');
                itemRow.remove();
                calculateTotal();
            }
        });

        function calculateSubtotal(itemRow) {
            const quantidade = parseFloat(itemRow.querySelector('.quantidade-input').value) || 0;
            const preco = parseFloat(itemRow.querySelector('.preco-input').value.replace('R$ ', '').replace(',', '.')) || 0;
            const subtotal = quantidade * preco;
            
            itemRow.querySelector('.subtotal-input').value = 'R$ ' + subtotal.toFixed(2);
            calculateTotal();
        }

        function calculateTotal() {
            const subtotals = document.querySelectorAll('.subtotal-input');
            let total = 0;
            
            subtotals.forEach(input => {
                const value = parseFloat(input.value.replace('R$ ', '').replace(',', '.')) || 0;
                total += value;
            });
            
            const totalInput = document.querySelector('#valor-total');
            if (totalInput) {
                totalInput.value = 'R$ ' + total.toFixed(2);
            }
        }
    }

    // Initialize charts
    if (document.getElementById('salesChart')) {
        const ctx = document.getElementById('salesChart').getContext('2d');
        const salesData = JSON.parse(document.getElementById('salesChart').dataset.sales || '[]');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: salesData.map(item => item.data),
                datasets: [{
                    label: 'Vendas',
                    data: salesData.map(item => item.vendas),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    // Print functionality
    document.querySelectorAll('.btn-print').forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Export to CSV functionality
    document.querySelectorAll('.btn-export-csv').forEach(button => {
        button.addEventListener('click', function() {
            const table = this.closest('.table-responsive').querySelector('table');
            const csv = tableToCSV(table);
            downloadCSV(csv, 'export.csv');
        });
    });

    function tableToCSV(table) {
        let csv = [];
        const rows = table.querySelectorAll('tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('th, td');
            const rowData = Array.from(cells).map(cell => {
                return '"' + cell.textContent.trim().replace(/"/g, '""') + '"';
            });
            csv.push(rowData.join(','));
        });
        
        return csv.join('\n');
    }

    function downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Add loading states to forms (only for actual form submissions, not cancel buttons)
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            // Get the element that triggered the submit
            const submitter = e.submitter;
            
            // Don't apply loading state for cancel buttons or links
            if (!submitter || 
                submitter.type === 'button' ||
                submitter.classList.contains('btn-outline-secondary') || 
                submitter.classList.contains('btn-secondary') ||
                submitter.textContent.toLowerCase().includes('cancelar') ||
                submitter.textContent.toLowerCase().includes('voltar')) {
                return; // Don't apply loading state for cancel buttons
            }
            
            // Only apply loading state for actual submit buttons
            if (submitter && submitter.type === 'submit') {
                const originalText = submitter.innerHTML;
                submitter.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processando...';
                submitter.disabled = true;
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitter.innerHTML = originalText;
                    submitter.disabled = false;
                }, 10000);
            }
        });
    });
    
    // Ensure cancel buttons work properly without interference
    document.querySelectorAll('a[href], button[type="button"]').forEach(element => {
        if (element.textContent.toLowerCase().includes('cancelar') || 
            element.textContent.toLowerCase().includes('voltar')) {
            element.addEventListener('click', function(e) {
                // Don't prevent default for cancel buttons - let them work normally
                e.stopPropagation();
            });
        }
    });
});

// Utility functions
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(date));
}

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

