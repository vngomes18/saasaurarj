import React, { useState } from 'react'
import { Users, Plus, Search, Edit, Trash2 } from 'lucide-react'
import { useClientes, useDeleteCliente } from '../hooks/useApi'

function Clientes() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: clientesData, isLoading: loading, error } = useClientes()
  const deleteClienteMutation = useDeleteCliente()

  const clientes = clientesData?.success ? clientesData.data : []

  const filteredClientes = clientes.filter(cliente =>
    cliente.nome.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteCliente = async (id) => {
    // Use the custom modal from the base template
    if (window.showConfirm) {
      window.showConfirm('Tem certeza que deseja excluir este cliente?', async () => {
        try {
          await deleteClienteMutation.mutateAsync(id)
        } catch (error) {
          console.error('Erro ao excluir cliente:', error)
        }
      })
    } else {
      // Fallback to native confirm if custom modal is not available
      if (window.confirm('Tem certeza que deseja excluir este cliente?')) {
        try {
          await deleteClienteMutation.mutateAsync(id)
        } catch (error) {
          console.error('Erro ao excluir cliente:', error)
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
        <p className="text-gray-500">Erro ao carregar clientes</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Users className="w-8 h-8 mr-3 text-blue-600" />
            Clientes
          </h1>
          <p className="text-gray-600">Gerencie sua base de clientes</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Novo Cliente
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar clientes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Clients Table */}
      <div className="card">
        {filteredClientes.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Endereço</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredClientes.map((cliente) => (
                  <tr key={cliente.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                          <span className="text-blue-600 font-medium">
                            {cliente.nome.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <h4 className="font-medium">{cliente.nome}</h4>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-gray-600">{cliente.email || '-'}</span>
                    </td>
                    <td>
                      <span className="text-gray-600">{cliente.telefone || '-'}</span>
                    </td>
                    <td>
                      <span className="text-gray-600">{cliente.endereco || '-'}</span>
                    </td>
                    <td>
                      <div className="flex space-x-2">
                        <button className="btn btn-secondary btn-sm">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteCliente(cliente.id)}
                          disabled={deleteClienteMutation.isPending}
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
            <Users className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhum cliente encontrado
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece adicionando seu primeiro cliente'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Adicionar Cliente
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Clientes

