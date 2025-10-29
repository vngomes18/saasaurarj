import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/api'

// Query Keys
export const queryKeys = {
  auth: ['auth'],
  dashboard: ['dashboard'],
  produtos: ['produtos'],
  clientes: ['clientes'],
  vendas: ['vendas'],
  fornecedores: ['fornecedores'],
  compras: ['compras'],
  produtos_auxiliares: ['produtos_auxiliares'],
  cupons: ['cupons'],
  notas_fiscais: ['notas_fiscais'],
  suporte: ['suporte'],
  relatorios: ['relatorios'],
  categorias: ['categorias'],
}

// Auth Hooks
export const useAuth = () => {
  return useQuery({
    queryKey: queryKeys.auth,
    queryFn: async () => {
      const response = await api.get('/auth/me')
      return response.data
    },
    retry: false,
    staleTime: Infinity,
  })
}

export const useLogin = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (credentials) => {
      const response = await api.post('/login', credentials)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.auth })
    },
  })
}

export const useLogout = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async () => {
      const response = await api.post('/logout')
      return response.data
    },
    onSuccess: () => {
      queryClient.setQueryData(queryKeys.auth, null)
    },
  })
}

// Dashboard Hooks
export const useDashboard = () => {
  return useQuery({
    queryKey: queryKeys.dashboard,
    queryFn: async () => {
      const response = await api.get('/dashboard')
      return response.data
    },
    staleTime: 2 * 60 * 1000, // 2 minutos
  })
}

// Produtos Hooks
export const useProdutos = () => {
  return useQuery({
    queryKey: queryKeys.produtos,
    queryFn: async () => {
      const response = await api.get('/produtos')
      return response.data
    },
  })
}

export const useProduto = (id) => {
  return useQuery({
    queryKey: [...queryKeys.produtos, id],
    queryFn: async () => {
      const response = await api.get(`/produtos/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateProduto = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (produto) => {
      const response = await api.post('/produtos', produto)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useUpdateProduto = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...produto }) => {
      const response = await api.put(`/produtos/${id}`, produto)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.produtos, variables.id] })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useDeleteProduto = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/produtos/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

// Clientes Hooks
export const useClientes = () => {
  return useQuery({
    queryKey: queryKeys.clientes,
    queryFn: async () => {
      const response = await api.get('/clientes')
      return response.data
    },
  })
}

export const useCliente = (id) => {
  return useQuery({
    queryKey: [...queryKeys.clientes, id],
    queryFn: async () => {
      const response = await api.get(`/clientes/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateCliente = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (cliente) => {
      const response = await api.post('/clientes', cliente)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.clientes })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useUpdateCliente = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...cliente }) => {
      const response = await api.put(`/clientes/${id}`, cliente)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.clientes })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.clientes, variables.id] })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useDeleteCliente = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/clientes/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.clientes })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

// Vendas Hooks
export const useVendas = () => {
  return useQuery({
    queryKey: queryKeys.vendas,
    queryFn: async () => {
      const response = await api.get('/vendas')
      return response.data
    },
  })
}

export const useVenda = (id) => {
  return useQuery({
    queryKey: [...queryKeys.vendas, id],
    queryFn: async () => {
      const response = await api.get(`/vendas/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateVenda = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (venda) => {
      const response = await api.post('/vendas', venda)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.vendas })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
    },
  })
}

export const useUpdateVenda = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...venda }) => {
      const response = await api.put(`/vendas/${id}`, venda)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.vendas })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.vendas, variables.id] })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
    },
  })
}

export const useDeleteVenda = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/vendas/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.vendas })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
    },
  })
}

// Fornecedores Hooks
export const useFornecedores = () => {
  return useQuery({
    queryKey: queryKeys.fornecedores,
    queryFn: async () => {
      const response = await api.get('/fornecedores')
      return response.data
    },
  })
}

export const useCreateFornecedor = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (fornecedor) => {
      const response = await api.post('/fornecedores', fornecedor)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.fornecedores })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useUpdateFornecedor = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...fornecedor }) => {
      const response = await api.put(`/fornecedores/${id}`, fornecedor)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.fornecedores })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.fornecedores, variables.id] })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useDeleteFornecedor = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/fornecedores/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.fornecedores })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

// Compras Hooks
export const useCompras = () => {
  return useQuery({
    queryKey: queryKeys.compras,
    queryFn: async () => {
      const response = await api.get('/compras')
      return response.data
    },
  })
}

export const useCompra = (id) => {
  return useQuery({
    queryKey: [...queryKeys.compras, id],
    queryFn: async () => {
      const response = await api.get(`/compras/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateCompra = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (compra) => {
      const response = await api.post('/compras', compra)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.compras })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
    },
  })
}

export const useUpdateCompra = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...compra }) => {
      const response = await api.put(`/compras/${id}`, compra)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.compras })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.compras, variables.id] })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
    },
  })
}

export const useDeleteCompra = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/compras/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.compras })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos })
    },
  })
}

// Produtos Auxiliares Hooks
export const useProdutosAuxiliares = () => {
  return useQuery({
    queryKey: queryKeys.produtos_auxiliares,
    queryFn: async () => {
      const response = await api.get('/produtos-auxiliares')
      return response.data
    },
  })
}

export const useProdutoAuxiliar = (id) => {
  return useQuery({
    queryKey: [...queryKeys.produtos_auxiliares, id],
    queryFn: async () => {
      const response = await api.get(`/produtos-auxiliares/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateProdutoAuxiliar = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (produto) => {
      const response = await api.post('/produtos-auxiliares', produto)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos_auxiliares })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useUpdateProdutoAuxiliar = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...produto }) => {
      const response = await api.put(`/produtos-auxiliares/${id}`, produto)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos_auxiliares })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.produtos_auxiliares, variables.id] })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

export const useDeleteProdutoAuxiliar = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/produtos-auxiliares/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.produtos_auxiliares })
      queryClient.invalidateQueries({ queryKey: queryKeys.dashboard })
    },
  })
}

// Cupons Hooks
export const useCupons = () => {
  return useQuery({
    queryKey: queryKeys.cupons,
    queryFn: async () => {
      const response = await api.get('/cupons')
      return response.data
    },
  })
}

export const useCupom = (id) => {
  return useQuery({
    queryKey: [...queryKeys.cupons, id],
    queryFn: async () => {
      const response = await api.get(`/cupons/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateCupom = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (cupom) => {
      const response = await api.post('/cupons', cupom)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.cupons })
    },
  })
}

export const useUpdateCupom = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...cupom }) => {
      const response = await api.put(`/cupons/${id}`, cupom)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.cupons })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.cupons, variables.id] })
    },
  })
}

export const useDeleteCupom = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/cupons/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.cupons })
    },
  })
}

// Notas Fiscais Hooks
export const useNotasFiscais = () => {
  return useQuery({
    queryKey: queryKeys.notas_fiscais,
    queryFn: async () => {
      const response = await api.get('/notas-fiscais')
      return response.data
    },
  })
}

export const useNotaFiscal = (id) => {
  return useQuery({
    queryKey: [...queryKeys.notas_fiscais, id],
    queryFn: async () => {
      const response = await api.get(`/notas-fiscais/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateNotaFiscal = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (nota) => {
      const response = await api.post('/notas-fiscais', nota)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.notas_fiscais })
    },
  })
}

export const useUpdateNotaFiscal = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...nota }) => {
      const response = await api.put(`/notas-fiscais/${id}`, nota)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.notas_fiscais })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.notas_fiscais, variables.id] })
    },
  })
}

export const useDeleteNotaFiscal = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/notas-fiscais/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.notas_fiscais })
    },
  })
}

// Suporte Hooks
export const useSuporte = () => {
  return useQuery({
    queryKey: queryKeys.suporte,
    queryFn: async () => {
      const response = await api.get('/suporte')
      return response.data
    },
  })
}

export const useSuporteTicket = (id) => {
  return useQuery({
    queryKey: [...queryKeys.suporte, id],
    queryFn: async () => {
      const response = await api.get(`/suporte/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateSuporte = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (ticket) => {
      const response = await api.post('/suporte', ticket)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.suporte })
    },
  })
}

export const useUpdateSuporte = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...ticket }) => {
      const response = await api.put(`/suporte/${id}`, ticket)
      return response.data
    },
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.suporte })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.suporte, variables.id] })
    },
  })
}

export const useDeleteSuporte = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id) => {
      const response = await api.delete(`/suporte/${id}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.suporte })
    },
  })
}

// Relatórios Hooks
export const useRelatorios = () => {
  return useQuery({
    queryKey: queryKeys.relatorios,
    queryFn: async () => {
      const response = await api.get('/relatorios')
      return response.data
    },
  })
}

export const useRelatorioFluxoCaixa = () => {
  return useQuery({
    queryKey: [...queryKeys.relatorios, 'fluxo-caixa'],
    queryFn: async () => {
      const response = await api.get('/relatorios/fluxo-caixa')
      return response.data
    },
  })
}

export const useRelatorioPL = () => {
  return useQuery({
    queryKey: [...queryKeys.relatorios, 'pl'],
    queryFn: async () => {
      const response = await api.get('/relatorios/pl')
      return response.data
    },
  })
}

export const useRelatorioTopProdutos = () => {
  return useQuery({
    queryKey: [...queryKeys.relatorios, 'top-produtos'],
    queryFn: async () => {
      const response = await api.get('/relatorios/top-produtos')
      return response.data
    },
  })
}

export const useRelatorioProdutosParados = () => {
  return useQuery({
    queryKey: [...queryKeys.relatorios, 'produtos-parados'],
    queryFn: async () => {
      const response = await api.get('/relatorios/produtos-parados')
      return response.data
    },
  })
}

export const useRelatorioRotatividade = () => {
  return useQuery({
    queryKey: [...queryKeys.relatorios, 'rotatividade'],
    queryFn: async () => {
      const response = await api.get('/relatorios/rotatividade')
      return response.data
    },
  })
}

export const useRelatorioSazonalidade = () => {
  return useQuery({
    queryKey: [...queryKeys.relatorios, 'sazonalidade'],
    queryFn: async () => {
      const response = await api.get('/relatorios/sazonalidade')
      return response.data
    },
  })
}

// Categorias Hooks
export const useCategories = () => {
  return useQuery({
    queryKey: queryKeys.categorias,
    queryFn: async () => {
      const response = await api.get('/categorias')
      return response.data
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  })
}

export const useCreateCategory = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (categoryData) => {
      const response = await api.post('/categorias', categoryData)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.categorias })
    },
  })
}

export const useCheckCategory = () => {
  return useMutation({
    mutationFn: async (categoryName) => {
      const response = await api.post('/categorias', { categoria: categoryName })
      return response.data
    },
  })
}
