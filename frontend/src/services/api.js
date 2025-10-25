import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para adicionar token se necessário
api.interceptors.request.use(
  (config) => {
    // Adicionar lógica de token se necessário
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para tratar respostas
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Redirecionar para login se não autenticado
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api


