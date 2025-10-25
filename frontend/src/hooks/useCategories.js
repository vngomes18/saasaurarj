import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/api'

// Query Keys
export const categoryKeys = {
  all: ['categories'],
  list: () => [...categoryKeys.all, 'list'],
}

// Hook para buscar categorias
export const useCategories = () => {
  return useQuery({
    queryKey: categoryKeys.list(),
    queryFn: async () => {
      const response = await api.get('/categorias')
      return response.data
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  })
}

// Hook para criar categoria
export const useCreateCategory = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (categoryData) => {
      const response = await api.post('/categorias', categoryData)
      return response.data
    },
    onSuccess: () => {
      // Invalidar cache de categorias
      queryClient.invalidateQueries({ queryKey: categoryKeys.all })
    },
  })
}

// Hook para verificar se categoria existe
export const useCheckCategory = () => {
  return useMutation({
    mutationFn: async (categoryName) => {
      const response = await api.post('/categorias', { categoria: categoryName })
      return response.data
    },
  })
}
