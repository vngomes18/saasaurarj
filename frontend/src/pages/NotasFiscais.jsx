import React, { useState } from 'react'
import { FileText, Plus, Search, Eye, Edit, Trash2, Calendar, DollarSign, Hash } from 'lucide-react'
import { useNotasFiscais, useDeleteNotaFiscal } from '../hooks/useApi'

function NotasFiscais() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: notasData, isLoading: loading, error } = useNotasFiscais()
  const deleteNotaMutation = useDeleteNotaFiscal()

  const notas = notasData?.success ? notasData.data : []

  const filteredNotas = notas.filter(nota =>
    nota.numero?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    nota.cliente_nome?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteNota = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta nota fiscal?')) {
      try {
        await deleteNotaMutation.mutateAsync(id)
      } catch (error) {
        console.error('Erro ao excluir nota fiscal:', error)
      }
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'emitida':
        return 'badge-success'
      case 'pendente':
        return 'badge-warning'
      case 'cancelada':
        return 'badge-danger'
      case 'processando':
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
        <p className="text-gray-500">Erro ao carregar notas fiscais</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <FileText className="w-8 h-8 mr-3 text-blue-600" />
            Notas Fiscais
          </h1>
          <p className="text-gray-600">Gerencie notas fiscais e documentos fiscais</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Nova Nota Fiscal
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar notas fiscais..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Notas Fiscais Table */}
      <div className="card">
        {filteredNotas.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Nota Fiscal</th>
                  <th>Cliente</th>
                  <th>Data Emissão</th>
                  <th>Valor</th>
                  <th>Status</th>
                  <th>Tipo</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredNotas.map((nota) => (
                  <tr key={nota.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                          <FileText className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="font-medium font-mono">#{nota.numero}</h4>
                          {nota.serie && (
                            <p className="text-sm text-gray-500">Série: {nota.serie}</p>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-gray-600">{nota.cliente_nome || '-'}</span>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="w-4 h-4 mr-2" />
                        {new Date(nota.data_emissao).toLocaleDateString('pt-BR')}
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <DollarSign className="w-4 h-4 mr-2" />
                        <span className="font-semibold text-green-600">
                          R$ {nota.valor_total.toFixed(2)}
                        </span>
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${getStatusBadge(nota.status)}`}>
                        {nota.status}
                      </span>
                    </td>
                    <td>
                      <span className="badge badge-info">
                        {nota.tipo || 'NFe'}
                      </span>
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
                          onClick={() => handleDeleteNota(nota.id)}
                          disabled={deleteNotaMutation.isPending}
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
            <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma nota fiscal encontrada
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece emitindo sua primeira nota fiscal'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Emitir Nota Fiscal
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default NotasFiscais

