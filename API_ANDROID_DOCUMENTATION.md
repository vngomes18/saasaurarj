# 📱 API Documentation - Android Integration

## 🔑 **Autenticação**

### **Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

**Resposta de Sucesso:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@exemplo.com",
    "empresa": "Minha Empresa",
    "role": "user",
    "two_factor_enabled": false
  }
}
```

**Resposta com 2FA:**
```json
{
  "error": "2FA required",
  "requires_2fa": true,
  "user_id": 1
}
```

### **Verificação 2FA**
```http
POST /api/auth/verify-2fa
Content-Type: application/json

{
  "user_id": 1,
  "token": "123456"
}
```

### **Refresh Token**
```http
POST /api/auth/refresh
Authorization: Bearer {refresh_token}
```

### **Logout**
```http
POST /api/auth/logout
Authorization: Bearer {access_token}
```

---

## 📦 **Produtos**

### **Listar Produtos**
```http
GET /api/produtos?page=1&per_page=20&search=termo&categoria=categoria
Authorization: Bearer {access_token}
```

**Resposta:**
```json
{
  "produtos": [
    {
      "id": 1,
      "nome": "Produto Exemplo",
      "descricao": "Descrição do produto",
      "preco": 29.99,
      "estoque_atual": 50,
      "estoque_minimo": 10,
      "categoria": "Eletrônicos",
      "codigo_barras": "123456789",
      "created_at": "2024-01-01T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

### **Criar Produto**
```http
POST /api/produtos
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Novo Produto",
  "descricao": "Descrição do produto",
  "preco": 29.99,
  "estoque_atual": 50,
  "estoque_minimo": 10,
  "categoria": "Eletrônicos",
  "codigo_barras": "123456789"
}
```

### **Buscar Produto por ID**
```http
GET /api/produtos/{id}
Authorization: Bearer {access_token}
```

### **Atualizar Produto**
```http
PUT /api/produtos/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Produto Atualizado",
  "preco": 39.99,
  "estoque_atual": 75
}
```

### **Deletar Produto**
```http
DELETE /api/produtos/{id}
Authorization: Bearer {access_token}
```

---

## 👥 **Clientes**

### **Listar Clientes**
```http
GET /api/clientes?page=1&per_page=20&search=termo
Authorization: Bearer {access_token}
```

### **Criar Cliente**
```http
POST /api/clientes
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@exemplo.com",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua das Flores, 123",
  "cidade": "São Paulo",
  "estado": "SP",
  "cep": "01234-567"
}
```

### **Buscar Cliente por ID**
```http
GET /api/clientes/{id}
Authorization: Bearer {access_token}
```

### **Atualizar Cliente**
```http
PUT /api/clientes/{id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "João Silva Santos",
  "telefone": "(11) 88888-8888"
}
```

### **Deletar Cliente**
```http
DELETE /api/clientes/{id}
Authorization: Bearer {access_token}
```

---

## 📊 **Dashboard**

### **KPIs do Dashboard**
```http
GET /api/dashboard-kpis
Authorization: Bearer {access_token}
```

**Resposta:**
```json
{
  "receita_atual": 15000.00,
  "receita_anterior": 12000.00,
  "crescimento": 25.0,
  "total_produtos": 150,
  "total_clientes": 45,
  "vendas_hoje": 8,
  "produtos_estoque_baixo": 12
}
```

---

## 🏷️ **Categorias**

### **Listar Categorias**
```http
GET /api/categorias
Authorization: Bearer {access_token}
```

### **Criar Categoria**
```http
POST /api/categorias
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Nova Categoria"
}
```

---

## 🔧 **Configurações**

### **Toggle Dark Mode**
```http
POST /api/toggle-dark-mode
Authorization: Bearer {access_token}
```

---

## 📱 **Headers Obrigatórios**

```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

---

## ⚠️ **Códigos de Erro**

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Dados inválidos |
| 401 | Não autorizado |
| 403 | Acesso negado |
| 404 | Recurso não encontrado |
| 423 | Conta bloqueada |
| 500 | Erro interno do servidor |

---

## 🔄 **Rate Limiting**

- **Login**: 10 tentativas por minuto
- **2FA**: 10 tentativas por minuto
- **API Geral**: 200 requisições por dia, 50 por hora

---

## 📱 **Exemplo de Implementação Android**

### **Classe de Autenticação**
```kotlin
class AuthManager {
    private val apiService = ApiService()
    private val prefs = SharedPreferences.getInstance()
    
    fun login(email: String, password: String, callback: (AuthResult) -> Unit) {
        apiService.login(email, password) { response ->
            if (response.isSuccessful) {
                val authData = response.body()
                prefs.saveToken(authData.access_token)
                prefs.saveRefreshToken(authData.refresh_token)
                callback(AuthResult.Success(authData.user))
            } else {
                callback(AuthResult.Error(response.message()))
            }
        }
    }
    
    fun refreshToken(callback: (Boolean) -> Unit) {
        val refreshToken = prefs.getRefreshToken()
        apiService.refreshToken(refreshToken) { response ->
            if (response.isSuccessful) {
                val newToken = response.body().access_token
                prefs.saveToken(newToken)
                callback(true)
            } else {
                callback(false)
            }
        }
    }
}
```

### **Classe de Produtos**
```kotlin
class ProductRepository {
    private val apiService = ApiService()
    
    fun getProducts(page: Int = 1, perPage: Int = 20, callback: (ProductListResponse) -> Unit) {
        apiService.getProducts(page, perPage) { response ->
            if (response.isSuccessful) {
                callback(ProductListResponse.Success(response.body()))
            } else {
                callback(ProductListResponse.Error(response.message()))
            }
        }
    }
    
    fun createProduct(product: Product, callback: (ProductResponse) -> Unit) {
        apiService.createProduct(product) { response ->
            if (response.isSuccessful) {
                callback(ProductResponse.Success(response.body()))
            } else {
                callback(ProductResponse.Error(response.message()))
            }
        }
    }
}
```

---

## 🚀 **Próximas Implementações**

### **Endpoints Planejados:**
- `/api/vendas` - CRUD completo de vendas
- `/api/compras` - CRUD completo de compras
- `/api/fornecedores` - CRUD completo de fornecedores
- `/api/upload` - Upload de imagens
- `/api/sync` - Sincronização offline
- `/api/notifications` - Push notifications

### **Funcionalidades Planejadas:**
- **Offline Sync**: Sincronização automática quando voltar online
- **Push Notifications**: Notificações em tempo real
- **Image Upload**: Upload de fotos de produtos
- **Barcode Scanner**: Integração com scanner de código de barras
- **Export Data**: Exportação de dados para CSV/PDF

---

**✅ Status**: API Base Implementada  
**📅 Data**: $(date)  
**👨‍💻 Desenvolvido por**: Sistema SaaS  
**🔧 Versão**: 1.0  
**📱 Compatível com**: Android, iOS, Web
