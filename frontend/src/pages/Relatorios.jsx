import React, { useState } from 'react'
import { BarChart3, Download, Calendar, TrendingUp, Package, DollarSign, Users, ShoppingCart } from 'lucide-react'
import { 
  useRelatorioFluxoCaixa, 
  useRelatorioPL, 
  useRelatorioTopProdutos, 
  useRelatorioProdutosParados,
  useRelatorioRotatividade,
  useRelatorioSazonalidade 
} from '../hooks/useApi'

function Relatorios() {
  const [activeReport, setActiveReport] = useState('fluxo-caixa')

  // Hooks para diferentes relatórios
  const { data: fluxoCaixaData, isLoading: loadingFluxo } = useRelatorioFluxoCaixa()
  const { data: plData, isLoading: loadingPL } = useRelatorioPL()
  const { data: topProdutosData, isLoading: loadingTopProdutos } = useRelatorioTopProdutos()
  const { data: produtosParadosData, isLoading: loadingProdutosParados } = useRelatorioProdutosParados()
  const { data: rotatividadeData, isLoading: loadingRotatividade } = useRelatorioRotatividade()
  const { data: sazonalidadeData, isLoading: loadingSazonalidade } = useRelatorioSazonalidade()

  const reports = [
    {
      id: 'fluxo-caixa',
      name: 'Fluxo de Caixa',
      icon: DollarSign,
      description: 'Análise de entradas e saídas de caixa',
      color: 'success'
    },
    {
      id: 'pl',
      name: 'P&L (Lucro e Perda)',
      icon: TrendingUp,
      description: 'Demonstrativo de resultados',
      color: 'primary'
    },
    {
      id: 'top-produtos',
      name: 'Top Produtos',
      icon: Package,
      description: 'Produtos mais vendidos',
      color: 'info'
    },
    {
      id: 'produtos-parados',
      name: 'Produtos Parados',
      icon: Package,
      description: 'Produtos com baixa rotatividade',
      color: 'warning'
    },
    {
      id: 'rotatividade',
      name: 'Rotatividade de Estoque',
      icon: BarChart3,
      description: 'Análise de giro de estoque',
      color: 'secondary'
    },
    {
      id: 'sazonalidade',
      name: 'Sazonalidade',
      icon: Calendar,
      description: 'Análise de sazonalidade de vendas',
      color: 'success'
    }
  ]

  const getCurrentData = () => {
    switch (activeReport) {
      case 'fluxo-caixa':
        return { data: fluxoCaixaData, loading: loadingFluxo }
      case 'pl':
        return { data: plData, loading: loadingPL }
      case 'top-produtos':
        return { data: topProdutosData, loading: loadingTopProdutos }
      case 'produtos-parados':
        return { data: produtosParadosData, loading: loadingProdutosParados }
      case 'rotatividade':
        return { data: rotatividadeData, loading: loadingRotatividade }
      case 'sazonalidade':
        return { data: sazonalidadeData, loading: loadingSazonalidade }
      default:
        return { data: null, loading: false }
    }
  }

  const { data, loading } = getCurrentData()

  const handleDownloadReport = () => {
    // Implementar download do relatório
    console.log('Download do relatório:', activeReport)
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center">
          <BarChart3 className="w-8 h-8 mr-3 text-blue-600" />
          Relatórios
        </h1>
        <p className="text-gray-600">Análises e relatórios do seu negócio</p>
      </div>

      {/* Report Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {reports.map((report) => (
          <button
            key={report.id}
            onClick={() => setActiveReport(report.id)}
            className={`card p-4 text-left transition-all ${
              activeReport === report.id 
                ? 'ring-2 ring-blue-500 bg-blue-50' 
                : 'hover:shadow-md'
            }`}
          >
            <div className="flex items-center mb-2">
              <report.icon className={`w-6 h-6 mr-3 text-${report.color}-600`} />
              <h3 className="font-semibold text-gray-900">{report.name}</h3>
            </div>
            <p className="text-sm text-gray-600">{report.description}</p>
          </button>
        ))}
      </div>

      {/* Report Content */}
      <div className="card">
        <div className="card-header">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">
              {reports.find(r => r.id === activeReport)?.name}
            </h3>
            <button 
              className="btn btn-primary"
              onClick={handleDownloadReport}
            >
              <Download className="w-4 h-4 mr-2" />
              Baixar Relatório
            </button>
          </div>
        </div>

        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
            </div>
          ) : data?.success ? (
            <div className="space-y-6">
              {/* Aqui seria renderizado o conteúdo específico de cada relatório */}
              <div className="text-center py-12">
                <BarChart3 className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Relatório {reports.find(r => r.id === activeReport)?.name}
                </h3>
                <p className="text-gray-500 mb-4">
                  Dados do relatório serão exibidos aqui com gráficos e tabelas
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center">
                      <DollarSign className="w-8 h-8 text-green-600 mr-3" />
                      <div>
                        <p className="text-sm text-gray-600">Receita Total</p>
                        <p className="text-2xl font-bold text-gray-900">R$ 0,00</p>
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center">
                      <ShoppingCart className="w-8 h-8 text-blue-600 mr-3" />
                      <div>
                        <p className="text-sm text-gray-600">Vendas</p>
                        <p className="text-2xl font-bold text-gray-900">0</p>
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center">
                      <Users className="w-8 h-8 text-purple-600 mr-3" />
                      <div>
                        <p className="text-sm text-gray-600">Clientes</p>
                        <p className="text-2xl font-bold text-gray-900">0</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <BarChart3 className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Erro ao carregar relatório
              </h3>
              <p className="text-gray-500">
                Não foi possível carregar os dados do relatório
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Relatorios

