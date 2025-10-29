import React, { useState } from 'react'
import { ShoppingCart, Plus, Search, Eye, Edit, Trash2 } from 'lucide-react'
import { useVendas, useDeleteVenda } from '../hooks/useApi'

function Vendas() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: vendasData, isLoading: loading, error } = useVendas()
  const deleteVendaMutation = useDeleteVenda()

  const vendas = vendasData?.success ? vendasData.data : []

  const filteredVendas = vendas.filter(venda =>
    venda.cliente_nome.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteVenda = async (id) => {
    // Use the custom modal from the base template
    if (window.showConfirm) {
      window.showConfirm('Tem certeza que deseja excluir esta venda?', async () => {
        try {
          await deleteVendaMutation.mutateAsync(id)
        } catch (error) {
          console.error('Erro ao excluir venda:', error)
        }
      })
    } else {
      // Fallback to native confirm if custom modal is not available
      if (window.confirm('Tem certeza que deseja excluir esta venda?')) {
        try {
          await deleteVendaMutation.mutateAsync(id)
        } catch (error) {
          console.error('Erro ao excluir venda:', error)
        }
      }
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'concluida':
        return 'badge-success'
      case 'pendente':
        return 'badge-warning'
      case 'cancelada':
        return 'badge-danger'
      default:
        return 'badge-secondary'
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
        <p className="text-gray-500">Erro ao carregar vendas</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <ShoppingCart className="w-8 h-8 mr-3 text-blue-600" />
            Vendas
          </h1>
          <p className="text-gray-600">Gerencie suas vendas e transações</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Nova Venda
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar vendas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Sales Table */}
      <div className="card">
        {filteredVendas.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Data</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Pagamento</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredVendas.map((venda) => (
                  <tr key={venda.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
                          <span className="text-green-600 font-medium">
                            {venda.cliente_nome.charAt(0).toUpperCase()}
                          </span>
                        </div>
                        <div>
                          <h4 className="font-medium">{venda.cliente_nome}</h4>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-gray-600">
                        {new Date(venda.data_venda).toLocaleDateString('pt-BR')}
                      </span>
                    </td>
                    <td>
                      <span className="font-semibold text-green-600">
                        R$ {venda.total.toFixed(2)}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${getStatusBadge(venda.status)}`}>
                        {venda.status}
                      </span>
                    </td>
                    <td>
                      <span className="text-gray-600">{venda.forma_pagamento || '-'}</span>
                    </td>
                    <td>
                      <div className="flex space-x-2">
                        <button className="btn btn-secondary btn-sm">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="btn btn-primary btn-sm">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteVenda(venda.id)}
                          disabled={deleteVendaMutation.isPending}
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
            <ShoppingCart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma venda encontrada
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece registrando sua primeira venda'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Nova Venda
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Vendas

