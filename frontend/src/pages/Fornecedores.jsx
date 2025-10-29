import React, { useState } from 'react'
import { Truck, Plus, Search, Edit, Trash2, Phone, Mail, MapPin } from 'lucide-react'
import { useFornecedores, useDeleteFornecedor } from '../hooks/useApi'

function Fornecedores() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: fornecedoresData, isLoading: loading, error } = useFornecedores()
  const deleteFornecedorMutation = useDeleteFornecedor()

  const fornecedores = fornecedoresData?.success ? fornecedoresData.data : []

  const filteredFornecedores = fornecedores.filter(fornecedor =>
    fornecedor.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    fornecedor.empresa?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteFornecedor = async (id) => {
    // Use the custom modal from the base template
    if (window.showConfirm) {
      window.showConfirm('Tem certeza que deseja excluir este fornecedor?', async () => {
        try {
          await deleteFornecedorMutation.mutateAsync(id)
        } catch (error) {
          console.error('Erro ao excluir fornecedor:', error)
        }
      })
    } else {
      // Fallback to native confirm if custom modal is not available
      if (window.confirm('Tem certeza que deseja excluir este fornecedor?')) {
        try {
          await deleteFornecedorMutation.mutateAsync(id)
        } catch (error) {
          console.error('Erro ao excluir fornecedor:', error)
        }
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Erro ao carregar fornecedores</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Truck className="w-8 h-8 mr-3 text-blue-600" />
            Fornecedores
          </h1>
          <p className="text-gray-600">Gerencie seus fornecedores e parceiros</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Novo Fornecedor
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar fornecedores..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Fornecedores Table */}
      <div className="card">
        {filteredFornecedores.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Fornecedor</th>
                  <th>Empresa</th>
                  <th>Contato</th>
                  <th>Endereço</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredFornecedores.map((fornecedor) => (
                  <tr key={fornecedor.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center mr-3">
                          <Truck className="w-5 h-5 text-orange-600" />
                        </div>
                        <div>
                          <h4 className="font-medium">{fornecedor.nome}</h4>
                          {fornecedor.cargo && (
                            <p className="text-sm text-gray-500">{fornecedor.cargo}</p>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-gray-600">{fornecedor.empresa || '-'}</span>
                    </td>
                    <td>
                      <div className="space-y-1">
                        {fornecedor.telefone && (
                          <div className="flex items-center text-sm text-gray-600">
                            <Phone className="w-4 h-4 mr-2" />
                            {fornecedor.telefone}
                          </div>
                        )}
                        {fornecedor.email && (
                          <div className="flex items-center text-sm text-gray-600">
                            <Mail className="w-4 h-4 mr-2" />
                            {fornecedor.email}
                          </div>
                        )}
                      </div>
                    </td>
                    <td>
                      {fornecedor.endereco ? (
                        <div className="flex items-center text-sm text-gray-600">
                          <MapPin className="w-4 h-4 mr-2" />
                          {fornecedor.endereco}
                        </div>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </td>
                    <td>
                      <span className={`badge ${
                        fornecedor.ativo ? 'badge-success' : 'badge-secondary'
                      }`}>
                        {fornecedor.ativo ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td>
                      <div className="flex space-x-2">
                        <button className="btn btn-secondary btn-sm">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteFornecedor(fornecedor.id)}
                          disabled={deleteFornecedorMutation.isPending}
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <Truck className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhum fornecedor encontrado
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece adicionando seu primeiro fornecedor'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Adicionar Fornecedor
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Fornecedores

