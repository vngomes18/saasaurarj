# Sistema de Controle de Estoque - SaaS Gestão

## 📋 Visão Geral

Sistema completo de controle de estoque desenvolvido em Flask com interface moderna e responsiva. Inclui gestão de produtos, fornecedores, compras, vendas, notas fiscais e sistema de suporte.

## 🚀 Funcionalidades Principais

### 📦 Gestão de Estoque
- **Produtos**: Cadastro completo com controle de estoque mínimo
- **Produtos Auxiliares**: Materiais, ferramentas e insumos
- **Controle de Estoque**: Alertas automáticos para produtos com estoque baixo

### 🏪 Gestão Comercial
- **Clientes**: Cadastro completo de clientes
- **Fornecedores**: Gestão de fornecedores e parceiros comerciais
- **Vendas**: Sistema completo de vendas com controle de estoque
- **Compras**: Gestão de compras com confirmação e atualização automática do estoque

### 📄 Gestão Fiscal
- **Notas Fiscais**: Cadastro e gestão de notas fiscais
- **Integração**: Vinculação com compras e vendas

### 🎫 Sistema de Suporte
- **Tickets**: Sistema completo de tickets de suporte
- **Categorização**: Diferentes tipos de solicitações
- **Prioridades**: Sistema de prioridades para atendimento

## 🎨 Interface e Design

### Design Moderno
- **Interface Responsiva**: Funciona perfeitamente em desktop, tablet e mobile
- **Tema Moderno**: Gradientes, sombras e animações suaves
- **UX Intuitiva**: Navegação clara e organizada

### Componentes Visuais
- **Cards Interativos**: Com hover effects e animações
- **Tabelas Responsivas**: Com filtros e ordenação
- **Formulários Intuitivos**: Com validação e feedback visual
- **Dashboard Completo**: Com estatísticas e gráficos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite (SQLAlchemy)
- **Frontend**: Bootstrap 5, Font Awesome
- **Gráficos**: Chart.js
- **Estilo**: CSS3 com gradientes e animações

## 📊 Dashboard

O dashboard principal inclui:

### Estatísticas Principais
- Total de produtos cadastrados
- Clientes ativos
- Fornecedores ativos
- Produtos auxiliares

### Indicadores Financeiros
- Vendas do mês atual
- Compras do mês atual
- Alertas de estoque baixo

### Ações Rápidas
- Nova venda
- Nova compra
- Cadastrar produto
- Novo fornecedor
- Produto auxiliar
- Nota fiscal
- Suporte

## 🗂️ Estrutura do Sistema

### Módulos Principais

1. **Estoque**
   - Produtos
   - Produtos Auxiliares

2. **Comercial**
   - Clientes
   - Fornecedores

3. **Movimentações**
   - Vendas
   - Compras

4. **Fiscal**
   - Notas Fiscais

5. **Suporte**
   - Tickets de Suporte

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Instalação
1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o sistema:
   ```bash
   python app.py
   ```

4. Acesse: `http://localhost:5000`

## 📱 Responsividade

O sistema é totalmente responsivo e funciona perfeitamente em:
- **Desktop**: Layout completo com sidebar
- **Tablet**: Layout adaptado com menu colapsável
- **Mobile**: Interface otimizada para touch

## 🎯 Funcionalidades por Módulo

### Fornecedores
- Cadastro completo com dados fiscais
- Controle de status (ativo/inativo)
- Integração com sistema de compras
- Máscaras automáticas para CNPJ, telefone e CEP

### Compras
- Criação automática de números de compra
- Seleção de fornecedores ativos
- Adição de múltiplos produtos
- Cálculo automático de totais
- Confirmação com atualização de estoque

### Produtos Auxiliares
- Categorização (Material, Ferramenta, Insumo, etc.)
- Unidades de medida personalizáveis
- Controle de estoque mínimo
- Códigos internos

### Notas Fiscais
- Suporte a diferentes modelos (NFe, NFCe, NF, NFS)
- Chave de acesso
- Vinculação com compras
- Controle de status

### Suporte
- Sistema de tickets completo
- Categorização de solicitações
- Sistema de prioridades
- Conversas com equipe de suporte

## 🎨 Personalização Visual

### Cores e Temas
- Gradientes modernos
- Paleta de cores consistente
- Efeitos hover e transições suaves
- Ícones Font Awesome

### Componentes
- Cards com sombras e bordas arredondadas
- Botões com gradientes
- Tabelas responsivas
- Formulários estilizados

## 📈 Relatórios e Estatísticas

- Dashboard com métricas principais
- Gráficos de vendas dos últimos 7 dias
- Alertas de estoque baixo
- Histórico de movimentações

## 🔐 Segurança

- Sistema de autenticação
- Controle de sessão
- Isolamento de dados por usuário
- Validação de formulários

## 🚀 Próximas Funcionalidades

- Relatórios avançados
- Exportação de dados
- Integração com APIs fiscais
- Sistema de backup automático
- Notificações em tempo real

## 📞 Suporte

O sistema inclui um módulo completo de suporte onde os usuários podem:
- Criar tickets de suporte
- Categorizar suas solicitações
- Definir prioridades
- Acompanhar o status do atendimento

## 🎉 Conclusão

Este sistema de controle de estoque oferece uma solução completa e moderna para gestão de negócios, com interface intuitiva e funcionalidades robustas. O design responsivo garante uma excelente experiência em qualquer dispositivo.

