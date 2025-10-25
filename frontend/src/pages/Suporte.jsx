import React, { useState } from 'react'
import { Headphones, Plus, Search, Eye, Edit, Trash2, Calendar, User, MessageSquare } from 'lucide-react'
import { useSuporte, useDeleteSuporte } from '../hooks/useApi'

function Suporte() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: suporteData, isLoading: loading, error } = useSuporte()
  const deleteSuporteMutation = useDeleteSuporte()

  const tickets = suporteData?.success ? suporteData.data : []

  const filteredTickets = tickets.filter(ticket =>
    ticket.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ticket.descricao?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    ticket.cliente_nome?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteTicket = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este ticket de suporte?')) {
      try {
        await deleteSuporteMutation.mutateAsync(id)
      } catch (error) {
        console.error('Erro ao excluir ticket:', error)
      }
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'aberto':
        return 'badge-warning'
      case 'em_andamento':
        return 'badge-info'
      case 'resolvido':
        return 'badge-success'
      case 'fechado':
        return 'badge-secondary'
      case 'cancelado':
        return 'badge-danger'
      default:
        return 'badge-secondary'
    }
  }

  const getPrioridadeBadge = (prioridade) => {
    switch (prioridade) {
      case 'alta':
        return 'badge-danger'
      case 'media':
        return 'badge-warning'
      case 'baixa':
        return 'badge-success'
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
        <p className="text-gray-500">Erro ao carregar tickets de suporte</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Headphones className="w-8 h-8 mr-3 text-blue-600" />
            Suporte
          </h1>
          <p className="text-gray-600">Gerencie tickets de suporte e atendimento</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Novo Ticket
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar tickets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Tickets Table */}
      <div className="card">
        {filteredTickets.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Ticket</th>
                  <th>Cliente</th>
                  <th>Assunto</th>
                  <th>Data</th>
                  <th>Status</th>
                  <th>Prioridade</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredTickets.map((ticket) => (
                  <tr key={ticket.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                          <Headphones className="w-5 h-5 text-purple-600" />
                        </div>
                        <div>
                          <h4 className="font-medium">#{ticket.id}</h4>
                          <p className="text-sm text-gray-500">
                            {ticket.categoria || 'Geral'}
                          </p>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center">
                        <User className="w-4 h-4 mr-2 text-gray-400" />
                        <span className="text-gray-600">{ticket.cliente_nome || '-'}</span>
                      </div>
                    </td>
                    <td>
                      <div>
                        <h4 className="font-medium">{ticket.titulo}</h4>
                        {ticket.descricao && (
                          <p className="text-sm text-gray-500 truncate max-w-xs">
                            {ticket.descricao}
                          </p>
                        )}
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="w-4 h-4 mr-2" />
                        {new Date(ticket.data_criacao).toLocaleDateString('pt-BR')}
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${getStatusBadge(ticket.status)}`}>
                        {ticket.status}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${getPrioridadeBadge(ticket.prioridade)}`}>
                        {ticket.prioridade}
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
                          onClick={() => handleDeleteTicket(ticket.id)}
                          disabled={deleteSuporteMutation.isPending}
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
            <Headphones className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhum ticket encontrado
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece criando seu primeiro ticket'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Criar Ticket
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Suporte

