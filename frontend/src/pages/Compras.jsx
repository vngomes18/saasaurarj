import React, { useState } from 'react'
import { ShoppingBag, Plus, Search, Eye, Edit, Trash2, Calendar, DollarSign } from 'lucide-react'
import { useCompras, useDeleteCompra } from '../hooks/useApi'

function Compras() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: comprasData, isLoading: loading, error } = useCompras()
  const deleteCompraMutation = useDeleteCompra()

  const compras = comprasData?.success ? comprasData.data : []

  const filteredCompras = compras.filter(compra =>
    compra.fornecedor_nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    compra.numero_pedido?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteCompra = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta compra?')) {
      try {
        await deleteCompraMutation.mutateAsync(id)
      } catch (error) {
        console.error('Erro ao excluir compra:', error)
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
      case 'em_transito':
        return 'badge-info'
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
        <p className="text-gray-500">Erro ao carregar compras</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <ShoppingBag className="w-8 h-8 mr-3 text-blue-600" />
            Compras
          </h1>
          <p className="text-gray-600">Gerencie suas compras e pedidos</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Nova Compra
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar compras..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Compras Table */}
      <div className="card">
        {filteredCompras.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Pedido</th>
                  <th>Fornecedor</th>
                  <th>Data</th>
                  <th>Total</th>
                  <th>Status</th>
                  <th>Forma Pagamento</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredCompras.map((compra) => (
                  <tr key={compra.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                          <ShoppingBag className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="font-medium">#{compra.numero_pedido || compra.id}</h4>
                          {compra.observacoes && (
                            <p className="text-sm text-gray-500">{compra.observacoes}</p>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-gray-600">{compra.fornecedor_nome || '-'}</span>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="w-4 h-4 mr-2" />
                        {new Date(compra.data_compra).toLocaleDateString('pt-BR')}
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <DollarSign className="w-4 h-4 mr-2" />
                        <span className="font-semibold text-blue-600">
                          R$ {compra.total.toFixed(2)}
                        </span>
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${getStatusBadge(compra.status)}`}>
                        {compra.status}
                      </span>
                    </td>
                    <td>
                      <span className="text-gray-600">{compra.forma_pagamento || '-'}</span>
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
                          onClick={() => handleDeleteCompra(compra.id)}
                          disabled={deleteCompraMutation.isPending}
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
            <ShoppingBag className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma compra encontrada
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece registrando sua primeira compra'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Nova Compra
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Compras

