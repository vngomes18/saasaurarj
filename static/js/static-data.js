/**
 * Dados Estáticos para Reduzir Requisições
 * Para sistemas com limite muito restritivo (5 req/min)
 */

window.STATIC_DATA = {
    // Categorias mais comuns
    categorias: [
        'Eletrônicos',
        'Roupas e Acessórios',
        'Casa e Jardim',
        'Esportes e Lazer',
        'Livros e Mídia',
        'Beleza e Saúde',
        'Automóveis',
        'Brinquedos',
        'Pet Shop',
        'Ferramentas',
        'Alimentícios',
        'Móveis',
        'Informática',
        'Celulares',
        'Eletrodomésticos',
        'Perfumaria',
        'Calçados',
        'Bolsas',
        'Relógios',
        'Joias',
        'Outros'
    ],
    
    // CFOPs mais comuns
    cfops: [
        '1102 - Compra para comercialização',
        '1101 - Compra para industrialização',
        '1202 - Devolução de venda de mercadoria',
        '1403 - Compra para comercialização em operação com ST',
        '1949 - Outras entradas não especificadas',
        '5102 - Venda de mercadoria adquirida',
        '5101 - Venda de mercadoria própria',
        '5202 - Devolução de compra para comercialização',
        '5403 - Venda de mercadoria em operação com ST',
        '5949 - Outras saídas não especificadas',
        '6102 - Venda de mercadoria para fora do estado',
        '6101 - Venda de mercadoria própria para fora do estado',
        '6202 - Devolução de compra para fora do estado',
        '6403 - Venda com ST para fora do estado',
        '6949 - Outras saídas para fora do estado'
    ],
    
    // CSTs mais comuns
    csts: [
        '00 - Tributada integralmente',
        '10 - Tributada e com cobrança do ICMS por ST',
        '20 - Com redução de base de cálculo',
        '30 - Isenta ou não tributada e com cobrança do ICMS por ST',
        '40 - Isenta',
        '41 - Não tributada',
        '50 - Suspensão',
        '51 - Diferimento',
        '60 - ICMS cobrado anteriormente por ST',
        '70 - Com redução de base de cálculo e cobrança do ICMS por ST',
        '90 - Outras'
    ],
    
    // Estados brasileiros
    estados: [
        { uf: 'AC', nome: 'Acre' },
        { uf: 'AL', nome: 'Alagoas' },
        { uf: 'AP', nome: 'Amapá' },
        { uf: 'AM', nome: 'Amazonas' },
        { uf: 'BA', nome: 'Bahia' },
        { uf: 'CE', nome: 'Ceará' },
        { uf: 'DF', nome: 'Distrito Federal' },
        { uf: 'ES', nome: 'Espírito Santo' },
        { uf: 'GO', nome: 'Goiás' },
        { uf: 'MA', nome: 'Maranhão' },
        { uf: 'MT', nome: 'Mato Grosso' },
        { uf: 'MS', nome: 'Mato Grosso do Sul' },
        { uf: 'MG', nome: 'Minas Gerais' },
        { uf: 'PA', nome: 'Pará' },
        { uf: 'PB', nome: 'Paraíba' },
        { uf: 'PR', nome: 'Paraná' },
        { uf: 'PE', nome: 'Pernambuco' },
        { uf: 'PI', nome: 'Piauí' },
        { uf: 'RJ', nome: 'Rio de Janeiro' },
        { uf: 'RN', nome: 'Rio Grande do Norte' },
        { uf: 'RS', nome: 'Rio Grande do Sul' },
        { uf: 'RO', nome: 'Rondônia' },
        { uf: 'RR', nome: 'Roraima' },
        { uf: 'SC', nome: 'Santa Catarina' },
        { uf: 'SP', nome: 'São Paulo' },
        { uf: 'SE', nome: 'Sergipe' },
        { uf: 'TO', nome: 'Tocantins' }
    ],
    
    // Formas de pagamento
    formasPagamento: [
        'Dinheiro',
        'Cartão de Débito',
        'Cartão de Crédito',
        'PIX',
        'Boleto Bancário',
        'Transferência Bancária',
        'Cheque',
        'Crediário',
        'Vale Alimentação',
        'Vale Refeição'
    ],
    
    // Tipos de cliente
    tiposCliente: [
        'Pessoa Física',
        'Pessoa Jurídica',
        'Consumidor Final',
        'Revenda',
        'Atacado',
        'Varejo'
    ],
    
    // Unidades de medida
    unidadesMedida: [
        'UN - Unidade',
        'PC - Peça',
        'KG - Quilograma',
        'G - Grama',
        'L - Litro',
        'ML - Mililitro',
        'M - Metro',
        'CM - Centímetro',
        'M² - Metro Quadrado',
        'M³ - Metro Cúbico',
        'CX - Caixa',
        'PCT - Pacote',
        'DZ - Dúzia',
        'PAR - Par'
    ]
};

/**
 * Função para buscar dados estáticos com filtro
 */
window.getStaticData = function(type, filter = '') {
    const data = window.STATIC_DATA[type] || [];
    
    if (!filter) {
        return data;
    }
    
    const filterLower = filter.toLowerCase();
    
    return data.filter(item => {
        const text = typeof item === 'string' ? item : (item.nome || item.text || '');
        return text.toLowerCase().includes(filterLower);
    });
};

/**
 * Função para adicionar dados personalizados
 */
window.addStaticData = function(type, newData) {
    if (!window.STATIC_DATA[type]) {
        window.STATIC_DATA[type] = [];
    }
    
    // Evitar duplicatas
    const existing = window.STATIC_DATA[type];
    const newItem = typeof newData === 'string' ? newData : newData.nome || newData.text;
    
    if (!existing.some(item => {
        const text = typeof item === 'string' ? item : (item.nome || item.text || '');
        return text === newItem;
    })) {
        existing.push(newData);
        console.log(`✅ Adicionado aos dados estáticos [${type}]:`, newData);
    }
};

/**
 * Função para salvar dados no localStorage
 */
window.saveStaticDataToLocal = function() {
    try {
        localStorage.setItem('staticData', JSON.stringify(window.STATIC_DATA));
        console.log('💾 Dados estáticos salvos no localStorage');
    } catch (error) {
        console.error('Erro ao salvar dados estáticos:', error);
    }
};

/**
 * Função para carregar dados do localStorage
 */
window.loadStaticDataFromLocal = function() {
    try {
        const saved = localStorage.getItem('staticData');
        if (saved) {
            const parsedData = JSON.parse(saved);
            // Mesclar com dados padrão
            Object.keys(parsedData).forEach(key => {
                if (window.STATIC_DATA[key]) {
                    // Mesclar arrays evitando duplicatas
                    const merged = [...window.STATIC_DATA[key]];
                    parsedData[key].forEach(item => {
                        const text = typeof item === 'string' ? item : (item.nome || item.text || '');
                        if (!merged.some(existing => {
                            const existingText = typeof existing === 'string' ? existing : (existing.nome || existing.text || '');
                            return existingText === text;
                        })) {
                            merged.push(item);
                        }
                    });
                    window.STATIC_DATA[key] = merged;
                } else {
                    window.STATIC_DATA[key] = parsedData[key];
                }
            });
            console.log('📂 Dados estáticos carregados do localStorage');
        }
    } catch (error) {
        console.error('Erro ao carregar dados estáticos:', error);
    }
};

// Carregar dados salvos ao inicializar
document.addEventListener('DOMContentLoaded', () => {
    window.loadStaticDataFromLocal();
    
    // Salvar automaticamente quando dados forem adicionados
    const originalAddStaticData = window.addStaticData;
    window.addStaticData = function(type, newData) {
        originalAddStaticData(type, newData);
        window.saveStaticDataToLocal();
    };
});

console.log('📊 Static Data System loaded - Dados para reduzir requisições');
