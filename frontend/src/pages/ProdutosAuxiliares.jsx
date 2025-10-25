import React, { useState } from 'react'
import { Wrench, Plus, Search, Edit, Trash2, Package, AlertTriangle } from 'lucide-react'
import { useProdutosAuxiliares, useDeleteProdutoAuxiliar } from '../hooks/useApi'

function ProdutosAuxiliares() {
  const [searchTerm, setSearchTerm] = useState('')
  const { data: produtosData, isLoading: loading, error } = useProdutosAuxiliares()
  const deleteProdutoMutation = useDeleteProdutoAuxiliar()

  const produtos = produtosData?.success ? produtosData.data : []

  const filteredProdutos = produtos.filter(produto =>
    produto.nome.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleDeleteProduto = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este produto auxiliar?')) {
      try {
        await deleteProdutoMutation.mutateAsync(id)
      } catch (error) {
        console.error('Erro ao excluir produto auxiliar:', error)
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
        <p className="text-gray-500">Erro ao carregar produtos auxiliares</p>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
            <Wrench className="w-8 h-8 mr-3 text-blue-600" />
            Produtos Auxiliares
          </h1>
          <p className="text-gray-600">Gerencie suprimentos e produtos auxiliares</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          Novo Produto Auxiliar
        </button>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="flex items-center">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            placeholder="Buscar produtos auxiliares..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 border-none outline-none bg-transparent"
          />
        </div>
      </div>

      {/* Products Table */}
      <div className="card">
        {filteredProdutos.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Produto</th>
                  <th>Preço</th>
                  <th>Estoque Atual</th>
                  <th>Estoque Mínimo</th>
                  <th>Categoria</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredProdutos.map((produto) => (
                  <tr key={produto.id}>
                    <td>
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center mr-3">
                          <Wrench className="w-5 h-5 text-orange-600" />
                        </div>
                        <div>
                          <h4 className="font-medium">{produto.nome}</h4>
                          {produto.descricao && (
                            <p className="text-sm text-gray-500">{produto.descricao}</p>
                          )}
                        </div>
                      </div>
                    </td>
                    <td>
                      <span className="badge badge-success">
                        R$ {produto.preco.toFixed(2)}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${
                        produto.estoque_atual <= 0 ? 'badge-danger' :
                        produto.estoque_atual <= produto.estoque_minimo ? 'badge-warning' :
                        'badge-primary'
                      }`}>
                        {produto.estoque_atual}
                      </span>
                    </td>
                    <td>
                      <span className="badge badge-secondary">
                        {produto.estoque_minimo}
                      </span>
                    </td>
                    <td>
                      {produto.categoria ? (
                        <span className="badge badge-info">{produto.categoria}</span>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </td>
                    <td>
                      <span className={`badge ${
                        produto.ativo ? 'badge-success' : 'badge-secondary'
                      }`}>
                        {produto.ativo ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td>
                      <div className="flex space-x-2">
                        <button className="btn btn-secondary btn-sm">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteProduto(produto.id)}
                          disabled={deleteProdutoMutation.isPending}
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
            <Wrench className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhum produto auxiliar encontrado
            </h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'Tente ajustar os filtros de busca' : 'Comece adicionando seu primeiro produto auxiliar'}
            </p>
            <button className="btn btn-primary">
              <Plus className="w-5 h-5 mr-2" />
              Adicionar Produto Auxiliar
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProdutosAuxiliares

