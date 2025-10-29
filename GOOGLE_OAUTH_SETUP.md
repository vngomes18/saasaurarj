# 🔐 Configuração do Google OAuth - SaaS Sistema de Gestão

Este guia irá te ajudar a configurar a autenticação com Google para o seu sistema SaaS.

## 📋 Pré-requisitos

- Conta Google
- Acesso ao Google Cloud Console
- Sistema SaaS já funcionando

## 🚀 Passo a Passo

### 1. Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em "Selecionar um projeto" no topo
3. Clique em "NOVO PROJETO"
4. Digite um nome para o projeto (ex: "SaaS Sistema OAuth")
5. Clique em "CRIAR"

### 2. Ativar APIs Necessárias

1. No menu lateral, vá em "APIs e serviços" > "Biblioteca"
2. Procure por "Google+ API" e clique nela
3. Clique em "ATIVAR"
4. Repita para "Google OAuth2 API" se necessário

### 3. Configurar Tela de Consentimento OAuth

1. Vá em "APIs e serviços" > "Tela de consentimento OAuth"
2. Selecione "Externo" e clique em "CRIAR"
3. Preencha os campos obrigatórios:
   - **Nome do aplicativo**: SaaS Sistema de Gestão
   - **Email de suporte do usuário**: seu-email@gmail.com
   - **Email de contato do desenvolvedor**: seu-email@gmail.com
4. Clique em "SALVAR E CONTINUAR"
5. Na seção "Escopos", clique em "SALVAR E CONTINUAR"
6. Na seção "Usuários de teste", adicione seu email e clique em "SALVAR E CONTINUAR"

### 4. Criar Credenciais OAuth 2.0

1. Vá em "APIs e serviços" > "Credenciais"
2. Clique em "CRIAR CREDENCIAIS" > "ID do cliente OAuth 2.0"
3. Selecione "Aplicativo da Web"
4. Configure as URLs:
   - **Nome**: SaaS Sistema OAuth
   - **Origens JavaScript autorizadas**: 
     - `http://localhost:5000`
     - `http://127.0.0.1:5000`
   - **URIs de redirecionamento autorizados**:
     - `http://localhost:5000/login/google/authorized`
     - `http://127.0.0.1:5000/login/google/authorized`
5. Clique em "CRIAR"

### 5. Obter Credenciais

1. Após criar, você verá uma janela com suas credenciais
2. **Copie o ID do cliente** e **Chave secreta do cliente**
3. Mantenha essas informações seguras!

### 6. Configurar o Sistema

1. Abra o arquivo `config_example.env`
2. Substitua os valores:
   ```
   GOOGLE_CLIENT_ID=seu_client_id_aqui
   GOOGLE_CLIENT_SECRET=sua_client_secret_aqui
   ```
3. Renomeie o arquivo para `.env`

### 7. Testar a Integração

1. Reinicie o servidor Flask:
   ```bash
   python run.py
   ```
2. Acesse: http://localhost:5000/login
3. Clique em "Entrar com Google"
4. Faça login com sua conta Google
5. Verifique se foi redirecionado para o dashboard

## 🔧 Funcionalidades Implementadas

### ✅ Login com Google
- Botão "Entrar com Google" na página de login
- Redirecionamento automático para o Google
- Retorno seguro para o sistema

### ✅ Registro com Google
- Botão "Cadastrar com Google" na página de registro
- Criação automática de conta
- Vinculação de conta Google existente

### ✅ Gerenciamento de Usuários
- Usuários Google têm `google_id` único
- Avatar do Google salvo automaticamente
- Senha não obrigatória para usuários Google
- Vinculação de contas existentes

### ✅ Segurança
- Tokens OAuth seguros
- Validação de domínios autorizados
- Proteção contra CSRF

## 🛠️ Solução de Problemas

### Erro: "redirect_uri_mismatch"
- Verifique se as URLs de redirecionamento estão corretas no Google Console
- Certifique-se de que `http://localhost:5000/login/google/authorized` está listado

### Erro: "invalid_client"
- Verifique se o `GOOGLE_CLIENT_ID` está correto no arquivo `.env`
- Certifique-se de que o arquivo `.env` está na raiz do projeto

### Erro: "access_denied"
- Verifique se a API Google+ está ativada
- Certifique-se de que o email está na lista de usuários de teste

### Botão do Google não aparece
- Verifique se o Font Awesome está carregado
- Certifique-se de que as rotas estão funcionando

## 📱 URLs Importantes

- **Login**: http://localhost:5000/login
- **Registro**: http://localhost:5000/register
- **Google OAuth**: http://localhost:5000/login/google
- **Callback**: http://localhost:5000/login/google/authorized

## 🔒 Segurança em Produção

Para usar em produção, você precisará:

1. **Configurar domínio real** no Google Console
2. **Usar HTTPS** (obrigatório para produção)
3. **Configurar variáveis de ambiente** no servidor
4. **Ativar verificação de domínio** no Google Console

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs do servidor Flask
2. Confirme se todas as URLs estão corretas
3. Teste com uma conta Google diferente
4. Verifique se as APIs estão ativadas

---

**🎉 Parabéns!** Seu sistema SaaS agora suporta autenticação com Google!
