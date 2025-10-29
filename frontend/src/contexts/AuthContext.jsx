import React, { createContext, useContext } from 'react'
import { useAuth as useAuthQuery, useLogin as useLoginMutation, useLogout as useLogoutMutation } from '../hooks/useApi'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const { data: authData, isLoading: loading, error } = useAuthQuery()
  const loginMutation = useLoginMutation()
  const logoutMutation = useLogoutMutation()

  const user = authData?.success ? authData.data : null

  const login = async (credentials) => {
    try {
      const result = await loginMutation.mutateAsync(credentials)
      return { success: result.success, error: result.error }
    } catch (error) {
      return { success: false, error: 'Erro ao fazer login' }
    }
  }

  const logout = async () => {
    try {
      await logoutMutation.mutateAsync()
    } catch (error) {
      console.error('Erro ao fazer logout:', error)
    }
  }

  const value = {
    user,
    loading: loading || loginMutation.isPending || logoutMutation.isPending,
    login,
    logout,
    checkAuth: () => {}, // Não é mais necessário com TanStack Query
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider')
  }
  return context
}

