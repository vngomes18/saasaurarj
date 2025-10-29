# 🚀 Configuração Google OAuth no Vercel

## 📋 **Configuração para Produção**

### **1. Configure o Google Cloud Console**

#### **Acesse o Google Cloud Console:**
https://console.cloud.google.com/

#### **Configure OAuth 2.0 para Produção:**
1. Vá para "APIs e serviços" → "Credenciais"
2. Edite seu OAuth 2.0 Client ID existente
3. Adicione as URLs de produção:

**Origens JavaScript autorizadas:**
```
https://seu-dominio.vercel.app
```

**URIs de redirecionamento autorizados:**
```
https://seu-dominio.vercel.app/login/google/authorized
```

> **IMPORTANTE**: Substitua `seu-dominio.vercel.app` pelo seu domínio real do Vercel

### **2. Configure Variáveis de Ambiente no Vercel**

#### **Acesse o Dashboard do Vercel:**
1. Vá para: https://vercel.com/dashboard
2. Clique no seu projeto SaaS
3. Vá para "Settings" → "Environment Variables"

#### **Adicione as Variáveis:**
```
GOOGLE_CLIENT_ID = seu_client_id_do_google
GOOGLE_CLIENT_SECRET = sua_client_secret_do_google
```

#### **Configurações Adicionais:**
```
FLASK_ENV = production
FLASK_DEBUG = False
```

### **3. Faça Deploy no Vercel**

#### **Via Git (Recomendado):**
1. Faça commit das mudanças:
```bash
git add .
git commit -m "Add Google OAuth support"
git push origin main
```

2. O Vercel fará deploy automático

#### **Via Vercel CLI:**
```bash
vercel --prod
```

### **4. Teste a Integração**

#### **Após o Deploy:**
1. Acesse: `https://seu-dominio.vercel.app/login`
2. Clique em "Entrar com Google"
3. Teste a autenticação

## 🔧 **Arquivos Criados para Vercel**

### **vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "run.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "run.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### **requirements.txt**
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-OAuthlib==0.9.6
Werkzeug==2.3.7
python-dotenv==1.0.0
reportlab==4.0.4
openpyxl==3.1.2
pandas==2.0.3
requests==2.31.0
oauthlib==2.1.0
requests-oauthlib==1.1.0
cachelib==0.13.0
```

## 🎯 **URLs de Exemplo**

### **Desenvolvimento (Local):**
- Login: `http://localhost:5000/login`
- OAuth Callback: `http://localhost:5000/login/google/authorized`

### **Produção (Vercel):**
- Login: `https://seu-dominio.vercel.app/login`
- OAuth Callback: `https://seu-dominio.vercel.app/login/google/authorized`

## 🔒 **Configurações de Segurança**

### **Google Cloud Console:**
- ✅ URLs HTTPS obrigatórias
- ✅ Domínio verificado (se necessário)
- ✅ Escopo limitado (email, profile)

### **Vercel:**
- ✅ Variáveis de ambiente seguras
- ✅ HTTPS automático
- ✅ Domínio personalizado (opcional)

## 🛠️ **Solução de Problemas**

### **Erro "redirect_uri_mismatch":**
- Verifique se as URLs no Google Console estão corretas
- Confirme se está usando HTTPS
- Verifique se o domínio está correto

### **Erro "invalid_client":**
- Verifique se as variáveis de ambiente estão configuradas no Vercel
- Confirme se o CLIENT_ID está correto
- Reinicie o deploy no Vercel

### **Botão Google não aparece:**
- Verifique se as variáveis de ambiente estão configuradas
- Confirme se o deploy foi feito com sucesso
- Verifique os logs do Vercel

## 📞 **Suporte**

### **Logs do Vercel:**
1. Acesse o dashboard do Vercel
2. Vá para "Functions" → "View Function Logs"
3. Verifique se há erros relacionados ao Google OAuth

### **Teste Local vs Produção:**
- **Local**: Funciona com `http://localhost:5000`
- **Produção**: Deve usar `https://seu-dominio.vercel.app`

---

## 🎉 **Resultado Final**

Após a configuração:
- ✅ Google OAuth funcionando em produção
- ✅ URLs HTTPS seguras
- ✅ Variáveis de ambiente configuradas
- ✅ Sistema SaaS profissional com autenticação Google

**Tempo estimado**: 15-20 minutos
**Resultado**: Sistema SaaS com Google OAuth em produção!
