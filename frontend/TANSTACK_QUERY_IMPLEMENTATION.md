# Implementação do TanStack Query

Este documento descreve a implementação do TanStack Query no sistema React do SaaS.

## O que foi implementado

### 1. Dependências Adicionadas
- `@tanstack/react-query`: ^5.0.0
- `@tanstack/react-query-devtools`: ^5.0.0

### 2. Configuração do QueryClient
- Configurado no `App.jsx` com opções otimizadas
- Cache de 5 minutos para queries
- Retry automático configurado
- DevTools habilitado para desenvolvimento

### 3. Hooks Customizados (`src/hooks/useApi.js`)
Criados hooks para todas as operações CRUD:

#### Autenticação
- `useAuth()` - Verificar autenticação
- `useLogin()` - Fazer login
- `useLogout()` - Fazer logout

#### Dashboard
- `useDashboard()` - Dados do dashboard

#### Produtos
- `useProdutos()` - Listar produtos
- `useProduto(id)` - Produto específico
- `useCreateProduto()` - Criar produto
- `useUpdateProduto()` - Atualizar produto
- `useDeleteProduto()` - Deletar produto

#### Clientes
- `useClientes()` - Listar clientes
- `useCliente(id)` - Cliente específico
- `useCreateCliente()` - Criar cliente
- `useUpdateCliente()` - Atualizar cliente
- `useDeleteCliente()` - Deletar cliente

#### Vendas
- `useVendas()` - Listar vendas
- `useVenda(id)` - Venda específica
- `useCreateVenda()` - Criar venda
- `useUpdateVenda()` - Atualizar venda
- `useDeleteVenda()` - Deletar venda

#### Fornecedores
- `useFornecedores()` - Listar fornecedores
- `useCreateFornecedor()` - Criar fornecedor
- `useUpdateFornecedor()` - Atualizar fornecedor
- `useDeleteFornecedor()` - Deletar fornecedor

### 4. Componentes Atualizados

#### AuthContext
- Migrado para usar TanStack Query
- Removido estado manual de loading
- Integração com hooks de autenticação

#### Dashboard
- Usa `useDashboard()` hook
- Cache automático de dados
- Loading e error states gerenciados automaticamente

#### Páginas (Produtos, Clientes, Vendas)
- Migradas para usar hooks do TanStack Query
- Funcionalidade de delete implementada
- Loading states otimizados
- Error handling melhorado

## Benefícios da Implementação

### 1. Cache Inteligente
- Dados são cacheados automaticamente
- Evita requisições desnecessárias
- Sincronização automática entre componentes

### 2. Gerenciamento de Estado
- Loading states automáticos
- Error handling centralizado
- Estados de pending para mutations

### 3. Invalidação Automática
- Cache é invalidado automaticamente após mutations
- Dados são atualizados em tempo real
- Sincronização entre diferentes views

### 4. Otimizações
- Background refetch
- Stale time configurado
- Retry automático em caso de erro
- DevTools para debugging

### 5. Experiência do Desenvolvedor
- Hooks reutilizáveis
- TypeScript support
- DevTools integrado
- Código mais limpo e organizado

## Como usar

### Exemplo básico de query:
```javascript
import { useProdutos } from '../hooks/useApi'

function ProdutosPage() {
  const { data, isLoading, error } = useProdutos()
  
  if (isLoading) return <Loading />
  if (error) return <Error />
  
  return <ProdutosList data={data} />
}
```

### Exemplo de mutation:
```javascript
import { useCreateProduto } from '../hooks/useApi'

function CreateProdutoForm() {
  const createProduto = useCreateProduto()
  
  const handleSubmit = async (formData) => {
    try {
      await createProduto.mutateAsync(formData)
      // Cache será invalidado automaticamente
    } catch (error) {
      console.error('Erro ao criar produto:', error)
    }
  }
}
```

## Próximos Passos

1. **Formulários**: Implementar formulários de criação/edição usando os hooks de mutation
2. **Otimistic Updates**: Implementar atualizações otimistas para melhor UX
3. **Infinite Queries**: Para listas grandes, implementar paginação infinita
4. **Prefetching**: Implementar prefetch de dados para navegação mais rápida
5. **Offline Support**: Configurar persistência de cache para funcionamento offline

## Comandos para instalar

```bash
cd frontend
npm install @tanstack/react-query @tanstack/react-query-devtools
```

## DevTools

O React Query DevTools está habilitado em desenvolvimento. Para acessar:
1. Abra o DevTools do navegador
2. Procure pela aba "React Query"
3. Visualize queries, cache e mutations em tempo real

