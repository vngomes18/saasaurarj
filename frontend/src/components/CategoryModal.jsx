import React, { useState, useEffect } from 'react'
import { X, AlertCircle, CheckCircle } from 'lucide-react'
import api from '../services/api'

function CategoryModal({ isOpen, onClose, onCategoryCreated, existingCategories = [] }) {
  const [categoryName, setCategoryName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Reset form when modal opens/closes
  useEffect(() => {
    if (isOpen) {
      setCategoryName('')
      setError('')
      setSuccess('')
    }
  }, [isOpen])

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!categoryName.trim()) {
      setError('Nome da categoria é obrigatório')
      return
    }

    // Verificar se já existe localmente (case-insensitive)
    const categoryExists = existingCategories.some(
      cat => cat.toLowerCase() === categoryName.trim().toLowerCase()
    )

    if (categoryExists) {
      setError(`A categoria "${categoryName.trim()}" já existe no sistema`)
      return
    }

    setIsLoading(true)
    setError('')
    setSuccess('')

    try {
      const response = await api.post('/categorias', {
        categoria: categoryName.trim()
      })

      if (response.data.success) {
        setSuccess(`Categoria "${categoryName.trim()}" criada com sucesso!`)
        setCategoryName('')
        
        // Callback para atualizar a lista de categorias
        if (onCategoryCreated) {
          onCategoryCreated(categoryName.trim())
        }
        
        // Fechar modal após 1.5 segundos
        setTimeout(() => {
          onClose()
        }, 1500)
      } else {
        setError(response.data.error || 'Erro ao criar categoria')
      }
    } catch (error) {
      console.error('Erro ao criar categoria:', error)
      if (error.response?.status === 409) {
        setError(error.response.data.error || 'Categoria já existe')
      } else {
        setError('Erro ao verificar categoria. Tente novamente.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleClose = () => {
    setCategoryName('')
    setError('')
    setSuccess('')
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Nova Categoria
          </h3>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nome da Categoria
            </label>
            <input
              type="text"
              value={categoryName}
              onChange={(e) => setCategoryName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Digite o nome da categoria"
              disabled={isLoading}
              autoFocus
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-center">
              <AlertCircle className="w-4 h-4 text-red-500 mr-2 flex-shrink-0" />
              <span className="text-sm text-red-700">{error}</span>
            </div>
          )}

          {/* Success Message */}
          {success && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md flex items-center">
              <CheckCircle className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
              <span className="text-sm text-green-700">{success}</span>
            </div>
          )}

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={handleClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
              disabled={isLoading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isLoading || !categoryName.trim()}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed rounded-md transition-colors flex items-center"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Verificando...
                </>
              ) : (
                'Criar Categoria'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CategoryModal
