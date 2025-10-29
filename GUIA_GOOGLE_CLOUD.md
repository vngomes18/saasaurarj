# 🔐 Guia Visual - Configuração Google Cloud Console

## 📋 **Passo a Passo Detalhado**

### 🚀 **Passo 1: Acessar Google Cloud Console**
1. Abra: https://console.cloud.google.com/
2. Faça login com sua conta Google
3. Aceite os termos se solicitado

### 🆕 **Passo 2: Criar Projeto**
1. Clique em **"Selecionar um projeto"** (topo da página)
2. Clique em **"NOVO PROJETO"**
3. Nome do projeto: `SaaS Sistema OAuth`
4. Clique em **"CRIAR"**
5. Aguarde a criação (alguns segundos)

### 🔧 **Passo 3: Ativar Google+ API**
1. Menu lateral: **"APIs e serviços"** → **"Biblioteca"**
2. Busque por: `Google+ API`
3. Clique na API quando aparecer
4. Clique em **"ATIVAR"**
5. Aguarde a ativação

### ⚙️ **Passo 4: Configurar Tela de Consentimento**
1. Menu: **"APIs e serviços"** → **"Tela de consentimento OAuth"**
2. Selecione **"Externo"** → **"CRIAR"**
3. Preencha:
   - **Nome do aplicativo**: `SaaS Sistema de Gestão`
   - **Email de suporte**: Seu email
   - **Email do desenvolvedor**: Seu email
4. Clique **"SALVAR E CONTINUAR"**
5. Seção "Escopos": **"SALVAR E CONTINUAR"**
6. Seção "Usuários de teste":
   - Adicione seu email
   - Clique **"SALVAR E CONTINUAR"**

### 🔑 **Passo 5: Criar Credenciais OAuth**
1. Menu: **"APIs e serviços"** → **"Credenciais"**
2. **"CRIAR CREDENCIAIS"** → **"ID do cliente OAuth 2.0"**
3. Tipo: **"Aplicativo da Web"**
4. Nome: `SaaS Sistema OAuth`
5. **Origens JavaScript autorizadas**:
   ```
   http://localhost:5000
   http://127.0.0.1:5000
   ```
6. **URIs de redirecionamento autorizados**:
   ```
   http://localhost:5000/login/google/authorized
   http://127.0.0.1:5000/login/google/authorized
   ```
7. Clique **"CRIAR"**

### 📋 **Passo 6: Copiar Credenciais**
Após criar, você verá:
- **ID do cliente**: `123456789-abcdef.apps.googleusercontent.com`
- **Chave secreta**: `GOCSPX-abcdef123456`

**COPIE AMBOS OS VALORES!**

### 💾 **Passo 7: Configurar Sistema**

Execute o script de configuração:
```bash
python setup_google_auth.py
```

Cole suas credenciais quando solicitado.

### 🧪 **Passo 8: Testar**
1. Reinicie o servidor: `python run.py`
2. Acesse: http://localhost:5000/login
3. Clique em **"Entrar com Google"**
4. Faça login com sua conta Google
5. Verifique se foi redirecionado para o dashboard

## 🎯 **URLs Importantes**

- **Google Cloud Console**: https://console.cloud.google.com/
- **Sistema Local**: http://localhost:5000/login
- **OAuth Callback**: http://localhost:5000/login/google/authorized

## 🔒 **Configurações de Segurança**

### URLs Autorizadas:
- `http://localhost:5000`
- `http://127.0.0.1:5000`
- `http://localhost:5000/login/google/authorized`
- `http://127.0.0.1:5000/login/google/authorized`

### Para Produção:
- Substitua `localhost` pelo seu domínio real
- Use HTTPS obrigatoriamente
- Configure domínio verificado no Google Console

## 🛠️ **Solução de Problemas**

### Erro "redirect_uri_mismatch":
- Verifique se as URLs estão corretas no Google Console
- Confirme se não há espaços extras nas URLs

### Erro "invalid_client":
- Verifique se o CLIENT_ID está correto
- Confirme se o arquivo .env está na raiz do projeto

### Botão Google não aparece:
- Verifique se as credenciais foram configuradas
- Reinicie o servidor Flask
- Confirme se o arquivo .env existe

## 📞 **Suporte**

Se encontrar problemas:
1. Verifique os logs do servidor Flask
2. Confirme se todas as URLs estão corretas
3. Teste com uma conta Google diferente
4. Verifique se as APIs estão ativadas

---

**🎉 Sucesso!** Seu sistema SaaS agora tem autenticação Google profissional!
