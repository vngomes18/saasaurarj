# 🚀 Instruções de Execução - SaaS Sistema de Gestão

## ⚡ Execução Rápida

### Opção 1: Instalação Automática (Recomendado)
```bash
python install.py
```

### Opção 2: Instalação Manual

#### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 2. Executar o sistema
```bash
python run.py
```

#### 3. Acessar o sistema
- **URL**: http://localhost:5000
- **Login**: http://localhost:5000/login
- **Registro**: http://localhost:5000/register

## 🎯 Primeiro Uso

### 1. Criar conta de usuário
1. Acesse http://localhost:5000/register
2. Preencha os dados:
   - **Nome de usuário**: admin
   - **Email**: admin@sistema.com
   - **Empresa**: Sua Empresa LTDA
   - **Senha**: 123456

### 2. Fazer login
1. Acesse http://localhost:5000/login
2. Use as credenciais criadas

### 3. Começar a usar
- **Dashboard**: Visualize métricas e estatísticas
- **Produtos**: Cadastre seus produtos
- **Clientes**: Cadastre sua base de clientes
- **Vendas**: Realize vendas

## 📊 Dados de Exemplo (Opcional)

Para testar o sistema com dados já cadastrados:

```bash
python exemplo_uso.py
```

Isso criará:
- 1 usuário: admin@sistema.com (senha: 123456)
- 5 produtos de exemplo
- 3 clientes de exemplo
- 3 vendas de exemplo

## 🔧 Configurações Avançadas

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-super-segura
SQLALCHEMY_DATABASE_URI=sqlite:///saas_sistema.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### Banco de Dados
- **Desenvolvimento**: SQLite (padrão)
- **Produção**: PostgreSQL, MySQL, etc.

## 🐛 Solução de Problemas

### Erro de dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de banco de dados
```bash
# Deletar banco atual (se existir)
rm instance/saas_sistema.db

# Executar novamente
python run.py
```

### Porta já em uso
```bash
# Mudar porta no run.py ou usar:
python run.py --port 5001
```

## 📱 Funcionalidades Principais

### Dashboard
- ✅ Métricas em tempo real
- ✅ Gráficos de vendas
- ✅ Alertas de estoque baixo
- ✅ Vendas recentes

### Produtos
- ✅ Cadastro completo
- ✅ Controle de estoque
- ✅ Categorização
- ✅ Busca e filtros

### Clientes
- ✅ Cadastro completo
- ✅ Informações de contato
- ✅ Histórico de compras

### Vendas
- ✅ Sistema completo de vendas
- ✅ Múltiplas formas de pagamento
- ✅ Cálculo automático
- ✅ Impressão de cupons

## 🎨 Interface

- **Responsiva**: Funciona em desktop, tablet e mobile
- **Modern**: Design limpo e profissional
- **Intuitiva**: Fácil de usar
- **Rápida**: Carregamento otimizado

## 🔒 Segurança

- **Autenticação**: Sistema de login seguro
- **Sessões**: Controle de sessão de usuário
- **Multi-tenant**: Cada usuário tem seus próprios dados
- **Validação**: Validação de dados no frontend e backend

## 📈 Próximos Passos

1. **Teste todas as funcionalidades**
2. **Cadastre seus produtos reais**
3. **Importe sua base de clientes**
4. **Configure as categorias**
5. **Personalize conforme necessário**

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Confirme se todas as dependências estão instaladas
3. Verifique se a porta 5000 está livre
4. Consulte o README.md completo

---

**🎉 Pronto para começar a usar seu sistema de gestão!**

