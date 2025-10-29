import React from 'react'
import { 
  Package, 
  Users, 
  Truck, 
  Wrench, 
  ShoppingCart, 
  ShoppingBag,
  AlertTriangle,
  TrendingUp
} from 'lucide-react'
import { useDashboard } from '../hooks/useApi'

function Dashboard() {
  const { data: dashboardData, isLoading: loading, error } = useDashboard()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error || !dashboardData?.success) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Erro ao carregar dados do dashboard</p>
      </div>
    )
  }

  const data = dashboardData.data

  const stats = [
    {
      name: 'Produtos Cadastrados',
      value: data.total_produtos,
      icon: Package,
      color: 'primary',
      subtitle: 'Estoque total'
    },
    {
      name: 'Clientes Ativos',
      value: data.total_clientes,
      icon: Users,
      color: 'success',
      subtitle: 'Base ativa'
    },
    {
      name: 'Fornecedores',
      value: data.total_fornecedores,
      icon: Truck,
      color: 'info',
      subtitle: 'Parceiros'
    },
    {
      name: 'Produtos Auxiliares',
      value: data.total_produtos_auxiliares,
      icon: Wrench,
      color: 'warning',
      subtitle: 'Suprimentos'
    },
    {
      name: 'Vendas do Mês',
      value: `R$ ${data.total_vendas_mes.toFixed(2)}`,
      icon: ShoppingCart,
      color: 'success',
      subtitle: 'Receita'
    },
    {
      name: 'Compras do Mês',
      value: `R$ ${data.total_compras_mes.toFixed(2)}`,
      icon: ShoppingBag,
      color: 'info',
      subtitle: 'Investimento'
    },
    {
      name: 'Estoque Baixo',
      value: data.produtos_estoque_baixo + data.produtos_auxiliares_estoque_baixo,
      icon: AlertTriangle,
      color: data.produtos_estoque_baixo + data.produtos_auxiliares_estoque_baixo > 0 ? 'danger' : 'success',
      subtitle: data.produtos_estoque_baixo + data.produtos_auxiliares_estoque_baixo > 0 ? 'Atenção' : 'OK'
    }
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Dashboard
        </h1>
        <p className="text-gray-600">
          Acompanhe o desempenho do seu negócio em tempo real
        </p>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid mb-8">
        {stats.map((stat, index) => (
          <div key={index} className={`stat-card ${stat.color}`}>
            <div className="flex items-center justify-between">
              <div>
                <div className="stat-number">{stat.value}</div>
                <div className="stat-label">{stat.name}</div>
                <div className="text-sm text-gray-500 mt-1">{stat.subtitle}</div>
              </div>
              <div className="text-gray-400">
                <stat.icon className="w-8 h-8" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and Recent Sales */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sales Chart */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Vendas dos Últimos 7 Dias</h3>
          </div>
          <div className="h-64 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <TrendingUp className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p>Gráfico de vendas será implementado aqui</p>
            </div>
          </div>
        </div>

        {/* Recent Sales */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Vendas Recentes</h3>
          </div>
          <div className="space-y-4">
            {data.vendas_recentes.length > 0 ? (
              data.vendas_recentes.map((venda, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">{venda.cliente_nome}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(venda.data_venda).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-green-600">
                      R$ {venda.total.toFixed(2)}
                    </p>
                    <span className={`badge ${
                      venda.status === 'concluida' ? 'badge-success' : 'badge-warning'
                    }`}>
                      {venda.status}
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <ShoppingCart className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p>Nenhuma venda recente</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Ações Rápidas</h3>
            <p className="text-gray-600">Acesso rápido às principais funcionalidades</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="btn btn-success">
              <ShoppingCart className="w-5 h-5 mr-2" />
              Nova Venda
            </button>
            <button className="btn btn-primary">
              <Package className="w-5 h-5 mr-2" />
              Novo Produto
            </button>
            <button className="btn btn-secondary">
              <Users className="w-5 h-5 mr-2" />
              Novo Cliente
            </button>
            <button className="btn btn-info">
              <Truck className="w-5 h-5 mr-2" />
              Novo Fornecedor
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

