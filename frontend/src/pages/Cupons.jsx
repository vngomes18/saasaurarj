import React, { useState } from 'react'
import { Tag, Plus, Search, Edit, Trash2, Calendar, Percent, Users } from 'lucide-react'
import { useCupons, useDeleteCupom } from '../hooks/useApi'

function Cupons() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: cuponsData, isLoading: loading, error } = useCupons()
  const deleteCupomMutation = useDeleteCupom()

  const cupons = cuponsData?.success ? cuponsData.data : []

  const filteredCupons = cupons.filter(cupom =>
    cupom.codigo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cupom.descricao?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteCupom = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este cupom?')) {
      try {
        await deleteCupomMutation.mutateAsync(id)
      } catch (error) {
        console.error('Erro ao excluir cupom:', error)
      }
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'ativo':
        return 'badge-success'
      case 'inativo':
        return 'badge-secondary'
      case 'expirado':
        return 'badge-danger'
      case 'usado':
        return 'badge-warning'
      default:
        return 'badge-secondary'
    }
  }

  const getTipoBadge = (tipo) => {
    switch (tipo) {
      case 'percentual':
        return 'badge-info'
      case 'valor_fixo':
        return 'badge-primary'
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
        <p className="text-gray-500">Erro ao carregar cupons</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Tag className="w-8 h-8 mr-3 text-blue-600" />
            Cupons
          </h1>
          <p className="text-gray-600">Gerencie cupons de desconto e promoções</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Novo Cupom
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar cupons..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Cupons Table */}
      <div className="card">
        {filteredCupons.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Cupom</th>
                  <th>Descrição</th>
                  <th>Desconto</th>
                  <th>Validade</th>
                  <th>Usos</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredCupons.map((cupom) => (
                  <tr key={cupom.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                          <Tag className="w-5 h-5 text-green-600" />
                        </div>
                        <div>
                          <h4 className="font-medium font-mono">{cupom.codigo}</h4>
                          <span className={`badge ${getTipoBadge(cupom.tipo)}`}>
                            {cupom.tipo}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="text-gray-600">{cupom.descricao || '-'}</span>
                    </td>
                    <td>
                      <div className="flex items-center">
                        {cupom.tipo === 'percentual' ? (
                          <>
                            <Percent className="w-4 h-4 mr-1" />
                            <span className="font-semibold text-green-600">
                              {cupom.valor}%
                            </span>
                          </>
                        ) : (
                          <>
                            <span className="font-semibold text-green-600">
                              R$ {cupom.valor.toFixed(2)}
                            </span>
                          </>
                        )}
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="w-4 h-4 mr-2" />
                        {cupom.data_validade ? 
                          new Date(cupom.data_validade).toLocaleDateString('pt-BR') : 
                          'Sem validade'
                        }
                      </div>
                    </td>
                    <td>
                      <div className="flex items-center text-sm text-gray-600">
                        <Users className="w-4 h-4 mr-2" />
                        {cupom.usos_atuais || 0} / {cupom.usos_limite || '∞'}
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${getStatusBadge(cupom.status)}`}>
                        {cupom.status}
                      </span>
                    </td>
                    <td>
                      <div className="flex space-x-2">
                        <button className="btn btn-secondary btn-sm">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteCupom(cupom.id)}
                          disabled={deleteCupomMutation.isPending}
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
            <Tag className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhum cupom encontrado
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece criando seu primeiro cupom'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Criar Cupom
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Cupons

